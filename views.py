from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Course, Lesson, Question, Choice, Submission, Enrollment

@login_required
def take_exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    questions = []
    for lesson in course.lessons.all():
        questions.extend(lesson.questions.all())
    
    if request.method == 'POST':
        return submit_exam(request, course, enrollment, questions)
    
    return render(request, 'exam.html', {'course': course, 'questions': questions})

# Fonction submit corrigée
def submit_exam(request, course, enrollment, questions):
    score = 0
    total_points = 0
    
    with transaction.atomic():
        for question in questions:
            total_points += question.points
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
    
    return redirect('show_exam_result', course_id=course.id)

# Fonction show_exam_result corrigée
@login_required
def show_exam_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    submissions = Submission.objects.filter(user=request.user, question__lesson__course=course)
    
    total_score = sum(s.question.points for s in submissions if s.is_correct)
    possible_score = sum(s.question.points for s in submissions)
    score_percentage = (total_score / possible_score * 100) if possible_score > 0 else 0
    passed = score_percentage >= 70
    
    return render(request, 'exam_result_bootstrap.html', {
        'course': course,
        'submissions': submissions,
        'total_score': total_score,
        'possible_score': possible_score,
        'score_percentage': round(score_percentage, 1),
        'passed': passed
    })
