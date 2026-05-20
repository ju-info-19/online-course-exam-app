from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission

# Classes importées : ModelAdmin, StackedInline, TabularInline, register, etc.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'lesson', 'points')
    list_filter = ('lesson__course', 'lesson')
    search_fields = ('text',)
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)
    inlines = [QuestionInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)