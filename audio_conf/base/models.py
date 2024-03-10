# # models.py
# from django.db import models

# class User(models.Model):
#     id = models.AutoField(primary_key=True)  # Add this line
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),
#     ]

#     user_name = models.CharField(max_length=255)
#     is_registered = models.BooleanField(default=False)
#     last_three_interviews_feedback = models.TextField(blank=True, null=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
#     firebase_uid = models.CharField(max_length=255, default='null')  # Add this line



#     def __str__(self):
#         return self.user_name

# class Interview(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     interview_id = models.CharField(max_length=50, unique=True)
#     feedback = models.TextField()

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         # Update the last_three_interviews_feedback field after saving the interview
#         interviews = Interview.objects.filter(user=self.user).order_by('-id')[:3]
#         feedback_list = [interview.feedback for interview in interviews]
#         self.user.last_three_interviews_feedback = ', '.join(feedback_list)
#         self.user.save()

#     def __str__(self):
#         return f"Interview ID: {self.interview_id} - User: {self.user.user_name}"

# class feedback(models.Model):
#     question = models.TextField()

#     def __str__(self):
#         return self.question
    
# class HrinterviewId(models.Model):
#     quesionlist=models.TextField()
    
#     def __str__(self):
#         return self.quesionlist
    
# class TechnicalinterviewQuestions(models.Model):
#     quesionlist=models.TextField()
    
#     def __str__(self):
#         return self.quesionlist

















from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
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

class Interview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interview_id = models.AutoField(primary_key=True)
    type_of_interview = models.CharField(max_length=10, choices=[('HR', 'HR'), ('Technical', 'Technical')], default='HR')
    feedback = models.TextField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the last_three_interviews_feedback field after saving the interview
        interviews = Interview.objects.filter(user=self.user).order_by('-id')[:3]
        feedback_list = [interview.feedback for interview in interviews]
        self.user.last_three_interviews_feedback = ', '.join(feedback_list)
        self.user.save()

    def __str__(self):
        return f"Interview ID: {self.interview_id} - User: {self.user.user_name} - Type: {self.type_of_interview}"


class HrInterviewQuestions(models.Model):
    question_list = models.TextField()

    def __str__(self):
        return self.question_list

class TechnicalInterviewQuestions(models.Model):
    question_list = models.TextField()

    def __str__(self):
        return self.question_list

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