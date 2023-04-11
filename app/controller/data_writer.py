#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')
import controller.auth as auth
import model.user as user_data
import model.role as role_data
import controller.data_reader as data_reader

def add_role(user_id, role):
    user = user_data.import_users()[user_id]
    user.roles.append(role)
    user_data.export_users(user_data.import_users())