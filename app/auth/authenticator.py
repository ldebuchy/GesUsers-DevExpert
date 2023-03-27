#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import bcrypt    
import time

session_path = ""

def get_token(workspace_name, user_name, password, permanent=False):
    check_expired_tokens() # Nettoyage des tokens expirés par précaution

    # Récupération de l'ID du workspace
    workspace_id = ""
    # On ouvre le fichier workspace.json
    with open(f'{session_path}data/workspace/workspace.json','r',encoding="utf-8") as f:
        workspace_file = json.loads(f.read())
    # Parcourt du fichier workspace.json pour trouver l'ID correspondant au nom du workspace
    for id in workspace_file:
        if workspace_file[id]['workspace_name'] == workspace_name:
            workspace_id = str(id)
            break

    # Vérification de l'existence du workspace 
    if not workspace_id in workspace_file: 
        return "Auth System message: Workspace not found"

    # Récupération de l'ID de l'utilisateur à partir de son nom d'utilisateur
    user_id = ""
    # on ouvre le fichier user.json du workspace concerné
    with open(f'{session_path}data/workspace/'+workspace_id+'/user.json','r',encoding="utf-8") as f:
        user_file = json.loads(f.read())
    # On parcourt le fichier user.json pour trouver l'ID correspondant au nom d'utilisateur
    for id in user_file: 
        if user_file[id]['user_name'] == user_name:
            user_id = str(id)
            break
    
    # Vérification de l'existence de l'ID de l'utilisateur
    if not user_id in user_file:
        return "Auth System message: User not found"
    
    # On vérifie si l'utilisateur n'est pas suspendu
    if user_file[user_id]['suspended']:
        return "Auth System message: User suspended"

    # Vérification du mot de passe
    with open(f'{session_path}auth/password.lock','r',encoding="utf-8") as f: # on ouvre le fichier password.json
        password_file = json.loads(f.read())
    # On vérifie que le mot de passe correspond à celui enregistré dans le fichier password.json
    if not bcrypt.checkpw(bytes(password, 'utf-8'), bytes(password_file[workspace_id][user_id], 'utf-8')):
        return "Auth System message: Wrong password"

    # Les informations entrées sont valides, on vérifie si le token existe déjà:
    with open(f'{session_path}auth/token.lock','r',encoding="utf-8") as f:
        token_file = json.loads(f.read())
    for token in token_file:
        if token_file[token]['workspace_id'] == workspace_id and token_file[token]['user_id'] == user_id and token_file[token]['password'] == password:
            return token

    # Si le token n'existe pas, on le crée:

    # Création du token (à partir de l'ID du workspace, de l'ID de l'utilisateur et du mot de passe)
    new_token = bcrypt.hashpw(bytes(workspace_id + user_id + password, 'utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Attribution d'une date de création et d'expiration au token
    creation_date = str(time.time())
    if permanent:
        expiration_date = str(time.time() + (30*86400)) # 30 jours de validité
    else:
        expiration_date = str(time.time() + 600) # Une heure de validité

    # Ajout du token au fichier
    with open(f'{session_path}auth/token.lock','r',encoding="utf-8") as f: # on ouvre le fichier token.json
        token_file = json.loads(f.read())

    token_file[new_token] = {"workspace_id": workspace_id, "user_id": user_id, "password": password, "creation date":creation_date, "expiration_date": expiration_date} # on ajoute le token au fichier

    with open(f'{session_path}auth/token.lock','w',encoding="utf-8") as f: # on écrit dans le fichier token.json
        json.dump(token_file,f,indent=4)  

    return new_token

# Fonction qui supprime un token
def delete_token(token):
    try:
        check_expired_tokens() # Nettoyage des tokens expirés par précaution
        # on ouvre le fichier token.json
        with open(f'{session_path}auth/token.lock','r',encoding="utf-8") as f: 
            token_file = json.loads(f.read())
        # on supprime le token du fichier
        del token_file[token] 
        # on enregistre le fichier
        with open(f'{session_path}auth/token.lock','w',encoding="utf-8") as f: 
            json.dump(token_file,f,indent=4)
    except:
        pass

# Fonction qui vérifie si des tokens actif sont expirés et les supprime si c'est le cas
def check_expired_tokens():
    # Fonction récursive qui supprime les tokens expirés et relance la fonction si un token a été supprimé (pour éviter les erreurs)
    def check():
        for token in token_file: # On parcourt le fichier token.json
            if str(time.time()) > token_file[token]['expiration_date']: # Si la date actuelle est supérieure à la date d'expiration du token alors on supprime ce token
                del token_file[token]
                check()
                break
            
    with open(f'{session_path}auth/token.lock','r',encoding="utf-8") as f:
        token_file = json.loads(f.read())
    check()
    with open(f'{session_path}auth/token.lock','w',encoding="utf-8") as f:
        json.dump(token_file,f,indent=4)

# Fonction qui renvoie les informations d'un token
def token_info(token):
    check_expired_tokens() # Nettoyage des tokens expirés par précaution
    with open(f'{session_path}auth/token.lock','r',encoding="utf-8") as f:
        token_file = json.loads(f.read())
    
    if token in token_file:
        return token_file[token]

# Fonction qui vérifie si un token est valide
def check_token(token):
    check_expired_tokens() # Nettoyage des tokens expirés par précaution
    with open(f'{session_path}auth/token.lock','r',encoding="utf-8") as f:
        token_file = json.loads(f.read())
    
    if token in token_file:
        return True
    else:
        return False