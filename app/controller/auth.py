#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import hashlib
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')
from model.user import *

session = None

super_admin_id = "id"

def login(user_name, password):
    global session
    users = import_users()
    for user in users:
        if users[user].user_name == user_name:
            if users[user].password == hash_password(password):
                session = users[user].id
                return [True, True]
            else:
                users[user].login_attempts += 1  
                if users[user].login_attempts >= 3:  
                    users[user].suspended = True  
                export_users(users)
                return [True, False]
    return [False, False]

def logout():
    global session
    session = None