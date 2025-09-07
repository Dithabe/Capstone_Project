from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

# Create the serializer class, initialize the password, and lastly, create a class method
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields ='__all__'

    def create(self, acceptable_values):
        user = User.objects.create_user(
            username=acceptable_values['username'],
            password=acceptable_values['password'],
            email=acceptable_values['email'])
        
        return user
    