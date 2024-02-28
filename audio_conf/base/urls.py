from django.urls import path
from .views import UserView,AudioUploadView,TechQuestions,HrQuestions

urlpatterns = [
    path('create_user/', UserView.as_view(), name='create_user'),
    # path('get_audio/', UserView.as_view(), name='get_audio')
    path('upload_audio/', AudioUploadView.as_view(), name='upload_audio'),
    path('tech_questions/', TechQuestions.as_view(), name='tech_questions'),
    path('hr_questions/', HrQuestions.as_view(), name='hr_questions'),

]
