

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, TechnicalInterviewQuestions,HrInterviewQuestions
from .serializers import UserSerializer,TechnicalInterviewQuestionsSerializer,HrInterviewQuestionsSerializer
from firebase_admin.exceptions import FirebaseError  # Import the correct exception class
from firebase_admin import auth
# from pydub import AudioSegment
# import io
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework import status
import os
import assemblyai as aai
import logging


aai.settings.api_key = "9cbde6c6d6304bdca7188b6c01c9118f"
transcriber = aai.Transcriber()
logger = logging.getLogger(__name__)

class UserView(APIView):
    
    
    def get(self, request):
        # Get the ID token from the request
        id_token = request.headers.get('Authorization', '').split('Bearer ')[-1]

        try:
            # Verify the ID token
            decoded_token = auth.verify_id_token(id_token)
            
            # Extract the UID from the decoded token
            uid = decoded_token['uid']
            
            # Retrieve the User model instance based on UID
            user_instance = User.objects.get(firebase_uid=uid)

            # Serialize the user_instance using DRF serializer
            user_serializer = UserSerializer(user_instance)
            
            return Response({'user': user_serializer.data})
            
        except auth.ExpiredIdTokenError:
            return Response({'error': 'Expired ID token'}, status=status.HTTP_401_UNAUTHORIZED)
        except auth.InvalidIdTokenError:
            return Response({'error': 'Invalid ID token'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    
    
    
    
    def post(self, request):
        # Extract Firebase ID token and form data from the request
        firebase_id_token = request.data.get('firebase_id_token')
        user_data = {
            'user_name': request.data.get('user_name'),
            'gender': request.data.get('gender'),
        }

        try:
            # Verify Firebase ID token
            decoded_token = auth.verify_id_token(firebase_id_token)

            # Get UID from decoded token
            uid = decoded_token['uid']

            is_registered = True
            # Check if a user with this UID already exists in your Django database
            user = User.objects.filter(firebase_uid=uid).first()

            if not user:
                # If the user doesn't exist, create a new one
                serializer = UserSerializer(data={**user_data, 'firebase_uid': uid})
                # serializer = UserSerializer()
                if serializer.is_valid():
                    user = serializer.save(is_registered=is_registered)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Your existing logic for creating or updating user information
            # ...

            # Return response with user details
            response_data = {
                'user_id': user.id,
                'user_name': user.user_name,
                'is_registered': is_registered,
                'last_three_interviews_feedback': user.last_three_interviews_feedback,
                'gender': user.gender
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except FirebaseError  as e:
            # Handle authentication error
            return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)






class AudioUploadView(APIView):
    parser_classes = (MultiPartParser,)
    transcript_file_path = 'media/transcript.txt'

    def post(self, request, *args, **kwargs):
        try:
            audio_file = request.FILES.get('audio')
            destination_path = 'media/audio.wav'

            # Create 'media' folder if it doesn't exist
            media_folder = os.path.dirname(destination_path)
            if not os.path.exists(media_folder):
                os.makedirs(media_folder)

            with open(destination_path, 'wb') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)
            transcriber = aai.Transcriber()

            # Transcribe the uploaded audio file
            transcript = transcriber.transcribe(destination_path)

            # Append the transcript text to the text file
            with open(self.transcript_file_path, 'a') as transcript_file:
                transcript_file.write(transcript.text + '\n')

            return Response({'message': 'Audio file uploaded successfully.',
                            'transcription': transcript.text})

        except Exception as e:
            error_message = f"An error occurred: {e}"
            logger.error(error_message)
            return Response({'error': error_message}, status=500)







class TechQuestions(APIView):
    def get(self, request):
        interview_questions = TechnicalInterviewQuestions.objects.all().order_by('?')[:10]
        serialized_questions = TechnicalInterviewQuestionsSerializer(interview_questions, many=True)  # Replace YourSerializerNameHere with your actual serializer
        return Response({'interview_questions': serialized_questions.data})
    


class HrQuestions(APIView):
    def get(self, request):
        interview_questions = HrInterviewQuestions.objects.all().order_by('?')[:10]
        serialized_questions = HrInterviewQuestionsSerializer(interview_questions, many=True)  # Replace YourSerializerNameHere with your actual serializer
        return Response({'interview_questions': serialized_questions.data})
    
    
    
class generate_interviewId(APIView):
    def get(self, request):
        interview_id = Interview.objects.latest('interview_id')
        return Response({'interview_id': interview_id.interview_id+1})
