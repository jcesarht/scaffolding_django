class PythonInstallersTools:
    def __init__(self) -> None:
        self.__project_name = None
        self.__libraries_needs = [
            'rest_framework',
            'rest_framework.authtoken',
            'corsheaders',
        ]
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
            setting_file = open(setting_file_path,mode = 'r')
            content_settings_file = setting_file.readlines()
            
            setting_file.close()
        except FileNotFoundError as fnf:
            response['message'] = fnf
        return response