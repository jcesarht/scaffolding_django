#!/usr/bin/env python3
import shutil
from ..utils.settings_helper import copy_and_paste
from ..manager_files_backups import ManagerSettingFile
class SetterVue:
    
    def __init__(self):
        self.__template_path:str = "./scaffolding/install_vue/template/"
        self.__project_name:str = ""
        self.__sufix_project_name:str = "_vue"
        self.__root_destination_path:str = "../"
        self.__manager_setting_file = ManagerSettingFile()
    
    @property
    def project_name(self):
        return self.__project_name
    
    @project_name.setter
    def project_name(self,project_name_param):
        self.__project_name = project_name_param
    
    def dashboard_setting(self):
        pass