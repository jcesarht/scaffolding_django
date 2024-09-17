#!/usr/bn/env python3
class viewSetTemplate:
    # initializie the class to use the necesary variable
    def __init__(self) -> None:
        self.__app_name = ''
        self.__class_name = ''
    
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
        
    # Create a viewSet file 
    def create_viewset_file(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        error_message = ''
        try:
            content = self.__viewset_schema()
            if not content['status']:    
                error_message = 'The viewSet file was not created.'
                raise ValueError(error_message)
            
            file_name = f".\\{self.__app_name}\\api.py"
            serialize_file = open(file_name,'w+')
            serialize_file.writelines(content['data'])
            response['status']  = True
            response['message'] = 'viewSet was executed successfully'
        except ValueError as e:
            response['message'] = e
        return response

    #contains the schema about the file content
    def __viewset_schema(self):
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
            
            schema_view_file = open('schema_view.py','r')
            content = ''
            for line in schema_view_file.readlines():
                content += line
            
            response['data'] = content
            response['status']  = True
            response['message'] = 'viewSet schema was generated successfully'
        except ValueError as e:
            response['message'] = e
        return response