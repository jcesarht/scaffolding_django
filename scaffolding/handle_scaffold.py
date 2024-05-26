#!/usr/bin/env python3
from os import environ as __enviroment__, getcwd, path as __getpath__
from django.db import connection as __con__
from django import setup as __setup__
#import settings conf 
from django.conf import settings as __dgsettings__
import subprocess
from .template.core.serialize.serialize_temp import SerializeTemplate
except_message = ''
class InspectDB:
    # initialize module
    def __init__(self):
        self.__targetdb = ''
        self.__alldbtables = ''
        self.__project_name = ''
        self.__initialize = False
        self.__cursor = None
        self.__sufix_app = '_app'

    # Setting the database table, tables or  the whole database
    def database_target(self,target_param):
        self.__targetdb = target_param
    #Get the database target like table, tables or the whole database 
    def database_target(self):
        return self.__targetdb

    # Setting the main DJango's app name
    def main_project_name(self,project_name_param):
        self.__project_name = project_name_param

    # Get the main DJango's app name
    def main_project_name(self):
        return self.__project_name

    # init module
    def initilize(self):
        response = {
            'status': self.__initialize,
            'message': ''
        }
        output_message = ''
        try:
            self.__targetdb = self.database_target
            self.__project_name = self.main_project_name
            if(self.__targetdb == ''):
                output_message = 'targetdb no puede estar vacio'
                output_message = 'targetdb can not be empty'
                raise ValueError(output_message)
            if(self.__project_name ==''):
                output_message = 'coloca el nombre de la app en el parámetro appname'
                output_message = 'appname can not be empty'
                raise ValueError(output_message)
            __enviroment__.setdefault('DJANGO_SETTINGS_MODULE', self.__project_name + '.settings')
            
            #get cursor where database is connected 
            self.__cursor = __con__.cursor()
            #check which database ENGINE is connected. (mysql, postgrest or sqlite)
            if 'mysql' in __dgsettings__.DATABASES['default']['ENGINE']:
                self.__cursor.execute("SHOW TABLES;");
            elif 'postgresql' in __dgsettings__.DATABASES['default']['ENGINE']:
                # comming soon
                raise ValueError("postgresql comming soon")
            elif 'sqlite3' in __dgsettings__.DATABASES['default']['ENGINE']:
                self.__cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            else:
                output_message = "Engine not supported"
                raise ValueError(output_message)
            
            self.__initialize = True
            response['status'] = self.__initialize
            response['message'] = 'Initialize successfully'
        except ValueError as e:
            response['message'] = e
        return response

    # Return all tables from database like a tupla
    def get_tables_from_cursor(self,cursor_param):
        response = {
            'status': False,
            'message': '',
            'data': None
        }
        output_message = ''
        try:
            if self.__initialize == False:
                output_message = "Module not initialized for get_tables_from_cursor"
                raise ValueError(output_message)
            result_tables = cursor_param.fetchall()
            table_list = []
            for element in result_tables:
                table_list.append(element[0])
            output_message = 'Process get_tables_from_cursor complete'
            response['data'] = tuple(table_list)
            response['message'] = output_message
        except ValueError as e:
            response['message'] = e
        return response
    
    # Create the models 
    def create_model(self,entity_param):
        response = {
            'status': False,
            'message': ''
        }
        
        try:
            output_message = ''
            if self.__initialize == False:
                output_message = "Module not initialized for create_model"
                raise ValueError(output_message)
            
            entity = entity_param
            if entity == "":
                output_message = "Entity have not empty to create_model"
                raise ValueError(output_message)
            
            with open(f'./{entity + self.__sufix_app}/models.py','w') as file:
                p = subprocess.run(["py","manage.py","inspectdb",entity],stdout=file)
                if p.returncode != 0:
                    output_message = f"something was wrong to create model with {entity} entity"
                    raise ValueError(output_message) 
            response['status'] = True  
            response['message'] = f'{entity} model created successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    # Create the entity's app
    def create_app(self,entity_param):
        response = {
            'status': False,
            'message': ''
        }
        try:
            entity = entity_param
            if self.__initialize == False:
                output_message = "Module not initialized for create_app"
                raise ValueError(output_message)
            if entity == "":
                output_message = "Entity have not empty"
                raise ValueError(output_message)
            appname = entity + self.__sufix_app
            p = subprocess.run(["py","manage.py","startapp",appname],stdout=subprocess.PIPE)
            if p.returncode != 0:
                    output_message = f"something was wrong to create app {appname} "
                    raise ValueError(output_message)
            response['status'] = True  
            response['message'] = f'{entity} app created successfully'
        except ValueError as e:
             response['message'] = e
        return response
    
    
    def migration_process(self,entity_param):
        response = {
            'status' : False,
            'message' : ''
        }
        try:
            if self.__initialize == False:
                output_message = "Module not initialized successfully"
                raise ValueError(output_message)
            entity = entity_param
            if not entity:
                output_message = "Entity for create migrations was failed"
                raise ValueError(output_message)
            
            appname = entity + self.__sufix_app
            p = subprocess.run(["py","manage.py","makemigrations",appname],stdout=subprocess.PIPE)
            p = subprocess.run(["py","manage.py","migrate",appname],stdout=subprocess.PIPE)
            response['status'] = True
            response['message'] = 'Setting were executed successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    # create Serialize file
    def create_serialize(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        try:
            serialize_file = SerializeTemplate()
            serialize_file.set_app_name = self.__project_name
            
            response['status']  = True
            response['message'] = 'serialize file process were executed successfully'
        except ValueError as e:
            response['message'] = e
        return response
        
    
    # Reverse all process executed
    def reverse_process(self):
        response = {
            'status': False,
            'message': ''
        }
        try:
            targetdb = self.__targetdb
            if ( targetdb != '.' and targetdb != 'all' ):
                target_list = targetdb.split(',')
                #Verify if all param's tables exists
                for table in target_list:
                    if(table not in self.__alldbtables):
                        output_message  = f"Table {table} not exist in database"
                        raise ValueError(output_message)
                targetdb = target_list
            else:
                targetdb = self.__alldbtables
            # Import the function to delete folders 
            from os import rmdir
            for entity in targetdb:
                rmdir(entity + self.__sufix_app)
                
                output_message = f'{entity + self.__sufix_app} deleted successfully'
                print(output_message)
            output_message = "Process reverse successfully"
            response['status'] = True    
            response['message'] = output_message    
        except ValueError as e:
            response['message'] = e
    #Ask to user
    def ask_user(self,section_question_param):
        section_question = section_question_param
        if(section_question == 'serialize'):
            message_to_user = f'See all fields related to the entity {entity} below'
            print(message_to_user)
    
    #Get all fields         
    def get_all_fields_entity(self,entity_param):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        try:
            entity = entity_param
            module_name = entity + self.__sufix_app + '.models'
            class_name = entity.capitalize()

            module = __import__(module_name, fromlist=[class_name])
            class_model = getattr(module, class_name)
            fields = class_model._meta.get_fields()
            
            response['data'] = fields
            response['status']  = True
            response['message'] = 'get all fields process were executed successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    #Install app in the proyect
    def install_app(self,entity_param):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        output_message = ''
        try:
            entity = entity_param
            appname = entity + self.__sufix_app
            if not entity:
                output_message = "Entity can not be empty for intall app process"
                raise ValueError(output_message)
            
            # path to settings.py file
            settings_file = f'./{self.__project_name}/settings.py'

            # we read the file
            with open(settings_file, 'r') as f:
                lines = f.readlines()
            
            # search INSTALLED_APPS line and add it
            line_number = 0
            for index, line in enumerate(lines):
                if line.startswith('INSTALLED_APPS'):
                    line_number = index
                # in case fin INSTALLED_APPS so start to search the app name or ] character    
                if line_number > 0:
                    #if find the app is installed then break and nothing for make
                    if appname in lines[index]:
                        break
                    #if find de ] character then add the line with the app name 
                    elif ']' in lines[index]:
                        lines[index] = line.rstrip()[:-1] + f"   '{appname}',\n ]\n\n"
                        break
            # re write the setting.py
            with open(settings_file, 'w') as f:
                f.writelines(lines)
    
            response['status']  = True
            output_message = f"{entity} was installed successfully"
            response['message'] = output_message
        except ValueError as e:
            response['message'] = e
        return response
    
    #Main function
    def main_handle(self):
        response = {
            'status': False,
            'message': ''
        }
        
        targetdb = self.__targetdb
        
        try:
            output_message = ''
            if self.__initialize == False:
                output_message = "Module not initialized successfully"
                raise ValueError(output_message)
            
            dbtables = self.get_tables_from_cursor(self.__cursor)
            self.__alldbtables = dbtables['data']
            targetdb = self.__targetdb
            if ( targetdb != '.' and targetdb != 'all' ):
                target_list = targetdb.split(',')
                #Verify if all param's tables exists
                for table in target_list:
                    if(table not in self.__alldbtables):
                        output_message  = f"Table {table} not exist in database"
                        raise ValueError(output_message)
                targetdb = target_list
            else:
                targetdb = self.__alldbtables
            
            for entity in targetdb:
                
                is_create_app = self.create_app(entity)
                if(not is_create_app['status']):
                    output_message  = f"{entity} app has not been created. Please reset the process"
                    raise ValueError(output_message)
                output_message = is_create_app['message']
                print(output_message)
                is_create_model = self.create_model(entity)
                if(is_create_model['status'] == False):
                    output_message  = f"{entity} model has not been created. Please reset the process"
                    raise ValueError(output_message)
                output_message = is_create_model['message']
                print(output_message)
                is_installed_app = self.install_app(entity)
                #installing app
                if(not is_installed_app['status']):
                    output_message  = f"{entity} install app process has not been finished. Please reset the process"
                    raise ValueError(output_message)
                # apply migration
                is_migration_created = self.migration_process(entity)
                if(not is_migration_created['status']):
                    output_message  = f"{entity} migration process has not been finished. Please reset the process"
                    raise ValueError(output_message)
                output_message = is_migration_created['message']
                print(output_message)
                #print(self.get_all_fields_entity(entity))
            output_message = "API created successfully"
            response['status'] = True    
            response['message'] = output_message    
        except ValueError as e:
            response['message'] = e
        return response
        
if __name__ == "__main__":
    print("Sorry this is not main package")
    exit()