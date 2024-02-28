from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import User, Interview

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'is_registered', 'last_three_interviews_feedback')

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('interview_id', 'user', 'feedback')

# @admin.register(InterviewQuestion)
# class InterviewQuestionAdmin(admin.ModelAdmin):
#     list_display = ('question',)
