#!/usr/bin/env python3
import shutil
from ..manager_files_backups import ManagerSettingFile
class ImplementVue:
    
    def __init__(self):
        self.__template_path:str = "./scaffolding/install_vue/template/"
        self.__project_name:str = ""
        self.__sufix_project_name:str = "_vue"
        self.__root_destinity_path:str = "../"
        self.__manager_setting_file = ManagerSettingFile()
    
    @property
    def project_name(self):
        return self.__project_name
    
    @project_name.setter
    def project_name(self,project_name_param):
        self.__project_name = project_name_param
    
    def install_vue(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        try:
            install_vue_result = self.__install_vue()
            if(install_vue_result['error']):
                raise ValueError("Error during Vue installation: " + install_vue_result['message'])
            print(install_vue_result['message'])
            
            install_components_response = self.install_components()
            if(install_components_response['error']):
                raise ValueError("Error during components installation: " + install_components_response['message'])
            print(install_components_response['message'])
            
            install_services_response = self.install_services()
            if(install_services_response['error']):
                raise ValueError("Error during services installation: " + install_services_response['message'])
            
            install_stores_response = self.install_stores()
            if(install_stores_response['error']):
                raise ValueError("Error during store installation: " + install_stores_response['message'])
            
            install_views_response = self.install_views()
            if(install_views_response['error']):
                raise ValueError("Error during views installation: " + install_views_response['message'])
            
            login_module_response = self.__install_login_module()
            if(login_module_response['error']):
                raise ValueError("Error during login module installation: " + login_module_response['message'])
            
            response['error']  = False
            response['message'] = 'Components has been installed successfully'
        except ValueError as e:
            response['message'] = e
        return response
    
    #install components in vue
    def install_components(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        path_components = self.__template_path + '/components/'
        destinity_path = self.__root_destinity_path + self.__project_name  + self.__sufix_project_name + '/src/components'
        try:
            
            shutil.copytree(path_components,destinity_path)
            
            response['error']  = False
            response['message'] = 'Proccess were executed successfully'
        except FileExistsError as fe:
            response['message'] = 'The destinity folder already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e
        return response
    
    #install services in vue
    def install_services(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        path_service = self.__template_path + '/services/'
        destinity_path = self.__root_destinity_path + self.__project_name  + self.__sufix_project_name + '/src/services'
        try:
            shutil.copytree(path_service,destinity_path)
            
            response['error']  = False
            response['message'] = 'Proccess services were executed successfully'
        except FileExistsError as fe:
            response['message'] = 'The destinity folder already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e
        return response
    
    #install store with PINIA in vue
    def install_stores(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        path_service = self.__template_path + '/stores/'
        destinity_path = self.__root_destinity_path + self.__project_name  + self.__sufix_project_name + '/src/stores'
        try:
            shutil.copytree(path_service,destinity_path)
            
            response['error']  = False
            response['message'] = 'Proccess stores were executed successfully'
        except FileExistsError as fe:
            response['message'] = 'The destinity folder already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e
        return response
    
    #install views with vue
    def install_views(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        path_service = self.__template_path + '/views/'
        destinity_path = self.__root_destinity_path + self.__project_name  + self.__sufix_project_name + '/src/views'
        try:
            shutil.copytree(path_service,destinity_path)
            
            response['error']  = False
            response['message'] = 'Proccess views were executed successfully'
        except FileExistsError as fe:
            response['message'] = 'The destinity folder already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e
        return response
    
    #install modules with vue
    def install_module(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        path_service = self.__template_path + '/views/'
        destinity_path = self.__root_destinity_path + self.__project_name  + self.__sufix_project_name + '/src/views'
        try:
            #shutil.copytree(path_service,destinity_path)
            
            response['error']  = False
            response['message'] = 'Proccess views were executed successfully'
        except FileExistsError as fe:
            response['message'] = 'The destinity folder already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e
        return response
    
    def __install_login_module(self)->dict:
        import os
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        
        origin_path = self.__template_path + '/module/Login'
        message:str = ''
        try:
            config_file = self.__manager_setting_file.get_scaffolding_config_file()
            if(config_file['status']):
                config_file = config_file['data']
                if "login_user" in config_file:
                    login_app:str = config_file['login_user']['module_name']
                    
                    if(login_app == ''):
                        raise ValueError("Login module have not name, check the config file.")
                    
                    destinity_path = self.__root_destinity_path + self.__project_name  + self.__sufix_project_name + '/src/module/' + login_app
                    shutil.copytree(origin_path,destinity_path)
                    #rename composable
                    composable_path = destinity_path + '/composables/'
                    service_path = destinity_path + '/services/'
                    store_path = destinity_path + '/stores/'
                    views_path = destinity_path + '/views/'
                    
                    os.rename(composable_path + 'useLogin.js',composable_path + '/use' + login_app +'.js')
                    self.__replace_content(login_app, composable_path + '/use' + login_app +'.js')
                    
                    os.rename(service_path + 'LoginService.js',service_path + login_app +'Service.js')
                    self.__replace_content(login_app, service_path + login_app +'Service.js')
                    
                    os.rename(store_path + 'useLoginUserStore.js',store_path + '/use' + login_app +'Store.js')
                    self.__replace_content(login_app, store_path + '/use' + login_app +'Store.js')
                    
                    os.rename(views_path + 'LoginUser.vue',views_path + login_app +'.vue')
                    self.__replace_content(login_app, views_path + login_app +'.vue')
                    
                    message = 'Module login has been installed'    
                else:
                    message = 'Module login is not installed'    
            response['error']  = False
            response['message'] = message
        except ValueError as ve:
            response['message'] = ve
        except Exception as ex:
            response['message'] = ex
        return response
    
    def __replace_content(self,word_to_sustitution:str,file_path_param:str):
        file_path = file_path_param
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        try:
            content_file = ''
            with open(file_path,'r') as file:
                content_file = file.read()
            
            new_text = content_file.replace('%module_name%',word_to_sustitution)
                        
            with open(file_path,'w') as file:
                file.write(new_text)
            
            response['error']  = False
            response['message'] = 'Proccess were executed successfully'
        except ValueError as ev:
            response['message'] = ev.__str__()
        except FileExistsError as fe:
            response['message'] = 'The destinity folder already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e.__str__()
        return response
    
    def __install_vue(self):
        
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        project_vue_name = self.__project_name  + self.__sufix_project_name
        try:
            import os
            import subprocess
            destinity_path = self.__root_destinity_path + project_vue_name
            message = "vue has been installed successfully"
            if not os.path.exists(destinity_path):
                commands_install = [
                    "npx"
                    ,"create-vite@latest"
                    ,project_vue_name
                    ,"--template vue"
                    ,f"&& cd {project_vue_name}"
                    ,"&& npm install axios vue-router"
                    ,"&& npm install pinia"
                ]
                process = subprocess.run(commands_install,cwd=os.getcwd(),capture_output=True, text=True)
                print(process.stdout)
            else:
                message = f'Project {project_vue_name} already exists, nothing to do'
            response['error']  = False
            response['message'] = message
        except ValueError as ve:
            response['message'] = ve.__str__()
        except Exception as ex:
            response['message'] = ex.__str__()
            
        return response