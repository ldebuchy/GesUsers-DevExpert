#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys





class User():
    def init(self, user_name, first_name, last_name, password, role=[]):
        self.id = 0
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.suspended = False
        self.role = []
    # create a user 


user_list={}
    # create a user 
def create_user(user_id,user_name,first_name,last_name,password):
        user_list.update({f"{user_id}":User(user_name,first_name,last_name,password)})

def delete_user(user_id):
    user_list.pop(f"{user_id}")



user_list = []

jhon = User("jdoe", "Jhon", "Doe", "123456")

user_list.append(jhon)

