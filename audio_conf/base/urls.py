from django.urls import path
from .views import UserView

urlpatterns = [
    path('create_user/', UserView.as_view(), name='create_user'),
    path('get_audio/', UserView.as_view(), name='get_audio')
]
