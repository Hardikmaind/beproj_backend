from rest_framework import serializers
from .models import User, Interview, InterviewQuestion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
