from rest_framework.serializers import ModelSerializer
from .models import UserPasswords


class UserPasswordsSerializer(ModelSerializer):
    class Meta:
        model = UserPasswords
        exclude = ['user']
