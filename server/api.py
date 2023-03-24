#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import random

session_path = __file__[0:len(__file__)-6].replace('\\','/')

sys.path.append(f'{session_path}auth')
sys.path.append(f'{session_path}data')

import authenticator as auth

auth.session_path = session_path

# Lire un fichier json
def read_json(token, path):
    if not auth.check_token(token): # Vérification du token avant de continuer
        return "Invalid token"
    # Si le token entré est valide, on lit le fichier
    workspace_id = auth.token_info(token)['workspace_id']
    with open(f'{session_path}data/workspace/'+workspace_id+'/'+path,'r',encoding="utf-8") as f:
        return json.loads(f.read())

# Écrire dans un fichier json
def write_json(token, path, data):
    if not auth.check_token(token): # Vérification du token avant de continuer
        return "Invalid token"
    # Si le token entré est valide, on écrit dans le fichier
    workspace_id = auth.token_info(token)['workspace_id']
    with open(f'{session_path}data/workspace/'+workspace_id+'/'+path,'w',encoding="utf-8") as f:
        json.dump(data,f,indent=4)

def create_workspace(ws_name, user_name, password):

    # génération d'un id pour le workspace	
    ws_id = random.randint(100000,999999)
    while ws_id not in os.listdir(f'{session_path}data/workspace'):
        ws_id = random.randint(100000,999999)
        print(ws_id) 

    # Création du dossier du workspace
    os.mkdir(f'{session_path}data/workspace/{ws_id}')

    # Création du fichier de configuration du workspace
    with open(f'{session_path}data/workspace/{ws_name}/config.json','w',encoding="utf-8") as f: 
        json.dump({"ws_name": ws_name},f,indent=4)
    # Création du fichier de configuration des utilisateurs
    with open(f'{session_path}data/workspace/{ws_name}/users.json','w',encoding="utf-8") as f:
        json.dump({},f,indent=4)
    # Création du fichier de configuration des tokens
    with open(f'{session_path}data/workspace/{ws_name}/token.lock','w',encoding="utf-8") as f:
        json.dump({},f,indent=4)
    # Création du fichier de configuration des mots de passe
    with open(f'{session_path}data/workspace/{ws_name}/password.lock','w',encoding="utf-8") as f:
        json.dump({},f,indent=4)
    # Création du fichier de configuration des données
    with open(f'{session_path}data/workspace/{ws_name}/data.json','w',encoding="utf-8") as f:
        json.dump({},f,indent=4)


#create_workspace("test", "test", "test")