#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from app.controller.exec import * # importe les fonctions de l'application

cli = Console() # instancie console
cli.set_menu(lambda: cli.start_menu()) # définit la console sur le menu de démarrage