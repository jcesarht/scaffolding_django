import shutil
from os import path as sopath, mkdir
class ManagerSettingFile:
    def __init__(self):
        self.__project_name = ''
        self.__backup_path = './scaffolding/backup_file'
        if( not sopath.exists(self.__backup_path)):
            mkdir(self.__backup_path)
    
    #get project name
    @property
    def project_name(self):
        return self.__project_name
    
    #set project name
    @project_name.setter
    def project_name(self,project_name_param):
        self.__project_name = project_name_param
    
    
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
            response['status']  = True
            response['message'] = 'Proccess copy urls were created successfully'
        except ValueError as e:
            response['message'] = e
        return response