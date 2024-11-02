#!usr/bin/env/ python3
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password']
        read_only_fields = ('create_at',) 
