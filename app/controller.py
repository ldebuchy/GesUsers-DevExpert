#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
sys.path.append('server')
import api

token = ""

def login(workspace_name, user_name, password, permanent=False):
    global token
    if not api.auth.check_token(token):
        token = api.auth.get_token(workspace_name, user_name, password, permanent)

def logout():
    global token
    api.auth.delete_token(token)
    token = ""