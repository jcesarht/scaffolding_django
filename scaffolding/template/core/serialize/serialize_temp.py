#!/usr/bin/env python3
class SerializeTemplate:
    # initializie the class to use the necesary variable
    def __init__(self):
        self.__app_name = ''
        self.__class_name = ''
        self.__entity_fields = []
        self.__read_only_fields = []
    
    #Get class name
    @property
    def class_name(self):
        return self.__class_name
    
    #Set class name
    @class_name.setter
    def class_name(self, class_name_param):
        self.__class_name = class_name_param
    
    # Get app name 
    @property
    def app_name(self):
        return self.__app_name 
    
    # Set app name
    @app_name.setter
    def app_name(self,app_name_param):
        self.__app_name = app_name_param
    
    
    # Get entity's fields list
    @property
    def entitys_fields(self):
        return self.__entity_fields
    
    # Set all fields that we want send to view
    @entitys_fields.setter
    def entitys_fields(self,fields_param):
        self.__entity_fields = fields_param
    
    
    # Get the fields only read
    @property
    def entitys_fields_only_read(self):
        return self.__read_only_fields
    
    # Set the fields only read
    @entitys_fields_only_read.setter
    def entitys_fields_only_read(self,fields_param):
        self.__read_only_fields = fields_param
    
    # Create a Serialize file 
    def create_serialize_file(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        error_message = ''
        try:
            content = self.__serialize_schema()
            if not content['status']:    
                error_message = 'The serialized file was not created.'
                raise ValueError(error_message)
            
            file_name = f".\\{self.__app_name}\\serializers.py"
            serialize_file = open(file_name,'w+')
            serialize_file.writelines(content['data'])
            response['status']  = True
            response['message'] = 'Serialization was executed successfully'
        except ValueError as e:
            response['message'] = e
        return response
        
    #contains the schema about the file content
    def __serialize_schema(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : ''
        }
        error_message = ''
        try:
            class_name = self.__class_name.capitalize()
            app_name = self.__app_name
            fields_entity = self.__entity_fields
            read_only_fields = self.__read_only_fields
            read_only_fields_code = ''
            if not app_name:
                error_message = 'app_name can not by empty'
                raise ValueError(error_message)
            if not class_name:
                error_message = 'class_name can not by empty'
                raise ValueError(error_message)
            if not fields_entity:
                error_message = 'fields_entity can not by empty'
                raise ValueError(error_message)
            
            if read_only_fields:
                read_only_fields_code = f"read_only_fields = {tuple(read_only_fields)} "
            
            content = [
                'from rest_framework import serializers\n',
                f'from .models import {class_name}\n\n',
                f'class {class_name}Serializer(serializers.ModelSerializer):\n\n',
                '   class Meta:\n',
                f'      model = {class_name}\n',
                f'      field = {tuple(fields_entity)}\n',
                f'      {read_only_fields_code}\n'
            ]
            response['data'] = content
            response['status']  = True
            response['message'] = 'Serializer schema was generated successfully'
        except ValueError as e:
            response['message'] = e
        return response