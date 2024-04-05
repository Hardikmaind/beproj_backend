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
    audio_folder_path = 'media/audio/'

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
        
        
        
        

















from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Interview
from .serializers import InterviewSerializer

class GetInterviewFeedback(APIView):
    def get(self, request):
        userid = request.data.get('user')  # Use query_params for GET requests
        
        if userid is None:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            interviews = Interview.objects.filter(user=userid)  # Filter by user ID
            serialized_interviews = InterviewSerializer(interviews, many=True)
            return Response(serialized_interviews.data)
        except Interview.DoesNotExist:
            return Response({'error': 'Interviews not found'}, status=status.HTTP_404_NOT_FOUND)






















# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# import google.generativeai as genai
# import re

# # Set your Gemini API key here
# YOUR_API_KEY = "AIzaSyDKIARUcsy7sU9o5gkmFgg50YX-nY21Thg"
# genai.configure(api_key=YOUR_API_KEY)

# class RateAnswerView(APIView):

#     def get(self, request):
#         try:
#             question = request.GET.get('question')
#             user_answer = request.GET.get('user_answer')

#             if not question or not user_answer:
#                 return Response({'error': 'Please provide both question and user_answer parameters.'},
#                                 status=status.HTTP_400_BAD_REQUEST)

#             rating = rate_answer(question, user_answer, "gemini_output1.txt")  # Adjust output file path if needed

#             return Response({'rating': rating})

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # Re-use the existing functions for rating and extraction

# def rate_answer(question, user_answer, output_file):
#     # Initialize the Gemini model
#     model = genai.GenerativeModel('gemini-pro')

#     # Generate a prompt by combining the question and user's answer
#     prompt = f"Question: {question}\nAnswer: {user_answer}\n Rate the correctness of the answer out of 10."

#     # Generate content using the prompt
#     response = model.generate_content(prompt)

#     # Print the response to inspect it
#     print("Gemini Response:")
#     print(response.text)

#     # Extract the rating from the response
#     rating = extract_rating(response.text)

#     # Write the rating and/or suggestion to the output file
#     with open(output_file, 'a') as f:
#         f.write(f"Question: {question}\nUser's Answer: {user_answer}\n")
#         if rating is not None:
#             if rating >= 7:
#                 f.write(f"Rating: {rating}/10\n\n")
#             else:
#                 f.write(f"Rating: {rating}/10\nSuggestion:\n{response.text}\n\n")
#         else:
#             f.write("Failed to rate the answer.\n\n")

#     return rating

# def extract_rating(response_text):
#     # Search for a numeric rating pattern in the response text
#     match = re.search(r'\b\d+(\.\d+)?/10\b', response_text)
#     if match:
#         rating = float(match.group(0).split('/')[0])
#         if 0 <= rating <= 10:
#             return rating
#     return None




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.ai import generativelanguage_v1beta
from google.generativeai import GenerativeModel
import re

def extract_rating(response_text):
    match = re.search(r'\b\d+(\.\d+)?/10\b', response_text)
    if match:
        rating = float(match.group(0).split('/')[0])
        if 0 <= rating <= 10:
            return rating
    return None

class RateAnswersAPIView(APIView):

    def get(self, request, format=None):
        YOUR_API_KEY = "AIzaSyDKIARUcsy7sU9o5gkmFgg50YX-nY21Thg"  # Hardcoded API key
        if not YOUR_API_KEY:
            return Response({"error": "Gemini API key not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Configure the Gemini API with your API key
        from google.generativeai import configure
        configure(api_key=YOUR_API_KEY)

        questions_file_path = "media/interview_questions.txt"  # Hardcoded file paths
        answers_file_path = "media/transcript.txt"

        with open(questions_file_path, 'r') as questions_file:
            questions = [line.strip() for line in questions_file]

        with open(answers_file_path, 'r') as answers_file:
            answers = [line.strip() for line in answers_file]

        response_data = []
        for question, answer in zip(questions, answers):
            model = GenerativeModel('gemini-pro')
            prompt = f"Question: {question}\nAnswer: {answer}\nRate the correctness of the answer out of 10."
            response = model.generate_content(prompt)
            rating = extract_rating(response.text)

            response_data.append({
                "question": question,
                "answer": answer,
                "rating": rating,
                "suggestion": response.text if rating is not None and rating < 7 else None
            })

        return Response(response_data)






from .utils.confidenceModel.lstm_function import extract_mfcc, classify_audio

audio_folder_path = "media/audio/"

class ConfidenceEstimation(APIView):
    def get(self, request):
        # Define variables for calculating average confidence
        total_confidence = 0
        num_files = 0

        # Iterate through audio files in the folder
        for filename in os.listdir(audio_folder_path):
            if filename.endswith(".wav"):  # Assuming audio files are in WAV format
                audio_file_path = os.path.join(audio_folder_path, filename)
                mfccs = extract_mfcc(audio_file_path)
                prediction = classify_audio(mfccs)
                total_confidence += prediction[1]
                num_files += 1
                print("this is the confidence=======>>>>>>>>>>>>>>>>>>.",total_confidence)

        # Calculate average confidence
        average_confidence = total_confidence / num_files if num_files > 0 else 0

        return Response({'average_confidence': average_confidence})
