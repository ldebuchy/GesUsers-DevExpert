#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')
from model.user import *


session = None

super_admin_id = "id"

def login(user_name, password):
    users = import_users()
    for user in users:
        if user.user_name == user_name:
            if user.password == password:
                session = user.id
                return user
        return [True, False]
    return [False, False]