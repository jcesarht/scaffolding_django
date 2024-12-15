import shutil
from os import path as sopath, mkdir
class ManagerSettingFile:
    def __init__(self):
        self.__project_name = ''
        self.__login_module = ''
        self.__create_login_module = False
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
    def project_name(self)-> str:
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
        
    #get login module
    @property
    def login_module(self)-> str:
        return self.__login_module
    
    #set login module
    @login_module.setter
    def login_module(self,login_module_param):
        self.__login_module = login_module_param
    
    #get create login module
    @property
    def create_login_module(self)-> bool:
        return self.__create_login_module
    
    #set create login module
    @create_login_module.setter
    def create_login_module(self,create_login_module_param: bool):
        """
            Set if the login module must be created or not
        Args:
            bool (create_login_module): true if have create, else for not create
        """
        self.__create_login_module = create_login_module_param
    
    #Copy setting file from main project
    def copy_setting_file(self):
        response = {
            'status' : False,
            'message' : '',
            'data' : ''
        }
        try:
            destinity_file = f'./{self.__backup_path}/settings.py'
            if(sopath.isfile(destinity_file)):
                error_message = 'Already a copy settings.py file'
                response['status'] = True
                response['data'] = 'exist'
                raise ValueError(error_message)
            
            path_setting = f'./{self.__project_name}/settings.py'
            shutil.copy(path_setting,destinity_file)
            # update the step or status copy setting for config file
            self.__content_setup['copy_setting'] = True
            response['data'] = 'created'
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
            'data': ''
        }
        try:
            destinity_file = f'./{self.__backup_path}/urls.py'
            if(sopath.isfile(destinity_file)):
                error_message = 'Already a copy urls.py file'
                response['status'] = True
                response['data'] = 'exist'
                raise ValueError(error_message)
            
            path_setting = f'./{self.__project_name}/urls.py'
            shutil.copy(path_setting,destinity_file)
            # update the step or status copy urls for config file
            self.__content_setup['copy_urls'] = True
            response['status']  = True
            response['message'] = 'Proccess copy urls were created successfully'
            response['data'] = 'created'
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
    
    def check_setting_files_copied(self) -> dict:
        """Check if settings.py file has been copied

        Returns:
            dict: response with status, message of process and data like a Bool
        """
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
            response['message'] = 'Verify files is finished'
        except ValueError as e:
            response['message'] = e
        return response        
    
    def create_scaffolding_config_file(self):
        """
        create config file about the scaffolding tool set up by user
        """
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
        if(self.__create_login_module):
            self.__content_setup['login_user'] = {"module_name": self.__login_module}
        path_config = self.__file_config_path + self.__file_config_name
        config_file = open(path_config,'+w')
        content = json.dumps(self.__content_setup)
        config_file.writelines(content)
        
        print(f'config file was created in {path_config}')
    
    #Obtaine config file
    def get_scaffolding_config_file(self) -> dict:
        """Obtaine config file about apps created \" __config.json\" and it features, also login module 

        Returns:
            dict: return scaffolding config file's content in json format 
        """
        import json
        from os import strerror
        response = {
            "status": False,
            "message": "",
            "data": []
        }
        message = ""
        try:
            contain = ''
            path_config = self.__file_config_path + self.__file_config_name
            file = open(path_config,'+r')
            for line in file.readlines():
                contain +=  line
            message = "__config.json file copied successfully"
            response['data'] = json.loads(contain)
            response['status'] = True
            response['message'] = message
        except IOError as ioe:
            message =  "Something was wrong with file. Error IO can not open file " + ioe
            response['message'] = message
        except Exception as e:
            message =  "Something was wrong with file. Error "+strerror(e.errno)+" check the process "
            response['message'] = message
            
        return response
    
    def delete_scaffolding_config_file(self):
        """reset the scaffolding config file

        Returns:
            dict: respose about proccess
        """
        response = {
            'status' : False,
            'message' : '',
            'data' : []
        }
        path_config = self.__file_config_path + self.__file_config_name
        try:
            config_file = open(path_config,'+w')
            config_file.writelines(['{}'])
            shutil.rmtree(self.__file_config_path, ignore_errors=True)
            output_message = f'{self.__file_config_name} reset successfully'
            response['status']  = True
            response['message'] = output_message
        except ValueError:
            error_message =  f"Something was wrong with file. Error IO can not be deleted {self.__file_config_name} file "
            response['message'] = error_message
        return response