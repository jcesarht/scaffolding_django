import json
import re
from pathlib import Path

def register_app(setting_list:str,app_name:str, project_name_param:str):
    
    response = {
        'error' : True,
        'message' : '',
        'data' : []
    }
    try:
        def get_libraries_registered_in_app(project_name_param:str)->dict:
            response = {
                'error' : True,
                'message' : '',
                'data' : []
            }
            try:
                
                setting_file_path = f'./{project_name_param}/settings.py'
                setting_file = open(setting_file_path,mode = 'r')
                content_settings_file = "".join(setting_file.readlines())
                regular_expression_search = rf"{setting_list} = \[.*?\]" #this is regular expression for extract all characters of intalled_app
                installed_app = re.search(regular_expression_search,content_settings_file,re.DOTALL).group()    
                if (installed_app):
                        regular_expression_search = r"\[.*?\]" #this is regular expression for extract all characters of intalled_app
                        app_list = re.search(regular_expression_search,installed_app,re.DOTALL).group()
                        app_list = app_list.replace("'",'"').replace(" ","").replace("\n","")
                        app_list = app_list.rstrip(',]') + "]"
                        app_list = json.loads(app_list)
                        if (not app_list):
                            raise ValueError("settings.py file is bad formated")
                response['error']  = False
                response['message'] = 'Proccess were executed successfully'
                response['data'] = app_list
            except ValueError as ve:
                response['message'] = ve
            except Exception as e:
                response['message'] = e
            return response

        def add_library_in_app(libraries_app_param:list,project_name_param:str):
            response = {
                'error' : True,
                'message' : '',
                'data' : []
            }
            try:
                register_app = libraries_app_param
        
                setting_file_path = f'./{project_name_param}/settings.py'
                setting_file = open(setting_file_path,'r')
                content_settings_file = "".join(setting_file.readlines())
                regular_expression_search = rf"{setting_list} = \[(.*?)\]" #this is regular expression for extract all characters of intalled_app
                app_installer_list_updated_regular_expression = (
                    f"{setting_list} = [\n    " + ",\n    ".join(f"'{app}'" for app in register_app) + "\n]"
                )
                app_installer_list_updated = re.sub(regular_expression_search, app_installer_list_updated_regular_expression, content_settings_file,flags=re.DOTALL)
                if(app_installer_list_updated and app_installer_list_updated.strip() != ""):
                    setting_file = open(setting_file_path,'w')
                    setting_file.writelines(app_installer_list_updated)
                else:
                    setting_file.close()
                    raise ValueError("Something was wrong with settings.py file while editing it")
                response['error']  = False
                response['message'] = "Proccess was registered successfully"
            except ValueError as ve:
                response['message'] = ve
            except Exception as e:
                response['message'] = e
            return response
        installed_app = get_libraries_registered_in_app(project_name_param)
        if installed_app['error']:
            raise ValueError("Something was wrong with apps list.")
        
        if app_name not in installed_app['data']:
            installed_app['data'].append(app_name)
            registered_app = add_library_in_app(installed_app['data'], project_name_param)
        
            if(registered_app['error']):
                raise ValueError(registered_app['message'])
        
        response['error']  = False
        response['message'] = 'Proccess were executed successfully'
    except ValueError as e:
        response['message'] = e
    return response

def register_app_in_line(setting_line_param:str, project_name_param:str):
    response = {
        'error' : True,
        'message' : '',
        'data' : []
    }
    try:

        setting_file_path = f'./{project_name_param}/settings.py'
        setting_file = open(setting_file_path,'r+')
        content_settings_file = "".join(setting_file.readlines())
        match_line = re.search( setting_line_param, content_settings_file)
        if(match_line):
            response['message'] = f'The configuration {setting_line_param} in settings exists already'
        else:
            setting_file.writelines(setting_line_param)
            response['message'] = f'The configuration {setting_line_param} in settings was added'
        response['error']  = False
    except ValueError as e:
        response['message'] = e
    return response

def copy_and_paste(source_file_path:str,destination_file_path:str,overwrite=False)->dict:
    """ Copy and paste a directory or file without overwriting it

    Args:
        source_file_path (str): Origin path of file or directory
        destination_file_path (str): Destination path of file or directory

    Raises:
        ValueError: Is launch if the source file or folder already exist

    Returns:
        dict: error and message is returned
    """
    import shutil
    import os
    response = {
        'error' : True,
        'message' : '',
    }
    try:
        type_resourse = 'file'
        
        if os.path.exists(destination_file_path) and not overwrite:
            if os.path.isdir(destination_file_path):
                type_resourse = 'directory'
            raise ValueError(f"The {type_resourse} already exist. Cannot be copied")
        
        if type_resourse == 'file':
            shutil.copyfile(source_file_path,destination_file_path)
        else:
            shutil.copytree(source_file_path,destination_file_path) 
        
        response['error']  = False
        response['message'] = f'{source_file_path} has been copied successfully'
    except FileExistsError as fe:
            response['message'] = f'The destination {type_resourse} already exists '+ fe.strerror
    except FileNotFoundError as fnf:
            response['message'] = 'Error in path '+ fnf.strerror
    except ValueError as ve:
        response['message'] = ve.__str__()
    except Exception as e:
        response['message'] = e.__str__()
    
    return response

def modify_js_object_attribute(content_param:str, path_keys: list,new_value_param:str):
    """Modifies the value of an attribute in a JS file within a nested object.

    Args:
        path_keys (list): List of keys forming the path to the attribute.
        content_param (str): JS object casted in string
        new_value_param (_type_): _New value for the attribute (can be an object or array).

    Returns:
        dict: response of process
    """
    
    response = {
        'error' : True,
        'message' : '',
        'data' : []
    }
    
    try:
        #Convertir el string a un diccionario
        js_object = json.loads(js_object_str.replace("'", '"'))  # Convertir comillas simples en dobles para JSON
        #Navegar por la jerarquía de atributos
        current_level = js_object
        for attribute in attribute_list[:-1]:
            #Si el atributo no existe, lo creamos como un diccionario
            if attribute not in current_level:
                current_level[attribute] = {}
            current_level = current_level[attribute]
            #Asignar el valor al último atributo de la lista
        current_level[attribute_list[-1]] = value
        #Convertir de nuevo el diccionario a un string de objeto JavaScript
        return json.dumps(js_object, indent=4).replace('"', "'")
        
        response['data'] = modified_js_object_str
        response['error'] = True
        response['message'] = f"The JS object has been successfully modified."
    except ValueError as ve:
        response['message'] = str(ve)
    return response

def add_import_line_in_js(file_content:str,import_line:str,mode='FULL_CONTENT')->dict:
    """
    Add an import line to a JavaScript file.

    Args:
        file_content (str): The content of the JavaScript file.
        import_line (str): The new import line to be added.
        mode (str, optional): Determines where to insert the import line. Defaults to 'FULL_CONTENT'.
            - "FULL_CONTENT": Adds the import line to the entire content.
            - "JUST_IMPORTS": Adds the import line only within the import section.

    Returns:
        dict: A response containing the error state, message, and result data.
"""
    response = {
        'error' : True,
        'message' : '',
        'data' : []
    }
    try:
        import_line = import_line.replace("\n", "")
        if (mode == 'FULL_CONTENT'):
            if import_line not in file_content:
                file_content = import_line + "\n" + file_content
            response['data'] = file_content
        elif (mode == 'IMPORT_MODE'):
            import_section = re.search(r'import.*\n', file_content, re.DOTALL).group()
            if import_line not in import_section:
                import_section = import_section + import_line + "\n"
                file_content = file_content.replace(re.search(r'import.*\n', file_content, re.DOTALL).group(), import_section)
        response['error'] = False
        response['data'] = file_content
        response['message'] = f"The import line {import_line} has been added successfully."
    except ValueError as ve:
        response['message'] = str(ve)
    return response
    