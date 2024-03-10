# from django.shortcuts import render
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import User, Interview, InterviewQuestion
# from .serializers import UserSerializer
# import firebase_admin
# from firebase_admin import auth

# class UserView(APIView):
#     def post(self, request):
        
#         serializer = UserSerializer(data=request.data)

#         user_name = request.data.get('user_name')
#         is_registered = True 
#         gender = request.data.get('gender') 
#         # user = User.objects.create(user_name=user_name, is_registered=is_registered)

#         if serializer.is_valid():
#             user = serializer.save(is_registered=is_registered)
#             response_data = {
#                 'user_id': user.id,
#                 'user_name':user_name ,
#                 'is_registered':is_registered,
#                 'last_three_interviews_feedback': user.last_three_interviews_feedback,
#                 'gender':gender
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# class UserView(APIView):
#     def post(self, request):
#         # Extract Firebase ID token from the request
#         firebase_id_token = request.data.get('firebase_id_token')

#         try:
#             # Verify Firebase ID token
#             decoded_token = auth.verify_id_token(firebase_id_token)

#             # Get UID from decoded token
#             uid = decoded_token['uid']

#             # Check if a user with this UID already exists in your Django database
#             user = User.objects.filter(firebase_uid=uid).first()

#             if not user:
#                 # If the user doesn't exist, create a new one
#                 serializer = UserSerializer(data={'user_name': decoded_token['name'], 'firebase_uid': uid})
#                 if serializer.is_valid():
#                     user = serializer.save()
#                 else:
#                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#             # Your existing logic for creating or updating user information
#             # ...

#             # Return response with user details
#             response_data = {
#                 'user_id': user.id,
#                 'user_name': user.user_name,
#                 'is_registered': user.is_registered,
#                 'last_three_interviews_feedback': user.last_three_interviews_feedback,
#                 'gender': user.gender
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)

#         except auth.AuthError as e:
#             # Handle authentication error
#             return Response({'error': 'Invalid Firebase ID token'}, status=status.HTTP_401_UNAUTHORIZED)































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


# from django.http import HttpResponse

# class GetAudio(APIView):
#     def post(self, request):
#         audio_data = request.data.get('audio')

#         try:
#             if audio_data:
#                 # Load audio from BytesIO
#                 audio = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")

#                 # Perform operations on audio if needed
#                 # For now, let's convert it back to bytes and send it as a response
#                 audio_bytes = audio.export(format="wav").read()

#                 # Return the audio file as a response
#                 response = HttpResponse(audio_bytes, content_type="audio/wav")
#                 response['Content-Disposition'] = 'attachment; filename="output_audio.wav"'
#                 return response
#             else:
#                 return Response({"message": "No audio data received"}, status=400)
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)



# class AudioUploadAPIView(APIView):
#     parser_classes = [FileUploadParser]

#     def post(self, request, format=None):
#         audio_file = request.data.get('audio')

#         if audio_file is None:
#             return Response({'error': 'No audio file provided'}, status=status.HTTP_400_BAD_REQUEST)

#         # Handle the audio file as needed (e.g., save it, process it)
#         # For example, save the audio file to the media directory
#         audio_path = 'media/' + audio_file.name
#         with open(audio_path, 'wb') as f:
#             f.write(audio_file.read())

#         # Return a response (you might want to customize this)
#         return Response({'message': 'Audio uploaded successfully'}, status=status.HTTP_201_CREATED)



# class AudioUploadView(APIView):
#     parser_classes = (MultiPartParser,)

#     def post(self, request, *args, **kwargs):
#         audio_file = request.FILES.get('audio')

#         with open('media/audio.wav', 'wb') as destination:
#             for chunk in audio_file.chunks():
#                 destination.write(chunk)

#         return Response({'message': 'Audio file uploaded successfully.'})



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



# class AudioUploadView(APIView):
#     parser_classes = (MultiPartParser,)

#     def post(self, request, *args, **kwargs):
#         audio_file = request.FILES.get('audio')
#         destination_path = 'media/audio.wav'

#         # Create 'media' folder if it doesn't exist
#         media_folder = os.path.dirname(destination_path)
#         if not os.path.exists(media_folder):
#             os.makedirs(media_folder)

#         with open(destination_path, 'wb') as destination:
#             for chunk in audio_file.chunks():
#                 destination.write(chunk)

#         return Response({'message': 'Audio file uploaded successfully.'})



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
    
    
    
# class
