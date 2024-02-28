from rest_framework import serializers
from .models import User,TechnicalInterviewQuestions,HrInterviewQuestions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TechnicalInterviewQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalInterviewQuestions
        fields = '__all__'
        

class HrInterviewQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrInterviewQuestions
        fields = '__all__'