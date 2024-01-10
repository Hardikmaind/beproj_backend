# models.py
from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=255)
    is_registered = models.BooleanField(default=False)
    last_three_interviews_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user_name

class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interview_id = models.CharField(max_length=50, unique=True)
    feedback = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the last_three_interviews_feedback field after saving the interview
        interviews = Interview.objects.filter(user=self.user).order_by('-id')[:3]
        feedback_list = [interview.feedback for interview in interviews]
        self.user.last_three_interviews_feedback = ', '.join(feedback_list)
        self.user.save()

    def __str__(self):
        return f"Interview ID: {self.interview_id} - User: {self.user.user_name}"

class InterviewQuestion(models.Model):
    question = models.TextField()

    def __str__(self):
        return self.question


