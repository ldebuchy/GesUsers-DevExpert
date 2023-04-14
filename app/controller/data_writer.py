#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')
import controller.auth as auth
import model.user as user_data
import model.role as role_data
import controller.data_reader as data_reader


def create_user(first_name, last_name, password):
    users = user_data.import_users()
    new_user = user_data.User(first_name, last_name, password)
    users.update({new_user.id: new_user})
    user_data.export_users(users)

def delete_user(user_id):
    users = user_data.import_users()
    try:
        del users[user_id]
    except:
        pass
    user_data.export_users(users)

def reactivate_user(user_id):
    users = user_data.import_users()
    try:
        users[user_id].suspended = False
        users[user_id].login_attempts = 0
    except:
        pass
    user_data.export_users(users)

def suspend_user(user_id):
    users = user_data.import_users()
    try:
        users[user_id].suspended = True
    except:
        pass
    user_data.export_users(users)



def add_role(user_id, role):
    users = user_data.import_users()
    users[user_id].roles.append(role)
    user_data.export_users(users)

def remove_role(user_id, role):
    users = user_data.import_users()
    users[user_id].roles.remove(role)
    user_data.export_users(users)