#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app') # ajoute le chemin vers le dossier app
from model.user import * # importe les fonctions de gestion de'utilisateur de l'application
from view.console import * # importe les fonctions d'affichage de l'application