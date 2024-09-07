#!/usr/bin/env python3
class RouteTemplate:
    
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
        
    # Create a url file 
    def create_url_file(self,create_login = False):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        error_message = ''
        try:
            content = self.__url_schema_login() if (create_login) else self.__url_schema()
            if not content['status']:    
                error_message = 'The viewSet file was not created.'
                raise ValueError(error_message)
            
            file_name = f".\\{self.__app_name}\\urls.py"
            serialize_file = open(file_name,'w+')
            serialize_file.writelines(content['data'])
            response['status']  = True
            response['message'] = 'viewSet was executed successfully'
        except ValueError as e:
            response['message'] = e
        return response

    #contains the schema about the file content
    def __url_schema(self):
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
            
            content = [
                '#!/usr/bin/env python3\n',
                'from rest_framework import routers\n',
                f'from .api import {class_name}ViewSet\n\n',
                'router =  routers.DefaultRouter()\n\n',
                f'router.register("api/{class_name.lower()}", {class_name}ViewSet, "{class_name.lower()}" )\n',
                'urlpatterns = router.urls',
            ]
            response['data'] = content
            response['status']  = True
            response['message'] = 'url schema was generated successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    def __url_schema_login(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : ''
        }
        error_message = ''
        try:
            app_name = self.__app_name
            if not app_name:
                error_message = 'app_name can not by empty'
                raise ValueError(error_message)
            
            content = [
                '#!/usr/bin/env python3\n',
                "from django.urls import path, re_path\n",
                "from django.contrib import admin\n",
                "from .views import register, signin, profile\n",
                "admin.autodiscover()\n",
                "urlpatterns = [\n",
                f"    path('api/v1/{app_name}/register/',register,name='login_register'),\n",
                f"    path('api/v1/{app_name}/',signin,name='login_signin'),\n",
                f"    re_path(r'^api/v1/{app_name}/profile/(?P<user_id_param>[\w-]+)?/?$',profile,name='login_profile'),\n",
                "]",
            ]
            response['data'] = content
            response['status']  = True
            response['message'] = 'url schema was generated successfully'
        except ValueError as e:
            response['message'] = e
        return response