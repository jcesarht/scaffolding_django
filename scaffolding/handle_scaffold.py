#!/usr/bin/env python3
from os import environ as __enviroment__, getcwd, path as __getpath__
from django.db import connection as __con__
from django import setup as __setup__
import subprocess
from sys import path 
except_message = ''
class InspectDB:
    # initialize module
    def __init__(self):
        self.__targetdb = ''
        self.__alldbtables = ''
        self.__appname = ''
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
    def main_appname(self,appname_param):
        self.__appname = appname_param

    # Get the main DJango's app name
    def main_appname(self):
        return self.__appname

    # init module
    def initilize(self):
        response = {
            'status': self.__initialize,
            'message': ''
        }
        output_message = ''
        try:
            self.__targetdb = self.database_target
            self.__appname = self.main_appname
            if(self.__targetdb == ''):
                output_message = 'targetdb no puede estar vacio'
                output_message = 'targetdb can not be empty'
                raise ValueError(output_message)
            if(self.__appname ==''):
                output_message = 'coloca el nombre de la app en el parámetro appname'
                output_message = 'appname can not be empty'
                raise ValueError(output_message)
            __enviroment__.setdefault('DJANGO_SETTINGS_MODULE', self.__appname + '.settings')
            #import settings conf 
            from django.conf import settings as __dgsettings__
            #get cursor where database is connected 
            self.__cursor = __con__.cursor()
            #check database's ENGINE is connected. (mysql, postgrest or sqlite)
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

    # Return all database or tables like a tupla
    def getTablesFromCursor(self,cursor_param):
        response = {
            'status': False,
            'message': '',
            'data': None
        }
        output_message = ''
        try:
            if self.__initialize == False:
                output_message = "Module not initialized for getTablesFromCursor"
                raise ValueError(output_message)
            result_tables = cursor_param.fetchall()
            table_list = []
            for element in result_tables:
                table_list.append(element[0])
            output_message = 'Process getTablesFromCursor complete'
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
            p = subprocess.run(["py","manage.py","startapp",entity + self.__sufix_app],stdout=subprocess.PIPE)
            response['status'] = True  
            response['message'] = f'{entity} app created successfully'
        except ValueError as e:
             response['message'] = e
        return response
    
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
            
            dbtables = self.getTablesFromCursor(self.__cursor)
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
                if(not is_create_model['status']):
                    output_message  = f"{entity} model has not been created. Please reset the process"
                    raise ValueError(output_message)
                output_message = is_create_model['message']
                print(output_message)
            self.setting_process()
            output_message = "API created successfully"
            response['status'] = True    
            response['message'] = output_message    
        except ValueError as e:
            response['message'] = e
        return response
    
    def setting_process(self):
        response = {
            'status' : False,
            'message' : ''
        }
        try:
            if self.__initialize == False:
                output_message = "Module not initialized successfully"
                raise ValueError(output_message)
            p = subprocess.run(["py","manage.py","makemigrations"],stdout=subprocess.PIPE)
            print(p)
            p = subprocess.run(["py","manage.py","migrate"],stdout=subprocess.PIPE)
            print(p)
            response['status'] = True
            response['message'] = 'Setting were executed successfully'
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
        
if __name__ == "__main__":
    print("Sorry this is not main package")
    exit()