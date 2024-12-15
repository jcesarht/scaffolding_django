#!/usr/bin/env python3
from django.core.management.base import BaseCommand, CommandParser
from sys import path
path.append('.\\scaffolding')
from scaffolding.install_vue.main_handle import ImplementVue
class Command(BaseCommand):
    help = "Crea el front-end en Vue desde un la API en DJANGO"
    help = "Create the front-end in Vue from DJANGO'S API"

    #prepare the argument of command scf
    def add_arguments(self, parser):
        target_text_help = '''Indica sobre que tabla debe actual, tambien puedes colocar (all) o (.) para aplicarlo a todas las tablas\n
                        puedes escribir varias tablas separadas por coma "," sin espacios.'''
        target_text_help = '''Specify which table to update. You can also use (all) or (.) to apply it to all tables.\n
                            You can write more that one table separated with comma "," without spaces'''
        project_name_text_help = 'Coloca el nombre de la app o nombre principal del proyecto'
        project_name_text_help = 'Enter the name of the main app or main name of the project'
        restore_text_help = 'Restaura el proyecto a su estado original'
        restore_text_help = 'Restore it project to begin status'
        parser.add_argument('projectname', nargs=1, type=str,help=project_name_text_help)
        parser.add_argument('--restore', nargs='?', type=str,const='',help=restore_text_help)
    
    #excecute the command's action 
    def handle(self, *args, **options):
        iv = ImplementVue()
        try:
            self.stdout.write(self.style.HTTP_INFO('scaffold is initializing...'))
            output_message = ''
            projectname = options['projectname'][0].strip()
            if(projectname == ''):
                output_message = 'projectname no puede estar vacio'
                output_message = 'projectname can not be empty'
                raise ValueError(output_message)
            iv.project_name = projectname
            if(not options['restore']):
                install_vue_response = iv.install_vue()
                if(install_vue_response['error']):
                    self.stdout.write(self.style.ERROR(install_vue_response['message']))
                output_message = 'Proceso finalizado con éxito'
                output_message = 'proccess finished succesfully'
                self.stdout.write(self.style.SUCCESS(output_message))
            else:
                iv.reverse_process()
        except ValueError as e:
            iv.reverse_process()
            self.stdout.write(self.style.ERROR(e))