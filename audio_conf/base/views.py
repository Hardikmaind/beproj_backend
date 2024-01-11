from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Interview, InterviewQuestion
from .serializers import UserSerializer

class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        user_name = request.data.get('user_name')
        is_registered = True 
        gender = request.data.get('gender') 
        # user = User.objects.create(user_name=user_name, is_registered=is_registered)

        if serializer.is_valid():
            user = serializer.save(is_registered=is_registered)
            response_data = {
                'user_id': user.id,
                'user_name':user_name ,
                'is_registered':is_registered,
                'last_three_interviews_feedback': user.last_three_interviews_feedback,
                'gender':gender
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
