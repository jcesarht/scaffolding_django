from django.core.management.base import BaseCommand, CommandParser
from sys import path
path.append('.\\scaffolding')
from scaffolding import create_model
class Command(BaseCommand):
    help = "Crea un API a partir de una base de datos"
    help = "Create an API from a database|"

    def add_arguments(self, parser):
        target_text_help = 'Indica sobre que tabla debe actual, tambien puedes colocar (all) o (.) para aplicarlo a todas las tablas'
        target_text_help = 'Specify which table to update. You can also use (all) or (.) to apply it to all tables.'
        appname_text_help = 'Coloca el nombre de la app o modulo principal del proyecto'
        appname_text_help = 'Enter the name of the main app or module of the project'
        parser.add_argument('targetdb', nargs=1, type=str,help=target_text_help)
        parser.add_argument('appname', nargs=1, type=str,help=appname_text_help)
    
    def handle(self, *args, **options):
        try:
            target = options['targetdb'][0].strip()
            appname = options['appname'][0].strip()
            error_message = ''
            if(target == ''):
                error_message = 'targetdb no puede estar vacio'
                error_message = 'targetdb can not be empty'
                raise ValueError(error_message)
            if(appname == ''):
                error_message = 'appname no puede estar vacio'
                error_message = 'appname can not be empty'
                raise ValueError(error_message)
            
            create_model.creatingModel(target,appname)
            self.stdout.write(self.style.SUCCESS('Comando ejecutado con éxito'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(e))