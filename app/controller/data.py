#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')
import model.user as u # importe les fonctions de gestion de l'utilisateur

# Fonction qui retourne un dictionnaire contenant les informations d'un utilisateur
def get_user(id):
    return convert_user_to_dict(u.import_users()[id])

# Fonction qui retourne un dictionnaire contenant tous les utilisateurs et leurs informations
def get_user_list():
    users = u.import_users()
    user_list = {}

    for user in users:
        user_list.update({users[user].id: convert_user_to_dict(users[user])})
        
    return user_list

# Fonction qui convertie un objet User en dictionnaire
def convert_user_to_dict(user):
    return {
        "id": user.id,
        "user_name": user.user_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "suspended": user.suspended,
        "login_attempts": user.login_attempts,
        "role": user.role
    }

# Fonction qui retourne un dictionnaire contenant les informations d'un utilisateur recherché
def search_user(search):
    users=u.import_users()
    user_list = {}
    for user in users:
        if users[user].first_name in search or users[user].last_name in search or users[user].user_name in search or str(users[user].id) in search:
            user_list.update({users[user].id: convert_user_to_dict(users[user])})    
    return user_list