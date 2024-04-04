from MySQLdb import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, TechnicalInterviewQuestions,HrInterviewQuestions,Interview
from .serializers import UserSerializer,TechnicalInterviewQuestionsSerializer,HrInterviewQuestionsSerializer,InterviewSerializer,FeedbackSerializer
from firebase_admin.exceptions import FirebaseError  # Import the correct exception class
from firebase_admin import auth
from .utils.bert_grammer import grammar
# from pydub import AudioSegment
# import io
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework import status
import os
import assemblyai as aai
import logging
from django.db.models import Max
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


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






# class AudioUploadView(APIView):
#     parser_classes = (MultiPartParser,)
#     transcript_file_path = 'media/transcript.txt'

#     def post(self, request, *args, **kwargs):
#         try:
#             audio_file = request.FILES.get('audio')
#             destination_path = 'media/audio.wav'

#             # Create 'media' folder if it doesn't exist
#             media_folder = os.path.dirname(destination_path)
#             if not os.path.exists(media_folder):
#                 os.makedirs(media_folder)

#             with open(destination_path, 'wb') as destination:
#                 for chunk in audio_file.chunks():
#                     destination.write(chunk)
#             transcriber = aai.Transcriber()

#             # Transcribe the uploaded audio file
#             transcript = transcriber.transcribe(destination_path)

#             # Append the transcript text to the text file
#             with open(self.transcript_file_path, 'a') as transcript_file:
#                 transcript_file.write(transcript.text + '\n')

#             return Response({'message': 'Audio file uploaded successfully.',
#                             'transcription': transcript.text})

#         except Exception as e:
#             error_message = f"An error occurred: {e}"
#             logger.error(error_message)
#             return Response({'error': error_message}, status=500)

class AudioUploadView(APIView):
    parser_classes = (MultiPartParser,)
    transcript_file_path = 'media/transcript.txt'
    audio_folder_path = 'media/'

    def post(self, request, *args, **kwargs):
        try:
            audio_file = request.FILES.get('audio')

            # Create 'media' folder if it doesn't exist
            if not os.path.exists(self.audio_folder_path):
                os.makedirs(self.audio_folder_path)

            # Generate a unique filename based on existing files
            recording_number = self._get_next_recording_number()
            destination_path = os.path.join(self.audio_folder_path, f'Recording ({recording_number}).wav')

            with open(destination_path, 'wb') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            transcriber = aai.Transcriber()

            # Transcribe the uploaded audio file
            transcript = transcriber.transcribe(destination_path)

            # Append the transcript text to the text file
            with open(self.transcript_file_path, 'a') as transcript_file:
                transcript_file.write(transcript.text + '\n')
            grammar(r'audio_conf\media\transcript.txt')

            return Response({
                'message': 'Audio file uploaded successfully.',
                'transcription': transcript.text
            })

        except Exception as e:
            error_message = f"An error occurred: {e}"
            logger.error(error_message)
            return Response({'error': error_message}, status=500)

    def _get_next_recording_number(self):
        # Find the next available recording number
        recording_number = 0
        while os.path.exists(os.path.join(self.audio_folder_path, f'Recording ({recording_number}).wav')):
            recording_number += 1
        return recording_number







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
    
    
    






class InterviewCreate(APIView):
    def post(self, request):
        # Extract data from the request
        user_id = request.data.get('user_id')
        interview_type = request.data.get('interview_type')

        # Check if the interview_type is valid
        if interview_type not in ['HR', 'Technical']:
            return Response({'error': 'Invalid interview type'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists
        try:
            user = User.objects.get(firebase_uid=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create the Interview instance without setting user_interview_no
        interview = Interview(user=user, type_of_interview=interview_type)

        try:
            interview.save()
        except IntegrityError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the interview instance
        serializer = InterviewSerializer(interview)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FeedbackUpdate(APIView):
    def put(self, request, interview_id):
        # Extract data from the request
        feedback = request.data.get('feedback')
        
        # Retrieve the interview instance
        try:
            interview = Interview.objects.get(interview_id=interview_id)
        except Interview.DoesNotExist:
            return Response({'error': 'Interview not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the feedback field
        interview.feedback = feedback
        interview.save()
        
        # Serialize the updated interview instance
        serializer = InterviewSerializer(interview)
        
        return Response(serializer.data, status=status.HTTP_200_OK)





class QuestionFromClient(APIView):
    def post(self, request):
        # Extract data from the request
        interview_questions = request.data.get('interview_questions', [])  # Get the interview questions array

        # Extract question_list attribute from each object in the interview_questions array
        question_list = [question.get('question_list') for question in interview_questions]

        # Define the file path where the text file will be saved
        file_path = 'media/interview_questions.txt'

        try:
            # Check if the file exists, if not, create it
            if not os.path.exists(file_path):
                with open(file_path, 'w') as file:
                    pass  # Create an empty file

            # Write the question_list to the text file
            with open(file_path, 'a') as file:
                for question in question_list:
                    file.write(f'{question}\n')  # Write each question to a new line in the file

            return Response({'message': 'Questions saved to file successfully.'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f'Error saving questions to file: {e}')
            return Response({'error': 'Error saving questions to file.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        














from .utils.geminiModel.gemini import rate_answer
class Getcorrection(APIView):
    def get(self, request):
        # this will not let the code to be in deadlock and prevent from cyclic import
        questions_file = 'media/interview_questions.txt'
        answers_file = 'media/transcript.txt'
        output_file = 'media/correctness.txt'

        # Read questions from the questions file
        try:
            with open(questions_file, 'r') as qf:
                questions = qf.readlines()
        except OSError as e:
            return Response({'error': f"Error reading questions file: {e}"}, status=500)

        # Read answers from the answers file
        try:
            with open(answers_file, 'r') as af:
                answers = af.readlines()
        except OSError as e:
            return Response({'error': f"Error reading answers file: {e}"}, status=500)

        if len(questions) != len(answers):
            return Response({'error': 'Number of questions does not match number of answers'}, status=400)

        output_results = []

        for question, answer in zip(questions, answers):
            question = question.strip()
            answer = answer.strip()

            # Call rate_answer function for each question-answer pair
            rate_answer(question, answer, output_file)

            # Append the result to the output_results list
            output_results.append({'question': question, 'answer': answer})

        return Response({'results': output_results})




