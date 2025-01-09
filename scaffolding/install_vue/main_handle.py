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
            
            shutil.rmtree(destinity_path)
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
                    
                    composable_path = destinity_path + '/composables/'
                    service_path = destinity_path + '/services/'
                    store_path = destinity_path + '/stores/'
                    views_path = destinity_path + '/views/'
                    route_path = destinity_path + '/'
                    route_file = 'routes.js'
                    
                    #rename the composable file to login module name
                    os.rename(composable_path + 'useLogin.js',composable_path + '/use' + login_app +'.js')
                    #replace the content of composable file with keywords to make the module works
                    self.__replace_content(login_app, composable_path + '/use' + login_app +'.js')
                    
                    #rename the service file to login module name
                    os.rename(service_path + 'LoginService.js',service_path + login_app +'Service.js')
                    #replace the content of service file with keywords to make the module works
                    self.__replace_content(login_app, service_path + login_app +'Service.js')
                    
                    #rename the store file to login module name
                    os.rename(store_path + 'useLoginUserStore.js',store_path + '/use' + login_app +'Store.js')
                    #replace the content of store file with keywords to make the module works
                    self.__replace_content(login_app, store_path + '/use' + login_app +'Store.js')
                    
                    #rename the view file to login module name
                    os.rename(views_path + 'LoginUser.vue',views_path + login_app +'.vue')
                    #replace the content of view file with keywords to make the module works
                    self.__replace_content(login_app, views_path + login_app +'.vue')
                    #replace the content of router file with keywords to make the the module works
                    self.__replace_content(login_app, views_path + 'SigninUser.vue')
                    self.__replace_content(login_app, views_path + 'PasswordRecovery.vue')
                    
                    #replace the content of router file with keywords to make the the module works
                    self.__replace_content(login_app, route_path + route_file)
                    
                    self.setting_app_file(login_app)
                    self.setting_main_file()    
                    self.setting_routes_file(login_app)    
                    
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
            response['message'] = 'Proccess finished successfully'
        except ValueError as ev:
            response['message'] = ev.__str__()
        except FileExistsError as fe:
            response['message'] = 'The destinity folder already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e.__str__()
        return response
    
    def __install_vue(self)->dict:
        """Install Vue and library necesary to work

        Returns:
            dict: response with error status, data and message
        """
        
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        project_vue_name = self.__project_name  + self.__sufix_project_name
        import subprocess
        process = ''
        try:
            import os
            destinity_path = self.__root_destinity_path + project_vue_name
            
            message = "Vue 3 has been installed successfully"
            if not os.path.exists(destinity_path):
                commands_install = ["npx","create-vite@latest",destinity_path,"--template","vue"]
                process = subprocess.run(commands_install,cwd=os.getcwd(),capture_output=True,check=True, text=True,shell=True)
                print(process.stdout)

                project_path = os.path.join(os.getcwd(), destinity_path)
                commands_install = ["npm", "install", "axios", "vue-router"]
                print('Axios and Vue-router are being installed')
                process = subprocess.run(commands_install,cwd=project_path,capture_output=True, check=True ,text=True,shell=True)
                print(process.stdout)
                
                commands_install = ["npm", "install", "pinia"]
                print('Pinia are being installed')
                process = subprocess.run(commands_install,cwd=project_path,capture_output=True, check=True ,text=True, shell=True)
                print(process.stdout)
                         
                #install tailwindcss
                tailwind_iantallation = self.install_tailwindcss()
                if tailwind_iantallation['error']:
                    raise ValueError("Tailwindcss have errors: " + tailwind_iantallation['message'])
                
                config_vite = project_path + '/vite.config.js'
                vite_config_file = open(config_vite,'r')
                content_vite_config = vite_config_file.read()
                content_vite_config = content_vite_config.replace(
                    "import vue from '@vitejs/plugin-vue'",
                    "import vue from '@vitejs/plugin-vue'\nimport path from 'path'"
                )
                content_vite_config = content_vite_config.replace(
                    'plugins: [vue()],',
                    'plugins: [vue()],\n   resolve:{\n       alias:{\n           "@": path.resolve(__dirname,"./src")\n        }\n   }'
                )
                vite_config_file.close()
                
                vite_config_file = open(config_vite,'w+')
                vite_config_file.write(content_vite_config)
                vite_config_file.close()
                
                self.setting_style_css()
                
            else:
                message = f'Project {project_vue_name} already exists, nothing to do'
            response['error']  = False
            response['message'] = message
        except subprocess.CalledProcessError as cpe:
            response['message'] = cpe.stderr
        except ValueError as ve:
            response['message'] = ve.__str__()
        except Exception as ex:
            response['message'] = ex.__str__()
            
        return response
    
    def install_tailwindcss(self)->dict:
        """Install twailwindscss in Vue 

        Returns:
            dict: response with error status, data and message
        """
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        project_vue_name = self.__project_name  + self.__sufix_project_name
        import subprocess
        process = ''
        try:
            from time import sleep
            import os
            
            destinity_path = self.__root_destinity_path + project_vue_name
            tailwindcss_path = destinity_path + '/tailwind.config.js'
            
            message = "tailwindcss has been installed successfully"
            if os.path.exists(destinity_path):
                project_path = os.path.join(os.getcwd(), destinity_path)
                commands_install = ["npm","install","-D","tailwindcss","postcss","autoprefixer"]
                print("Tailwindcss is being installed")
                process = subprocess.run(commands_install,cwd=project_path,capture_output=True,check=True, text=True,shell=True)
                print(process.stdout)

                commands_install = ["npx", "tailwindcss", "init", "-p"]
                print('The tailwind.config.js and postcss.config.js are being generated')
                process = subprocess.run(commands_install,cwd=project_path,capture_output=True, check=True ,text=True,shell=True)
                print(process.stdout)
                
                tailwindcss_config = open(tailwindcss_path,mode='r+')
                content_tailwindcss = tailwindcss_config.read() #"".join( )
                tailwindcss_config.close()
                content_tailwindcss = content_tailwindcss.replace(
                    "content: [],",
                    "content: [\n    \"./index.html\",\n    \"./src/**/*.{vue,js,ts,jsx,tsx}\"\n  ],"
                )
                sleep(5)
                
                tailwindcss_config = open(tailwindcss_path,mode='w+')
                tailwindcss_config.write(content_tailwindcss)
                tailwindcss_config.close()
                
                index_css_file = open(destinity_path + './src/index.css',mode='w' )
                index_css_file.write(
                    "@tailwind base;\n@tailwind components;\n@tailwind utilities;"
                )
            else:
                message = f'Project {project_vue_name} already exists, nothing to do'
            response['error']  = False
            response['message'] = message
        except ValueError as e:
            response['message'] = e.__str__()
        return response
    
    def setting_app_file(self,main_module_name):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        try:
            project_vue_name = self.__project_name  + self.__sufix_project_name
            destinity_path = self.__root_destinity_path + project_vue_name + "/src/App.vue"
            
            content_app_file = """
<script setup>
  import """+main_module_name+""" from '@/module/"""+main_module_name+"""/views/"""+main_module_name+""".vue'
  import { useOverlay } from '@/stores/useOverlay';
  const overlay = useOverlay()
</script>

<template>
  <div class="relative h-dvh w-dvw">
    <router-view></router-view>
    <div class="
      fixed inset-0
      bg-black
      bg-opacity-70
      z-50
      flex items-center justify-center
      "
      v-show="overlay.watchShowOverlay"
    >
      <div class="spinner "></div>
    </div>
  </div>
</template>

<style scoped>
</style>
            """
            app_file = open(destinity_path,mode="w+")
            app_file.write(content_app_file)
            app_file.close()
            
            response['error']  = False
            response['message'] = 'Proccess were executed successfully'
        except ValueError as e:
            response['message'] = e.__str__()
        return response
    
    def setting_main_file(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        try:
            project_vue_name = self.__project_name  + self.__sufix_project_name
            destinity_path = self.__root_destinity_path + project_vue_name + "/src/main.js"
            
            content_main_file = """
import { createApp } from 'vue'
import './style.css'
import { createPinia } from 'pinia';
import App from './App.vue'
import './index.css'
import router from './router'

const pinia = createPinia();
createApp(App).use(pinia).use(router).mount('#app')
            """
            main_file = open(destinity_path,mode="w+")
            main_file.write(content_main_file)
            main_file.close()
            response['error']  = False
            response['message'] = 'Proccess were executed successfully'
        except ValueError as e:
            response['message'] = e.__str__()
        return response
    
    def setting_routes_file(self,module_name):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        try:
            project_vue_name = self.__project_name  + self.__sufix_project_name
            destinity_path = self.__root_destinity_path + project_vue_name + "/src/router.js"
            
            content_main_file = """
import {createRouter, createWebHistory } from 'vue-router'
import routes%module_name% from '@/module/%module_name%/routes'
import PageNotFound from '@/views/PageNotFound.vue'
import {use%module_name%Store} from '@/module/%module_name%/stores/use%module_name%Store'

const routes = [
    ...routes%module_name%,
    {
        path: '/:catchAll(.*)',
        component: PageNotFound, 
        name: 'page_not_found'
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach( (to, from, next) => {
    const store = use%module_name%Store()
    const {loadUser} = store
    loadUser()
    const {isAuthenticated} = store
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
    if( requiresAuth && !isAuthenticated){
        next('/page_not_found')
    }else{
        next()
    }
})

export default router
            """
            content_main_file = content_main_file.replace('%module_name%',module_name)
            main_file = open(destinity_path,mode="w+")
            main_file.write(content_main_file)
            main_file.close()
            response['error']  = False
            response['message'] = 'Proccess were executed successfully'
        except ValueError as e:
            response['message'] = e.__str__()
        return response
    
    def setting_style_css(self):
        response = {
            'error' : True,
            'message' : '',
            'data' : []
        }
        path_css_file = self.__template_path + '/style.css'
        destinity_path = self.__root_destinity_path + self.__project_name  + self.__sufix_project_name + '/src/style.css'
        try:
            print("coping style.css")
            #get the style.css contnt
            style_css_file = open(path_css_file,mode='r')
            content_file = style_css_file.read()
            style_css_file.close()
            
            print("pasting style.css")
            #put the style.css content
            style_css_file = open(destinity_path,mode='w+')
            style_css_file.write(content_file)           
            style_css_file.close()
                        
            response['error']  = False
            response['message'] = 'The style.css has been copied successfully'
        except FileExistsError as fe:
            response['message'] = 'The destinity file already exists '+ fe.strerror
        except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
        except Exception as e:
            response['message'] = e
        return response