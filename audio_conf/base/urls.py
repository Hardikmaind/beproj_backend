from django.urls import path
from .views import UserView,AudioUploadView,TechQuestions,HrQuestions,InterviewCreate,QuestionFromClient,RateAnswersAPIView,GetInterviewFeedback

urlpatterns = [
    path('create_user/', UserView.as_view(), name='create_user'),
    # path('get_audio/', UserView.as_view(), name='get_audio')
    path('upload_audio/', AudioUploadView.as_view(), name='upload_audio'),
    path('tech_questions/', TechQuestions.as_view(), name='tech_questions'),
    path('hr_questions/', HrQuestions.as_view(), name='hr_questions'),
    path('InterviewCreate-id/', InterviewCreate.as_view(), name='InterviewCreate_id'),
    path('send_ques/',QuestionFromClient.as_view(),name='send_ques'),
    path('rate_answers/', RateAnswersAPIView.as_view(), name='rate_answers_api'),
    path('get_interview_Feedback/',GetInterviewFeedback.as_view(),name='get_interview_Feedback')

    

]
