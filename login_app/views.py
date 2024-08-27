from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status as httpstatus
from .serializer import UserSerializer

__REQUEST__ = None

@api_view(['POST'])
def register(request):
    result = {
        'error': True,
        'message': '',
        'data': {}
    }
    try:
        __verify_request__(request, 'register')
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
            resp['user'] = serializer.data
            result['error'] = False 
            result['message'] = 'Admin user created successfully'
            result['data'] = resp
            status = httpstatus.HTTP_201_CREATED
        else:
            resp = serializer.errors
    except NameError as ne:
        status = httpstatus.HTTP_400_BAD_REQUEST
        result['message'] = str(ne)
    except Exception :
        status = httpstatus.HTTP_500_INTERNAL_SERVER_ERROR
        result['message'] = 'Your request could not be resolved, please contact support'
    return Response(result,status)

@api_view(['POST'])
def signin(request):
    
    result = {
        'error': True,
        'message': '',
        'data': {}
    }
    status = httpstatus.HTTP_404_NOT_FOUND
    try:
        __verify_request__(request, 'signin')
        
        username = request.data['username']
        password = request.data['password']
        
        user = get_object_or_404(User, username = username)
        if not user.check_password(password):
            result['message'] = 'Password was wrong, please try again'
        else:
            #add user ID to session
            request.session['admin_id'] = user.id
            token = Token.objects.get_or_create(user=user)
            result['message'] = 'Log in successfully'
            result['data'] = {'token': token[0].key}
            result['error'] = False
            status = httpstatus.HTTP_200_OK
    except NameError as ne:
        status = httpstatus.HTTP_400_BAD_REQUEST
        result['message'] = str(ne)
    except Http404 :
        status = httpstatus.HTTP_404_NOT_FOUND
        result['message'] = 'User not found'
    except Exception :
        status = httpstatus.HTTP_500_INTERNAL_SERVER_ERROR
        result['message'] = 'Your request could not be resolved, please contact support'
        
    return Response(result,status=status)

'''Retireve user profile'''
@api_view(['GET'])
def profile(request,user_id_param=None):
    
    result = {
        'error': True,
        'message': '',
        'data': {}
    }
    status = httpstatus.HTTP_404_NOT_FOUND
    user_id = False
    try:
        
        if(user_id_param == None):
            raise NameError('The field user_id is missing')
        user_id = int(user_id_param)
        user = get_object_or_404(User, id=user_id)    
        result['error'] = False
        result['message'] = 'User obtained successfully'
        result['data'] = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined
        }
        status = httpstatus.HTTP_200_OK
    except NameError as ne:
        result['message'] = str(ne)
        status = httpstatus.HTTP_400_BAD_REQUEST
    except Http404 as e404:
        result['message'] = 'User not found'
    except Exception:
        message_error = 'Your request could not be resolved, please contact support'
        if(user_id == False):
            message_error = 'Field user_id must int type, string not supported'
        status = httpstatus.HTTP_500_INTERNAL_SERVER_ERROR
        result['message'] = message_error
    return Response(result,status=status)

'''Verify the fields that coming of request'''
def __verify_request__(request_param,type_endpoint:str):
    # Check every field that if required
    def check_field(valid_field,request_field):
        req_fields = list(request_field.data.keys())
        verified_fields = list(filter(lambda field: field not in req_fields, valid_field))
        if len(verified_fields) > 0:
           raise NameError(f"Field {verified_fields[0]} is missing")
    
    req = request_param
    if(type_endpoint == 'register'):
       valid_fields = ['username','password','email','first_name']
    elif(type_endpoint == 'signin'):
       valid_fields = ['username','password']
    elif(type_endpoint == 'profile'):
        valid_fields = ['id']
    check_field(valid_fields,req)