from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status as httpstatus
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .serializers import EmpleadosSerializer
# Create your views here.

@api_view(['POST','PUT'])
def transaction_data(request,id_param = ''):
    status = httpstatus.HTTP_400_BAD_REQUEST
    data = []
    if request.method == 'POST':
        res = __create_register(request)
        status = res['data']['status']
        data = res['data']
    elif request.method == 'PUT':
        __update_register(request,id_param)
    return Response(data,status)

def __create_register(request_param: Request):
    response = {
        'status' : False,
        'message' : '',
        'data' : []
    }
    try:
        serializer = EmpleadosSerializer(data = request_param.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            response['status']  = True
            response['message'] = 'Proccess were executed successfully'
            data = serializer.data | {'status': httpstatus.HTTP_201_CREATED}
        else:
            for error_field in serializer.errors.keys():
                data[error_field] = serializer.errors[error_field][0].title()
            data = {
                'errors' : data,
                'status': httpstatus.HTTP_400_BAD_REQUEST,
            }
        # add the new  status  
        response['data'] = data
    except ValueError as e:
        response['message'] = e
    return response

def __update_register(request: Request,id_param: str):
    pass