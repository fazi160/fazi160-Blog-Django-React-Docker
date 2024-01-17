from django.shortcuts import render
from rest_framework.views import APIView
from .models import UserPasswords
from .serializers import UserPasswordsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import random
import string
# Create your views here.

class PasswordGenerator(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordsSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve user from the authenticated request
        user = request.user

        # Filter queryset based on the authenticated user
        queryset = UserPasswords.objects.filter(user=user)
        
        # Serialize the queryset
        serializer = self.serializer_class(queryset, many=True)

        # Return the serialized data as a response
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            # print('hello')
            title = request.data['title']
            length = request.data['length']
            types = request.data['types']
            # cap = request.data['cap']
            # small = request.data['small']
            # number = request.data['number']
            # special_char = request.data['special_char']

            password = password_genarator(length, types)
            print(user, title, password,"daaaaaaaaaaaaaaaaaaaaaaaaaa-----------------------------------------------------------")
            data = UserPasswords.objects.create(
                user= user,
                title=title,
                password = password
            )
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    

    def delete(self, request, *args, **kwargs):
        user = request.user

        data_id = request.data['data_id']
        print(data_id, user, '-----------------------------------------------------------------------------------')
        try:
            password_instance = UserPasswords.objects.get(id=data_id)
            # Check if the password instance belongs to the authenticated user
            if password_instance.user == user:
                password_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except UserPasswords.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def password_genarator(length, arr, password=''):
    if len(password) == length:
        char_list = list(password)

        random.shuffle(char_list)

        shuffled_string = ''.join(char_list)
        return shuffled_string

    if 'upper' in arr and len(password) != length:
        password += random.choice(string.ascii_uppercase)
    if 'lower' in arr and len(password) != length:
        password += random.choice(string.ascii_lowercase)
    if 'num' in arr and len(password) != length:
        password += str(random.randint(0, 9))
    if 'special_char' in arr and len(password) != length:
        special_characters = "!@#$%^&*()_-+=<>?/[]{},."
        password += random.choice(special_characters)
    return password_genarator(length, arr, password)
    
    


