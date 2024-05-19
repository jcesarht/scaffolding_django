#!/usr/bin/env python3
import argparse
import subprocess

from sys import path
path.append(".\\scaffolding")
from scaffolding import create_model


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Crea un API a partir de una base de datos")
        parser.add_argument("scf", nargs=1,help="usa scf para inicializar el proceso de scaffolding.")
        parser.add_argument("--target",required=True, help="Indica sobre que tabla debe actual, tambien puedes colocar (all) o (.) para aplicarlo a todas las tablas")
        parser.add_argument("--appname",required=True, help="Nombre de la app o modulo principal del proyecto")
        
        args = parser.parse_args()
        target = args.target.strip()
        appname = args.appname.strip()
        create_model.creatingModel(target,appname)
    except argparse.ArgumentError:
        print("An Error has been accurred")