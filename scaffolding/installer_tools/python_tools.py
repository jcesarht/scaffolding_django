class PythonInstallersTools:
    def __init__(self) -> None:
        self.__project_name = None
        self.__libraries_needs = [
            'rest_framework',
            'rest_framework.authtoken',
            'corsheaders',
        ]
        self.__library_missing=[]
        
    @property
    def project_name(self):
        return self.__project_name
        
    #Settel project name
    @project_name.setter
    def project_name(self,project_name_param):
        self.__project_name = project_name_param
    
    def verify_tools(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : ''
        }
        
        setting_file_path = f'./{self.__project_name}/settings.py'
        try:
            import re
            
            if self.__project_name == None or self.__project_name == '':
                raise ValueError("project_name is empty, please provide the project name")
            setting_file = open(setting_file_path,mode = 'r')
            content_settings_file = "".join(setting_file.readlines())
            regular_expression_search = r"INSTALLED_APPS = \[.*?\]" #this is regular expression for extract all characters of intalled_app
            app_installed = re.search(regular_expression_search,content_settings_file,re.DOTALL).group()
            for library in self.__libraries_needs:
                regular_expression_search = rf"{library},?"
                tool_found = re.search(regular_expression_search,app_installed)
                if(not tool_found):
                    answer_valid = False
                    install_tool_answer = 'no'
                    while(not answer_valid):
                        install_tool_answer = input(f"{library} need to be installed, do you want to install it? (yes/no): ").lower()
                        if (
                            install_tool_answer == 'y' or
                            install_tool_answer == 'yes' or
                            install_tool_answer == 'no' or
                            install_tool_answer == 'n'
                        ):
                            answer_valid = True
                        else:
                            print("Please write a valid answer")
                    if(install_tool_answer == 'yes' or install_tool_answer == 'y'):
                        tool_installed = self.__install_tool(library)
                        if tool_installed['error']:
                            print(f"{library} could not be installed\n",tool_installed['message'])
                        else:
                            print(f"{library} has been installed successfully")
                        
            setting_file.close()
        except FileNotFoundError as fnf:
            response['message'] = fnf
        except ValueError as ve:
            response['message'] = ve
            
        return response
    
    def __install_tool(self, tool_param: str):
        from utils.settings_helper import register_app, register_app_in_line
        """Install a library or module or app in app_intaller array in the settings.py file

        Args:
            tool_param (str): is the library, module or app name
        """
        try:
            response = {
                'error' : True,
                'message' : '',
            }
            tool = tool_param
            if self.__project_name == None or self.__project_name == '':
                raise ValueError("project_name is empty, please provide the project name")
            
            import subprocess
            if (tool == 'corsheaders'):
                print(f"starting {tool} installation")
                process = subprocess.run(["pip","install","django-cors-headers"],capture_output=True, text=True)
                register_app_result = register_app('INSTALLED_APPS',tool,self.__project_name)
                if (register_app_result['error']):
                    raise ValueError ("An error occurred while trying to register module")
                line = '''
# CORS Allowed: ALL
CORS_ALLOW_ALL_ORIGINS = True

#CORS Customized
CORS_ALLOWED_ORIGINS = [
    "https://tu_dominio.com",
    "https://otro_dominio.com",
]
                '''
                register_app_result = register_app_in_line(line,self.__project_name)
            elif (tool == 'rest_framework'):
                print(f"starting {tool} installation")
                process = subprocess.run(["pip","install","djangorestframework"],capture_output=True, text=True)
                register_app_result = register_app('INSTALLED_APPS',tool,self.__project_name)
                if (register_app_result['error']):
                    raise ValueError ("An error occurred while trying to register module")
            elif (tool == 'rest_framework.authtoken'):
                print(f"starting {tool} installation")
                process = subprocess.run(["pip","install","djangorestframework-authtoken"],capture_output=True, text=True)
                register_app_result = register_app('INSTALLED_APPS',tool,self.__project_name)
                if (register_app_result['error']):
                    raise ValueError ("An error occurred while trying to register module")
                register_app_result = register_app('MIDDLEWARE','django.middleware.security.SecurityMiddleware',self.__project_name)
                if register_app_result['error']:
                    raise ValueError ("An error occurred while trying to register Middleware django.middleware.security.SecurityMiddleware")
                register_app_result = register_app('MIDDLEWARE','corsheaders.middleware.CorsMiddleware',self.__project_name)
                if register_app_result['error']:
                    raise ValueError ("An error occurred while trying to register Middleware corsheaders.middleware.CorsMiddleware")
                
            else:
                raise ValueError(f"Library, module or app {tool} not found")
            response['message'] = process.stdout
            response['error'] = False                
        except subprocess.CalledProcessError as process_error:    
            response['message'] = process_error
        except ValueError as general_exception:
            response['message'] = general_exception
                    
        return response