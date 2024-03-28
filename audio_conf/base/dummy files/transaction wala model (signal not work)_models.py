# from django.db import models

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     ]

#     user_name = models.CharField(max_length=255)
#     is_registered = models.BooleanField(default=False)
#     last_three_interviews_feedback = models.TextField(blank=True, null=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
#     firebase_uid = models.CharField(max_length=255, default='null')

#     def __str__(self):
#         return self.user_name

# class Interview(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     interview_id = models.AutoField(primary_key=True)
#     type_of_interview = models.CharField(max_length=10, choices=[('HR', 'HR'), ('Technical', 'Technical')], default='HR')
#     feedback = models.TextField()

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         # Update the last_three_interviews_feedback field after saving the interview
#         interviews = Interview.objects.filter(user=self.user).order_by('-id')[:3]
#         feedback_list = [interview.feedback for interview in interviews]
#         self.user.last_three_interviews_feedback = ', '.join(feedback_list)
#         self.user.save()

#     def __str__(self):
#         return f"Interview ID: {self.interview_id} - User: {self.user.user_name} - Type: {self.type_of_interview}"


# class HrInterviewQuestions(models.Model):
#     question_list = models.TextField()

#     def __str__(self):
#         return self.question_list

# class TechnicalInterviewQuestions(models.Model):
#     question_list = models.TextField()

#     def __str__(self):
#         return self.question_list

# class Feedback(models.Model):
#     interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='feedbacks')  # Added related_name
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     feedback = models.TextField()

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         # Update the last_three_interviews_feedback field after saving the feedback
#         feedbacks = Feedback.objects.filter(user=self.user).order_by('-id')[:3]
#         feedback_list = [fb.feedback for fb in feedbacks]
#         self.user.last_three_interviews_feedback = ', '.join(feedback_list)
#         self.user.save()

#     def __str__(self):
#         return f"Interview: {self.interview.interview_id} - User: {self.user.user_name} - Question: {self.question}"







from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user_name = models.CharField(max_length=255)
    is_registered = models.BooleanField(default=False)
    last_three_interviews_feedback = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    firebase_uid = models.CharField(max_length=255, default='null')

    def __str__(self):
        return self.user_name

class HrInterviewQuestions(models.Model):
    question_list = models.TextField()

    def __str__(self):
        return self.question_list

class TechnicalInterviewQuestions(models.Model):
    question_list = models.TextField()

    def __str__(self):
        return self.question_list

class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interview_id = models.AutoField(primary_key=True, editable=False)
    
    user_interview_no=models.IntegerField(default=0,editable=False)
    type_of_interview = models.CharField(max_length=10, choices=[('HR', 'HR'), ('Technical', 'Technical')], default='HR')
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview ID: {self.interview_id} - User: {self.user.user_name} - Type: {self.type_of_interview}  - User Interview No: {self.user_interview_no}"

# Signal to reset interview ID sequence after creating a new user
@receiver(post_save, sender=User)
def reset_interview_id_sequence(sender, instance, created, **kwargs):
    if created:
        user_interview_no = instance.interview_set.aggregate(Max('user_interview_no'))['user_interview_no__max'] or 0
        if user_interview_no:
            instance.interview_set.update(user_interview_no=models.F('user_interview_no') + 1)
        else:
            instance.interview_set.update(user_interview_no=1)


class Feedback(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_text = models.TextField()

    def __str__(self):
        return f"Feedback for Interview ID: {self.interview.interview_id}"