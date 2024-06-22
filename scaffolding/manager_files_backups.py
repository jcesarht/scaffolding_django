import shutil
from os import path as sopath, mkdir
class ManagerSettingFile:
    def __init__(self):
        self.__project_name = ''
        self.__file_config_name = '__config.json'
        self.__backup_path = './scaffolding/backup_file/'
        self.__file_config_path = './scaffolding/config/'
        if( not sopath.exists(self.__backup_path)):
            mkdir(self.__backup_path)
        if( not sopath.exists(self.__file_config_path)):
            mkdir(self.__file_config_path)
        self.__apps = []
        self.__content_setup = {
            'copy_setting': False,
            'copy_urls': False,
            'create_app': self.__apps,
        }
    
    #get project name
    @property
    def project_name(self):
        return self.__project_name
    
    #set project name
    @project_name.setter
    def project_name(self,project_name_param):
        self.__project_name = project_name_param
    
    #return apps
    @property
    def apps(self):
        return self.__apps
    # add app
    @apps.setter
    def apps(self,add_param):
        self.__apps.append(add_param)
        self.__content_setup["create_app"] = self.__apps
        
    #Copy setting file from main project
    def copy_setting_file(self):
        response = {
            'status' : False,
            'message' : '',
        }
        try:
            destinity_file = f'./{self.__backup_path}/settings.py'
            if(sopath.isfile(destinity_file)):
                error_message = 'Already a copy settings.py file'
                response['status'] = True
                raise ValueError(error_message)
            
            path_setting = f'./{self.__project_name}/settings.py'
            shutil.copy(path_setting,destinity_file)
            # update the step or status copy setting for config file
            self.__content_setup['copy_setting'] = True
            response['status']  = True
            response['message'] = 'Proccess copy settings were created successfully'
        except ValueError as e:
            response['message'] = e
        return response
    #Copy url file from main project
    def copy_url_file(self):
        response = {
            'status' : False,
            'message' : '',
        }
        try:
            destinity_file = f'./{self.__backup_path}/urls.py'
            if(sopath.isfile(destinity_file)):
                error_message = 'Already a copy urls.py file'
                response['status'] = True
                raise ValueError(error_message)
            
            path_setting = f'./{self.__project_name}/urls.py'
            shutil.copy(path_setting,destinity_file)
            # update the step or status copy urls for config file
            self.__content_setup['copy_urls'] = True
            response['status']  = True
            response['message'] = 'Proccess copy urls were created successfully'
        except ValueError as e:
            response['message'] = e
        return response
    #Copy url file from main project
    def restore_file(self,setting_file_param):
        response = {
            'status' : False,
            'message' : '',
        }
        try:
            setting_file = ''
            if(setting_file_param == 'settings' or setting_file_param == 'setting'):
                setting_file = 'settings'
            elif(setting_file_param == 'urls' or setting_file_param == 'url'):
                setting_file = 'urls'
            else:
                raise ValueError("File did not restore")
            path_setting = f'./{self.__backup_path}/{setting_file}.py'
            destinity_file = f'./{self.__project_name}/{setting_file}.py'
            shutil.copy(path_setting,destinity_file)
            response['status']  = True
            response['message'] = f'File {setting_file_param} restored successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    #Check if settings.py file has been copied
    def check_setting_files_copied(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : False
        }
        try:
            destinity_file = f'./{self.__backup_path}/settings.py'
            if(sopath.isfile(destinity_file)):
                response['data'] = True
            response['status']  = True
            response['message'] = 'Vefify files is finished'
        except ValueError as e:
            response['message'] = e
        return response        
    
    #Create config file about user's choises 
    def create_config_file(self):
        import json
        check_setting_files_copied = False
        check_url_files_copied = False
        destinity_file = f'./{self.__backup_path}/settings.py'
        if(sopath.isfile(destinity_file)):
            check_setting_files_copied= True
        destinity_file = f'./{self.__backup_path}/urls.py'
        if(sopath.isfile(destinity_file)):
            check_url_files_copied= True
        self.__content_setup['copy_setting'] = check_setting_files_copied
        self.__content_setup['copy_urls'] = check_url_files_copied
        print('creating config file',self.__content_setup)
        path_config = self.__file_config_path + self.__file_config_name
        config_file = open(path_config,'+w')
        content = json.dumps(self.__content_setup)
        config_file.writelines(content)
        