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
from .models import User, Interview, InterviewQuestion
from .serializers import UserSerializer
from firebase_admin.exceptions import FirebaseError  # Import the correct exception class
from firebase_admin import auth



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
