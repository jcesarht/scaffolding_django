#!usr/bin/env/ python3
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status as httpstatus
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .models import {app_name}
from .serializers import {app_name}Serializer
# Create your views here.

@api_view(['POST','PUT','GET','DELETE'])
def transaction_data(request,id_param = ''):
    status = httpstatus.HTTP_400_BAD_REQUEST
    data = []
    if request.method == 'POST':
        verified_fields = __verify_request__(request)
        if(verified_fields['error']):
            status = httpstatus.HTTP_400_BAD_REQUEST
            data = {
                'error': verified_fields['error'],
                'message': verified_fields['message'],
                'http_status': httpstatus.HTTP_400_BAD_REQUEST     
            }
        else:
            res = __create_register(request)
            status = res['data']['http_status']
            data = res['data']
            
    elif request.method == 'PUT':
        if id_param == '':
            status = httpstatus.HTTP_400_BAD_REQUEST
            error_message = 'This field is required in url.'
            data = {
                'errors': {
                    'id': error_message
                },
                'status': httpstatus.HTTP_400_BAD_REQUEST
            }
        else:
            res = __update_register(request,id_param)
            data = {}
            if(not res['status']):    
                status = res['data']['http_status']
                data = res['data']
            else:
                data = res['data']
                status = res['data']['http_status']
    elif request.method == 'GET':
        res = __query() if id_param == '' else __query(id_param)
        status = res['data']['http_status']
        if (not res['status']):
            error_message = res['message']
            data = {
                'errors': {
                    'message': error_message
                },
                'http_status': res['data']['http_status']
            }
        else:
            data = res['data']
            status = res['data']['http_status'] 
    elif request.method == 'DELETE':
        if id_param == '':
            status = httpstatus.HTTP_400_BAD_REQUEST
            error_message = 'This field is required in url.'
            data = {
                'errors': {
                    'id param': error_message
                },
                'status': httpstatus.HTTP_400_BAD_REQUEST
            }
        else:
            res = __delete(id_param)
            data = {}
            status = res['data']['http_status']
            data = res['data']
            
    return Response(data,status)

def __create_register(request_param: Request):
    response = {
        'status' : False,
        'message' : '',
        'data' : []
    }
    try:
        serializer = {app_name}Serializer(data = request_param.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            response['status']  = True
            response['message'] = 'Proccess were executed successfully'
            data = serializer.data | {'http_status': httpstatus.HTTP_201_CREATED}
        else:
            for error_field in serializer.errors.keys():
                data[error_field] = serializer.errors[error_field][0].title()
            data = {
                'errors' : data,
                'http_status': httpstatus.HTTP_400_BAD_REQUEST,
            }
        # add the new  status  
        response['data'] = data
    except ValueError as e:
        response['message'] = e
    return response

def __update_register(request: Request,id_param: str):
    response = {
        'status' : False,
        'message' : '',
        'data' : {}
    }
    data = {}
    try:
        entity_object = get_object_or_404({app_name}, emp_id = id_param)
        serializer = {app_name}Serializer(entity_object, data=request.data)
        if(serializer.is_valid()):
            serializer.save()    
            response['status']  = True
            response['message'] = 'Proccess were executed successfully'
            data = {
                'data':serializer.data,
                'http_status': httpstatus.HTTP_200_OK
            }
        else:
            for error_field in serializer.errors.keys():
                data[error_field] = serializer.errors[error_field][0].title()
            data = {
                'errors' : data,
                'http_status': httpstatus.HTTP_400_BAD_REQUEST,
            }
            response['message'] = 'Bad request'
        # add the new  status  
        response['data'] = data
    except ValueError:
        error_message = 'A value is wrong, please check your data'
        data['errors'] = {'message':error_message}
        data['http_status'] = httpstatus.HTTP_400_BAD_REQUEST
        response['message'] = error_message
    except Http404:
        error_message = f'record with id {id_param} not found'
        data['http_status'] = httpstatus.HTTP_400_BAD_REQUEST
        data['errors'] = {'message':error_message}
        response['message'] = error_message
    except Exception:
        error_message = 'Something was wrong, please contact support'
        data = {
            'errors': {'message':error_message},
            'http_status': httpstatus.HTTP_500_INTERNAL_SERVER_ERROR
        }
        response['message'] = error_message
    response['data'] = data
    return response

def __query(id_param:str = None):
    response = {
        'status' : False,
        'message' : '',
        'data' : {}
    }
    data = {}
    try:
        if(id_param == None):
            query_set = {app_name}.objects.all()
            serializer = {app_name}Serializer(query_set,many=True)
            data = serializer.data                
        else:
            query_set = get_object_or_404({app_name}, emp_id = id_param)
            serializer = {app_name}Serializer(query_set)                
            data  = serializer.data
        data = {
            'data': data,
            'http_status': httpstatus.HTTP_200_OK
        }
        response['status']  = True
        response['message'] = 'Proccess were executed successfully'
    except ValueError:
        data['http_status'] = httpstatus.HTTP_500_INTERNAL_SERVER_ERROR
        response['message'] = 'Something was wrong with param in query'
    except Http404:
        error_message = f'record with id {id_param} not found'
        data = {
            'data': data,
            'http_status': httpstatus.HTTP_200_OK
        }
        response['status'] = True
        response['message'] = error_message
    except Exception:
        error_message = 'Something was wrong, please contact support'
        data = {
            'http_status': httpstatus.HTTP_500_INTERNAL_SERVER_ERROR
        }
        response['message'] = error_message
    response['data'] = data 
    return response

def __delete(id_param:str = None):
    response = {
        'status' : False,
        'message' : '',
        'data' : {}
    }
    data={}
    status = httpstatus.HTTP_404_NOT_FOUND
    try:
        if (id_param == None):
            raise ValueError
        
        query_set = get_object_or_404({app_name}, emp_id = id_param)
        query_set.delete()
        serialize = {app_name}Serializer(query_set)
        data = {
            'data': serialize.data,
        }
        status = httpstatus.HTTP_204_NO_CONTENT
        response['status']  = True
        response['message'] = 'Proccess were executed successfully'
    except ValueError:
        status = httpstatus.HTTP_400_BAD_REQUEST
        error_message = 'id parameter is missing, can not deleted record'
        data['errors'] = {'message':error_message}
        response['message'] = error_message
    except Http404:
        error_message = f'record with id {id_param} not found'
        data['http_status'] = httpstatus.HTTP_400_BAD_REQUEST
        data['errors'] = {'message':error_message}
        response['message'] = error_message
    except Exception:
        error_message = 'Something was wrong, please contact support'
        status = httpstatus.HTTP_500_INTERNAL_SERVER_ERROR
        response['message'] = error_message
        data['errors'] = {'message':error_message}
    data['http_status'] = status
    response['data'] = data
    return response

def __verify_request__(request_param:Request):
    """verify fields if are required

    Args:
        request_param (_Request_): requestnparams
        type_endpoint (str): type request
    """
    def check_field(valid_field,request_field):
        """
        Validate fields required
        Args:
            valid_field (list): list of mandatory fields
            request_field (list): list of inputs from front-end 

        Raises:
            NameError: An exception is raised when any field required does not exist
        """
        response = {
            'error': False,
            'message': ''
        }
        req_fields = list(request_field.data.keys())
        verified_fields = list(filter(lambda field: field not in req_fields, valid_field))
        if len(verified_fields) > 0:
           response['error'] = True
           response['message'] = f"Field {verified_fields[0]} is missing"
        return response
    
    req = request_param
    valid_fields = ["emp_id","fecha_ingreso",]
    
    req = request_param
    valid_fields = [{fields_required}]
    
    return check_field(valid_fields,req)     