#!/usr/bn/env python3
class viewSetTemplate:
    # initializie the class to use the necesary variable
    def __init__(self) -> None:
        self.__app_name = ''
        self.__class_name = ''
        self.__required_fields = {}
    
    #Get class name
    @property
    def class_name(self):
        return self.__class_name
    
    #Set class name 
    @class_name.setter
    def class_name(self,class_name_param):
        self.__class_name = class_name_param
    
    #get app name
    @property
    def app_name (self):
        return self.__app_name
    
    #Set app name 
    @app_name.setter
    def app_name(self, app_name_param):
        self.__app_name = app_name_param
    
    #get required fields
    @property
    def required_fields (self):
        return self.__required_fields
    
    #Set app name 
    @required_fields.setter
    def required_fields(self, required_fields_param):
        self.__required_fields = required_fields_param
        
    # Create a viewSet file 
    def create_viewset_file(self, auth_module = False):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        error_message = ''
        try:
            content = self.__view_schema(auth_module)
            if not content['status']:    
                error_message = 'The viewSet file was not created.'
                raise ValueError(error_message)
            
            file_name = f".\\{self.__app_name}\\views.py"
            serialize_file = open(file_name,'w+')
            serialize_file.writelines(content['data'])
            response['status']  = True
            response['message'] = 'viewSet was executed successfully'
        except ValueError as e:
            response['message'] = e
        return response

    #contains the schema about the file content
    def __view_schema(self, auth_module_param = False):
        response = {
            'status' : False,
            'message' : '',
            'data' : ''
        }
        error_message = ''
        try:
            class_name = self.__class_name.capitalize()
            app_name = self.__app_name
            if not app_name:
                error_message = 'app_name can not by empty'
                raise ValueError(error_message)
            if not class_name:
                error_message = 'class_name can not by empty'
                raise ValueError(error_message)
            schema_view_file = open('.\\scaffolding\\template\\core\\viewset\\schema_view.py','r')
            content = ''
            for line in schema_view_file.readlines():
                if(auth_module_param == True):
                    if('from rest_framework.decorators import api_view' in line):
                        line += '''from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated'''

                    if('transaction_data' in line):
                        line = '''@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])\n''' + line
                content += line
            required_fields = ''
            for field, value in self.__required_fields.items():
               if value['required']:
                    required_fields += '"' +field + '",'
            content_modified = content.replace("{app_name}",class_name).replace("{fields_required}",required_fields)
            response['data'] = content_modified
            response['status']  = True
            response['message'] = 'viewSet schema was generated successfully'
        except ValueError as e:
            response['message'] = e
        return response