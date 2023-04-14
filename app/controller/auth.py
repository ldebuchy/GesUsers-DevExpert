#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import hashlib
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')
from model.user import *

session = None

def login(user_name, password):
    global session
    users = import_users()
    for user in users:
        if users[user].user_name == user_name:
            if users[user].password == hash_password(password) and not users[user].suspended:
                session = users[user].id
                users[user].login_attempts = 0
                export_users(users)
                return [True, True, users[user].id]
            else:
                users[user].login_attempts += 1  
                if users[user].login_attempts >= 3 and users[user].id != super_admin_id:  
                    users[user].suspended = True  
                export_users(users)
                return [True, False, users[user].id]
            
    return [False, False, None]

def logout():
    global session
    session = None