#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys





class User():
    def init(self, user_name, first_name, last_name, password, role=[]):
        self.id = 0
        self.user_name = user_name
        self.first_name = ""
        self.last_name = ""
        self.password = password
        self.suspended = False
        self.role = []




user_list = []

jhon = User("jdoe", "Jhon", "Doe", "123456")

user_list.append(jhon)

