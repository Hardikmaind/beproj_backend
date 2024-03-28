from rest_framework import serializers
from .models import User,TechnicalInterviewQuestions,HrInterviewQuestions ,Interview,Feedback

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
        
        
class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['user', 'interview_id', 'type_of_interview', 'feedback','user_interview_no']
        read_only_fields = ['interview_id']  # We want the interview_id to be generated automatically

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['interview', 'feedback_text']