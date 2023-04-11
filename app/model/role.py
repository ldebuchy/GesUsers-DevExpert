#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
from random import randint

import pickle

sys.path.insert(1, f'{os.path.dirname(__file__)}/../../data')

# export des données dans le fichier roles.pickl
def export_roles(data):
    with open("data/roles.pickle", "wb") as file:
        pickle.dump(data, file)

# import des données depuis le fichier roles.pickle
def import_roles():
    with open("data/roles.pickle", "rb") as file:
        return pickle.load(file)

class Role():
    def __init__(self, name, priority, permissions=[]):
        # Trouve un id unique au role
        self.id = randint(100, 999)
        while self.id in import_roles():
            self.id = randint(100, 999)

        self.name = name  # Nom du role
        # Priorité (plus le nombre est petit plus le role à d'autorité.
        self.priority = priority

        ### Liste des permissions du role ###

        # permissions d'outrepasser toutes restrictions (à utiliser avec précaution)
        self.administrator = "administrator" in permissions

        # permission de crée, gérer et supprimer des roles
        self.manage_roles = "manage_roles" in permissions  # *

        # permissions de gérer les comptes
        self.creat_delete_user = "create_delete_user" in permissions
        self.edit_user_names = "edit_user_names" in permissions  # *
        self.reset_passwords = "reset_passwords" in permissions  # *
        self.edit_names = "edit_names" in permissions  # *
        self.suspended = "suspended" in permissions  # *

        # permissions pour gérer les documents
        self.creat_delete_documents = "create_delete_documents" in permissions
        self.read_documents = "read_documents" in permissions
        self.edit_documents = "edit_documents" in permissions

        # permissions de modifier son compte
        self.edit_account = "edit_account" in permissions

        '''
        précision sur les permissions:
        #* = Effectife uniquement si la priorité du role est structement supérieur au role ou role de l'utilisateur ciblé
        '''

admin = Role("admin", 0, ["administrator"])
hrm = Role("hrm", 20, ["manage_roles", "create_delete_user", "edit_user_names", "reset_passwords", "edit_names", "suspended", "create_delete_documents", "read_documents", "edit_documents", "edit_account"])
team_leader = Role("manager", 40, ["edit_user_names", "reset_passwords", "edit_names", "create_delete_documents", "read_documents", "edit_documents", "edit_account"])
employee = Role("employee", 80, ["create_delete_documents", "read_documents", "edit_documents", "edit_account"])
internship = Role("internship", 90, ["read_documents"])






def main():
    # Demander à l'administrateur l'action à effectuer
    action = input("Entrez l'action à effectuer (edit_user_name, edit_names, create_delete_user, reset_passwords, suspended) : ")
    
    if action == "edit_user_name":
        
        user_id = input("Entrez l'identifiant de l'utilisateur à modifier : ")

        
        new_username = input("Entrez le nouveau nom d'utilisateur : ")

        # Modifier le nom d'utilisateur de l'utilisateur
        os.system(f"usermod -l {new_username} {user_id}")

        print(f"Le nom d'utilisateur de l'utilisateur {user_id} a été modifié avec succès.")

    elif action == "edit_names":
    
        user_id = input("Entrez l'identifiant de l'utilisateur à modifier : ")

        
        new_full_name = input("Entrez le nouveau nom d'utilisateur : ")

        # Modifier le nom complet de l'utilisateur
        os.system(f"usermod -c '{new_full_name}' {user_id}")
        
        print(f"Le nom d'utilisateur {user_id} a été modifié avec succès.")

    elif action == "create_delete_user":
        # Demander l'action à effectuer (créer ou supprimer un utilisateur)
        user_action = input("Entrez l'action à effectuer (créer ou supprimer) : ")

        if user_action == "create":
            
            username = input("Entrez le nom d'utilisateur de l'utilisateur à créer : ")

            # Créer l'utilisateur
            os.system(f"useradd {username}")
            
            print(f"L'utilisateur {username} a été créé avec succès.")
        elif user_action == "delete":
            
            user_id = input("Entrez l'identifiant de l'utilisateur à supprimer : ")

            # Supprimer l'utilisateur
            os.system(f"userdel {user_id}")

            print(f"L'utilisateur {user_id} a été supprimé avec succès.")
        else:
            print("Action invalide.")

    elif action == "reset_passwords":
        
        user_id = input("Entrez l'identifiant de l'utilisateur à qui modifier le mot de passe : ")

        # Réinitialiser le mot de passe de l'utilisateur
        os.system(f"passwd -d {user_id}")
  
        print(f"Le mot de passe de l'utilisateur {user_id} a été réinitialisé avec succès.")

    elif action == "suspended":
        
    user_id = input("Entrez l'identifiant de l'utilisateur à suspendre ou réactiver : ")

    # Demander l'action à effectuer (suspendre ou réactiver)
    suspend_action = input("Entrez l'action à effectuer (suspendre ou réactiver) : ")

    if suspend_action == "suspendre":
        # Suspendre l'utilisateur
        os.system(f"usermod -L {user_id}")

        # Afficher un message de confirmation
        print(f"L'utilisateur {user_id} a été suspendu avec succès.")
    elif suspend_action == "réactiver":
        # Réactiver l'utilisateur
        os.system(f"usermod -U {user_id}")

        # Afficher un message de confirmation
        print(f"L'utilisateur {user_id} a été réactivé avec succès.")
    else:
        print("Action invalide.")

else:
    print("Action invalide.")

