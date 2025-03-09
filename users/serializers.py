from rest_framework import serializers
from . models import User

#Serializers for each model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User 
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'password']
    