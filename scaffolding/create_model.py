#!/usr/bin/env python3
from os import environ as __enviroment__, getcwd, path as __getpath__
from django.db import connection as __con__
from django import setup as __setup__
import subprocess
from sys import path 
except_message = ''

#init module
def init():
    return False

def creatingModel(target_param,appname_param):
    try:
        if(target_param ==''):
            raise ValueError("targetdb no puede estar vacio")
        if(appname_param ==''):
            raise ValueError("coloca el nombre de la app en el parámetro appname")
        
        __enviroment__.setdefault('DJANGO_SETTINGS_MODULE', appname_param + '.settings')
        #import settings conf 
        from django.conf import settings as __dgsettings__
        #get cursor where database is connected 
        cursor = __con__.cursor()
        #check database's ENGINE is connected. (mysql, postgrest or sqlite)
        if 'mysql' in __dgsettings__.DATABASES['default']['ENGINE']:
            cursor.execute("SHOW TABLES;");
        elif 'postgresql' in __dgsettings__.DATABASES['default']['ENGINE']:
            # comming soon
            raise ValueError("postgresql comming soon")
        elif 'sqlite3' in __dgsettings__.DATABASES['default']['ENGINE']:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        else:
            raise ValueError("Engine not supported")
        
        dbtables = cursor.fetchall();
        
        #subprocess.run(["cd.."],shell=True)
        #p = subprocess.run(["py","manage.py","inspectdb"],stdout=subprocess.PIPE);
        print(dbtables)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    print("Sorry this is not main package")
    exit()