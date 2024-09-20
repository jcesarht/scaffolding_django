#!/usr/bin/env python3
#import tools to works
from os import environ as __enviroment__, getcwd, path as __getpath__
from django.db import connection as __con__
from django import setup as __setup__
import importlib
#import settings conf 
from django.conf import settings as __dgsettings__
import subprocess
#Import our librarys based on template
from .template.core.serialize.serialize_temp import SerializeTemplate
from .template.core.viewset.viewset import viewSetTemplate
from .template.core.url.route import RouteTemplate
import template.core.login.login_temp as loginView
from .manager_files_backups import ManagerSettingFile
except_message = ''
class InspectDB:
    # initialize module
    def __init__(self):
        self.__targetdb = ''
        self.__alldbtables = ''
        self.__project_name = ''
        self.__include_frontend = False
        self.__include_login_module = False
        self.__initialize = False
        self.__cursor = None
        self.__sufix_app = '_app'
        self.__manager_setting_file = ManagerSettingFile()

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
            # prepare the copy folder in case to restore
            self.__manager_setting_file.project_name = self.__project_name
            copy_setting = self.__manager_setting_file.copy_setting_file()
            if(copy_setting['status'] and copy_setting['data'] == 'created'):
                # Create config file to restore
                self.__manager_setting_file.create_scaffolding_config_file()
                print(copy_setting['message'])
            elif(copy_setting['status'] and copy_setting['data'] == 'exist'):
                print("setting already exist")
            else:
                print('settings.py did not create')
            copy_url = self.__manager_setting_file.copy_url_file()
            if(copy_url['status'] and copy_url['data'] == 'created'):
                # Create config file to restore
                self.__manager_setting_file.create_scaffolding_config_file()
                print(copy_url['message'])
            elif(copy_url['status'] and copy_url['data'] == 'exist'):
                print("url.py already exist")
            else:
                print('urls.py file did not create')
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
            with open(f'./{entity + self.__sufix_app}/models.py','r') as file:
                lines = file.readlines()
            #search all forenig keys in model.py 
            foreing_keys = []
            content_file = []
            keyword = "ForeignKey('"
            flat_label_app=0
            for index, line in enumerate(lines):
                if keyword in line:
                    start = line.find(keyword) + 12
                    end = line.find("'",start)
                    foreing_key = line[start:end]
                    line = line.replace("\'","",2)
                    foreing_keys.append(
                        {
                            'line':index,
                            'foreing_key': foreing_key
                        }
                    )
                if "class Meta:" in line and flat_label_app == 0:
                    line = line + f"\n        app_label = '{entity + self.__sufix_app}'\n"
                    flat_label_app = 1
                content_file.append(line)
            #insert foreing keys into file model.py
            flat = 0
            for index, line in enumerate(content_file):
                if 'from' in line and flat == 0:
                    flat = 1
                elif 'from' not in line and flat == 1:
                    for fkey in foreing_keys:
                        str_app = f"{fkey['foreing_key']}"+self.__sufix_app
                        str_import = f'from {str_app.lower()}.models import {fkey["foreing_key"]}'
                        content_file.insert(index,str_import)
                    flat = 2
            # rewrite model.py    
            with open(f'./{entity + self.__sufix_app}/models.py','w') as file:
                file.writelines(content_file)
            response['status'] = True  
            response['message'] = f'{entity} model created successfully'
        except ValueError as e:
            response['message'] = e
        # except TypeError as tye:
        #     response['message'] = tye
        except AttributeError as atre:
            response['message'] = atre
        return response
    
    # Create the entity's app
    def create_app(self,entity_param: str) -> dict:
        """Create an app or starapp inside of the  application

        Args:
            entity_param (str): app name

        Raises:
            ValueError: if initailize in bad
            ValueError: param appname is empty
            ValueError: An error occurred creating the app 

        Returns:
            dict: _description_
        """
        response = {
            'status': False,
            'message': ''
        }
        try:
            appname = entity_param
            if self.__initialize == False:
                output_message = "Module not initialized for create_app"
                raise ValueError(output_message)
            if appname == "":
                output_message = "Entity have not empty"
                raise ValueError(output_message)
            p = subprocess.run(["py","manage.py","startapp",appname],stdout=subprocess.PIPE)
            if p.returncode != 0:
                    output_message = f"something was wrong to create app {appname} "
                    raise ValueError(output_message)
            response['status'] = True  
            response['message'] = f'{appname} app created successfully'
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
            response['message'] = f'{entity} setting was implemented successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    # create Serialize file
    def create_serialization(self,entity_param):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        try:
            entity = entity_param
            if self.__initialize == False:
                output_message = "Module not initialized for serialize file"
                raise ValueError(output_message)
            if entity == "":
                output_message = "Entity have not empty"
                raise ValueError(output_message)
            # User must answer somes questions
            input_data = self.ask_user('serialization',entity)
            if not input_data['status']:
                raise ValueError("Something was wrong getting inputs; Try again please")
            #create serialize file
            serialize_file = SerializeTemplate()
            serialize_file.class_name = entity
            serialize_file.app_name = entity + self.__sufix_app
            serialize_file.entitys_fields = input_data['data'][0]
            serialize_file.entitys_fields_only_read = input_data['data'][1]
            response_ser = serialize_file.create_serialize_file()
            if(not response_ser['status']):
                raise ValueError("Serialization was not created")
            response['status']  = True
            response['message'] = 'serialize file process was executed successfully'
            response['data'] = [serialize_file.entitys_fields, serialize_file.entitys_fields_only_read]
        except ValueError as e:
            response['message'] = e
        return response
    
    #Create viewSet file
    def create_viewset_file(self,entity_param):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        try:
            entity = entity_param
            if self.__initialize == False:
                output_message = "Module not initialized for viewset"
                raise ValueError(output_message)
            if entity == "":
                output_message = "Entity have not empty"
                raise ValueError(output_message)
            #create viewSet file
            viewset_file = viewSetTemplate()
            viewset_file.class_name = entity
            viewset_file.app_name = entity + self.__sufix_app
            response_ser = viewset_file.create_viewset_file()
            if(not response_ser['status']):
                raise ValueError("Viewset was not created")
            response['status']  = True
            response['message'] = 'Viewset file process was executed successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    #Create viewSet file
    def create_url_file(self,entity_param):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        try:
            entity = entity_param
            if self.__initialize == False:
                output_message = "Module not initialized for view"
                raise ValueError(output_message)
            if entity == "":
                output_message = "Entity have not empty"
                raise ValueError(output_message)
            #create url file
            route_file = RouteTemplate()
            route_file.class_name = entity
            route_file.app_name = entity + self.__sufix_app
            response_router = route_file.create_url_file()
            if(not response_router['status']):
                raise ValueError("View was not created")
            response['status']  = True
            response['message'] = 'View file process was executed successfully'
        except ValueError as e:
            response['message'] = e
        return response   
    #Ask to user
    def ask_user(self,section_question_param,entity_param = None):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        try:
            section_question = section_question_param
            entity = entity_param
            if(section_question == 'ask_frontend'):
                valid_frontend = True
                while (valid_frontend):
                    input_frontend = input('Do you want include front end? responde Y/N (Yes/No): ').lower()
                    if(
                        input_frontend == 'y'
                        or input_frontend == 'yes'
                    ):
                        valid_frontend = False
                        self.__include_frontend = True
                        self.__manager_setting_file.create_login_module = True
                    elif (
                        input_frontend == 'n'
                        or input_frontend == 'no'
                    ):
                        self.__include_frontend = False
                        valid_frontend = False
                    else:
                        print('Introduce a valid value please')
            elif(section_question == 'serialization'):
                list_fields = self.get_all_fields_entity(entity)['data']
                message_to_user = f'See all fields related to the entity {entity} below'
                print(message_to_user)
                for index, field in enumerate(list_fields):
                    print(str(index + 1) + ". " + field)            
                print("Please select which will be enable fields for API")
                fields_choose_input = input("Write the number or numbers separated with comma. ej: 1,3,..n: or let empty for all: ").split(",")
                print("Please select which will be fields only read")
                only_read_fields_choose_input = input("Write the number or numbers separated with comma. ej: 1,3,..n; or let empty for anything: ").split(",")
                fields_choose = []
                fields_choose_only_read = []
                
                if (fields_choose_input[0] == ''):
                    fields_choose = list_fields
                else:
                    for field_choose in fields_choose_input:
                        fields_choose.append(list_fields[(int(field_choose) - 1)])
                if(only_read_fields_choose_input[0] == ""):
                    only_read_fields_choose_input = []
                else:
                    for field_choose_only_read in only_read_fields_choose_input:
                        fields_choose_only_read.append(list_fields[(int(field_choose_only_read) - 1)])
                    
                response['data']  = [fields_choose,fields_choose_only_read]
                response['message'] = 'input obtained successfully'
            elif(section_question == 'login'):
                scaffolding_config_file = self.__manager_setting_file.get_scaffolding_config_file()
                if (
                    scaffolding_config_file['status'] == False or
                    (scaffolding_config_file['status'] and 'login_user' not in scaffolding_config_file['data'])
                ):     
                    valid_login = True
                    login_module_name = ""
                    while (valid_login):
                        input_login = input('Do you want login module? responde Y/N (Yes/No): ').lower()
                        if(
                            input_login == 'y'
                            or input_login == 'yes'
                        ):
                            
                            login_module_name = input("what name do you want call the login module?")
                            if(login_module_name == "" or login_module_name.isnumeric()):
                                print("Name can not by empty neither be numeric value")
                                continue
                            valid_login = False
                            self.__include_login_module = True
                            
                        elif (
                            input_login == 'n'
                            or input_login == 'no'
                        ):
                            self.__include_login_module = False
                            valid_login = False
                        else:
                            print('Introduce a valid value please')
                     
                    response['data'] = login_module_name
                else:
                    response['data'] = scaffolding_config_file['data']['login_user']['module_name']
                                  
            response['status']  = True
        except ValueError as e:
            response['message'] = e
        except Exception as e:
            response['message'] = e
        return response
            
            
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

            module_model_class = importlib.import_module(module_name)
            # obtain all fields from model
            class_fields = getattr(module_model_class,class_name)._meta.get_fields()
            fields = []
            for field in class_fields:
                fields.append(field.name);
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
                        lines[index] = line.rstrip()[:-1] + f"    '{appname}',\n]\n"
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
    
    def config_main_url(self, entity_param):
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        try:
            entity = entity_param
            appname = entity + self.__sufix_app
            if not entity:
                output_message = "Entity can not be empty for intall app process"
                raise ValueError(output_message)
            
             # path to settings.py file
            urls_file = f'./{self.__project_name}/urls.py'

            # we read the file
            with open(urls_file, 'r') as f:
                lines = f.readlines()
            flag_import = 0
            for index,line in enumerate(lines):
                if line.startswith('from django.urls import path') and index > 1 and flag_import == 0:
                    lines[index] = line[: -1] + ", include\n"
                    flag_import +=1
                    
                if line.startswith("urlpatterns = ["):
                   lines[index] = line[: -1] + f"\n    path('', include('{appname}.urls')),\n"
            with open(urls_file,'w+') as file:
                file.writelines(lines)
            response['status']  = True
            response['message'] = 'Proccess were executed successfully'
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
            #ask to user if want frontend
            self.ask_user('ask_frontend')
            output_message = ''
            if self.__initialize == False:
                output_message = "Module not initialized successfully"
                raise ValueError(output_message)
            
            dbtables = self.get_tables_from_cursor(self.__cursor)
            self.__alldbtables = dbtables['data']
            targetdb = self.__targetdb
            #ask to user if want login
            login_module = self.ask_user('login')
            if (self.__include_login_module):
                login_module_name = login_module['data'] #module name assigned by the user
                create_login_result = self.create_app(login_module_name)
                if(create_login_result['status'] == False):
                    message_error = "Login module has not been created successfully. Please contact support"
                    raise ValueError(message_error)
                mlogin = loginView.ManagerLogin()
                mlogin.login_name = login_module_name
                cla = mlogin.create_login_app()
                if(not cla['status']):
                    message_error = "The login module has not been built successfully. Please contact support."
                    raise ValueError(message_error)
                self.__manager_setting_file.login_module =  login_module_name
                
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
                
                is_create_app = self.create_app(entity + self.__sufix_app)
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
                #installing app
                is_installed_app = self.install_app(entity)
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
                is_serialize_implement = self.create_serialization(entity)
                fields = is_serialize_implement['data'][0]
                feature_fields={}
                #If frontend is true then ask the user about required
                if(self.__include_frontend):
                    for field in fields:
                        verify_input = True
                        while(verify_input):
                            is_required = input(f"Is it {field} an input required? answer y/n yes/no: ")
                            if(is_required == 'y' or is_required == 'yes'):
                                feature_fields[field] = {
                                    'required': True
                                }
                                verify_input = False
                            elif(is_required == 'n' or is_required == 'no'):
                                feature_fields[field] = {
                                    'required': False
                                }
                                verify_input = False
                            if(verify_input):
                                print('Introduce a valid value. y/n')
                            
                if (not is_serialize_implement['status']):
                    output_message  = f"{entity} serialization process has not been finished. Please reset the process"
                    raise ValueError(output_message)
                is_viewset_implement = self.create_viewset_file(entity)
                if (not is_viewset_implement['status']):
                    output_message  = f"{entity} viewSet process has not been finished. Please reset the process"
                    raise ValueError(output_message)
                is_urls_register = self.create_url_file(entity)
                if (not is_urls_register['status']):
                    output_message  = f"{entity} Urls process has not been finished. Please reset the process"
                    raise ValueError(output_message)
                is_main_urls_register = self.config_main_url(entity)
                if (not is_main_urls_register['status']):
                    output_message  = f"{entity} Main urls process has not been installed successfully. Please reset the process"
                    raise ValueError(output_message)
                self.__manager_setting_file.apps = {
                    'app': entity + self.__sufix_app,
                    'fields': feature_fields,
                    'fields_only_read': is_serialize_implement['data'][1],
                    'auth':False
                }
                self.__manager_setting_file.create_scaffolding_config_file()
            output_message = "API created successfully"
            response['status'] = True    
            response['message'] = output_message    
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
           
            config_file = self.__manager_setting_file.get_scaffolding_config_file()
            if(config_file['status']):
                config_file = config_file['data']
                # Import the function to delete folders 
                import shutil
                
                #restore urls.py in main project
                msf = self.__manager_setting_file
                msf.project_name = self.main_project_name
                
                #restore the urls.py file
                restore_file = msf.restore_file('url')
                if(restore_file['status']):
                    print("urls.py was restored")
                else:
                    raise ValueError(msf['message'])
                #restore the settings in main project
            
                restore_file = msf.restore_file('setting')
                if(restore_file['status']):
                    print("settings.py was restored")
                else:
                    raise ValueError(msf['message'])
                if(config_file['login_user']):
                    login_app = config_file['login_user']['module_name']
                    if(login_app == ''):
                        print("login module is empty, does not delete")
                    else:
                        shutil.rmtree("./"+login_app, ignore_errors=True)
                        output_message = f'{login_app} deleted successfully'
                        print(output_message)                    
                for entity in config_file['create_app']:
                    app_name = entity['app']
                    if(app_name == ''):
                        print(app_name,"can not be deleted")
                    else:
                        shutil.rmtree("./"+app_name, ignore_errors=True)
                        output_message = f'{app_name} deleted successfully'
                        print(output_message)
                output_message = "Process reverse successfully"
                response['status'] = True    
                response['message'] = output_message    
            else:
                output_message = "Nothing for restaure" 
                response['message'] = output_message   
                response['status'] = True  
                print(output_message)  
        except ValueError as e:
            response['message'] = e    
if __name__ == "__main__":
    print("Sorry this is not main package")