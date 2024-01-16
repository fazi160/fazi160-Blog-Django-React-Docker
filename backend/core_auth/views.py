from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User
import re


class HomeView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {
            'message': 'Welcome to the JWT Authentification page using React Js and Django!'}
        return Response(content)


class CheckWithoutPermission(APIView):
    def get(self, request):
        content = {
            'message': 'this is not authenticated so the data will be got anyone with link no need to send anything'}
        return Response(content)


class LogoutView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    def post(self, request):
        print(request.data,"request.data")
        try:
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            user_type = request.data['user_type']

            if not (username and email and password):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            else:

                validation_result = password_validator(password)

                if len(username) > 50 or len(username) < 3:
                    content = {
                        'message': 'the length of username should be less than 50 and greater than 3'}
                    return Response(content, status=status.HTTP_411_LENGTH_REQUIRED)

                elif not is_valid_email(email):
                    content = {'message': 'Please enter a proper email'}
                    return Response(content, status=status.HTTP_406_NOT_ACCEPTABLE)

                elif validation_result is not True:
                    content = {'message': 'In password ' + validation_result}
                    print(validation_result,"password")
                    return Response(content, status=status.HTTP_412_PRECONDITION_FAILED)


            if User.objects.filter(username=username).exists():
                content = {'message': 'Username already exists'}
                return Response(content, status=status.HTTP_409_CONFLICT)
            
            if User.objects.filter(email=email).exists():
                content = {'message': 'email already exist'}
                return Response(content, status=status.HTTP_409_CONFLICT)


           
            user = User.objects.create(
                username=username,
                email=email,
                user_type=user_type
            )

            user.set_password(password)

            user.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print("some error", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


def is_valid_email(email):
    # Regular expression for a simple email validation
    email_pattern = r'^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z-.]+$'

    # Check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False


def password_validator(password):
    if len(password) < 8:
        return "too small"
    if not re.search(r'[a-z]', password):
        return "Small letter is missing"
    elif not re.search(r'[0-9]', password):
        return "Number is missing"
    elif not re.search(r'[A-Z]', password):
        return "Capital letter is missing"
    elif not re.search(r'^(?=.*[\W_])', password):
        return "Special character is missing"
    else:
        return True
