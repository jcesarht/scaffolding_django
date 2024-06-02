#!/usr/bin/env python3
class SerializeTemplate:
    # initializie the class to use the variable necesary
    def __init__(self):
        self.__appname = '';
        self.__entity_fields = [];
        self.__read_only_fields = [];
    
    # Set app name
    def set_app_name(self,app_name_param):
        self.__appname = app_name_param
    
    # Get app name 
    def get_app_name(self):
        return self.__appname 
    
    # Set all fields that we want send to view
    def set_entitys_fields(self,fields_param):
        self.__entity_fields = fields_param
    
    # Get entity's fields list
    def get_entitys_fields(self):
        return self.__entity_fields
    
    # Create a Serialize file 
    def create_serialize_file(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        error_message = ''
        try:
            content = self.__serialize_schema();
            if not content['status']:    
                error_message = 'The serialized file was not created.'
                raise ValueError(error_message)
            file_name = f".\\{self.__appname}\\serializers.py"
            serialize_file = open(file_name,'w')
            serialize_file.writelines(content)
            response['status']  = True
            response['message'] = 'Proccess was executed successfully'
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
            class_name = self.__appname.capitalize()
            fields_entity = self.__entity_fields
            read_only_fields = self.__read_only_fields
            read_only_fields_code = ''
            if not class_name:
                error_message = 'class_name can not by empty'
                raise ValueError(error_message)
            if not fields_entity:
                error_message = 'fields_entity can not by empty'
                raise ValueError(error_message)
            
            if read_only_fields:
                read_only_fields_code = f"""
                read_only_fields = {tuple(read_only_fields)}
                """
            response['data'] = f"""
            from rest_framework import serializers\n
            from .models import {class_name}\n
            \n
            class {class_name}Serializer(serializers.ModelSerializer):\n
                class Meta:\n
                    model = {class_name}\n
                    field = {tuple(fields_entity)}\n
                    {read_only_fields_code}\n
            """
            response['status']  = True
            response['message'] = 'Proccess were executed successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    
        
        