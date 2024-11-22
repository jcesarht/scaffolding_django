#!/usr/bin/env python3
from django.core.management.base import BaseCommand, CommandParser
from sys import path
path.append('.\\scaffolding')
from scaffolding.handle_scaffold import InspectDB
from scaffolding.installer_tools.python_tools import PythonInstallersTools
class Command(BaseCommand):
    help = "Crea un API a partir de una base de datos"
    help = "Create an API from a database|"

    #prepare the argument of command scf
    def add_arguments(self, parser):
        target_text_help = '''Indica sobre que tabla debe actual, tambien puedes colocar (all) o (.) para aplicarlo a todas las tablas\n
                        puedes escribir varias tablas separadas por coma "," sin espacios.'''
        target_text_help = '''Specify which table to update. You can also use (all) or (.) to apply it to all tables.\n
                            You can write more that one table separated with comma "," without spaces'''
        appname_text_help = 'Coloca el nombre de la app o modulo principal del proyecto'
        appname_text_help = 'Enter the name of the main app or main module name of the project'
        restore_text_help = 'Restaura el proyecto a su estado original'
        restore_text_help = 'Restore it project to begin status'
        parser.add_argument('--targetdb', nargs='?', type=str,help=target_text_help)
        parser.add_argument('projectname', nargs=1, type=str,help=appname_text_help)
        parser.add_argument('--restore', nargs='?', type=str,const='',help=restore_text_help)
    
    #excecute the command's action 
    def handle(self, *args, **options):
        idb = InspectDB()
        try:
            self.stdout.write(self.style.HTTP_INFO('scaffold is initializing...'))
            output_message = ''
            projectname = options['projectname'][0].strip()
            if(projectname == ''):
                output_message = 'projectname no puede estar vacio'
                output_message = 'projectname can not be empty'
                raise ValueError(output_message)
            idb.main_project_name = projectname
            if(not options['restore']):
                # installpython libraries
                pit = PythonInstallersTools()
                pit.project_name = projectname
                check_tools = pit.verify_tools()
                if check_tools['error']:
                    print(check_tools['message'])
                    exit() 
                    # end to install
                target = options['targetdb'].strip()
                if(target == ''):
                    output_message = 'targetdb no puede estar vacio'
                    output_message = 'targetdb can not be empty'
                    raise ValueError(output_message)
                # create models with params obtained
                idb.database_target = target
                idb.initilize()
                is_successfully_process = idb.main_handle()
                if(not is_successfully_process['status']):
                    raise ValueError(is_successfully_process['message'])
                    
                output_message = 'Proceso finalizado con éxito'
                output_message = 'proccess finished succesfully'
                self.stdout.write(self.style.SUCCESS(output_message))
            else:
                idb.reverse_process()
        except ValueError as e:
            idb.reverse_process()
            self.stdout.write(self.style.ERROR(e))