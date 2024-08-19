from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status as httpstatus
from .serializer import UserSerializer
from django.contrib.auth.models import User
# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    resp = {}
    status = httpstatus.HTTP_400_BAD_REQUEST
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=serializer.data['username']);
        user.set_password(serializer.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        resp['toke'] = token.key
        resp['data'] = serializer.data
        status = httpstatus.HTTP_201_CREATED
    else:
        resp = serializer.errors
    return Response(resp,status)
        