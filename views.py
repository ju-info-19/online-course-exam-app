from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Course, Lesson, Question, Choice, Submission

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_details_bootstrap.html', {'course': course})

@login_required
def take_exam(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.questions.all()
    
    if request.method == 'POST':
        return submit_exam(request, lesson, questions)
    
    return render(request, 'exam.html', {'lesson': lesson, 'questions': questions})

# Fonction submit
def submit_exam(request, lesson, questions):
    score = 0
    total = questions.count()
    
    with transaction.atomic():
        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                selected_choice = get_object_or_404(Choice, id=selected_choice_id)
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += question.points
                
                Submission.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={
                        'selected_choice': selected_choice,
                        'is_correct': is_correct
                    }
                )
    
    return redirect('show_exam_result', lesson_id=lesson.id)

# Fonction show_exam_result
@login_required
def show_exam_result(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    submissions = Submission.objects.filter(user=request.user, question__lesson=lesson)
    
    total_questions = lesson.questions.count()
    correct_answers = submissions.filter(is_correct=True).count()
    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    passed = score_percentage >= 70
    
    return render(request, 'exam_result.html', {
        'lesson': lesson,
        'submissions': submissions,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': round(score_percentage, 1),
        'passed': passed
    })