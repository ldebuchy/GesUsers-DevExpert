#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys





class User():
    def __init__(self, user_name, first_name, last_name, password, role=[]):
        self.id = 0
        self.__user_name = user_name
        self.__first_name = first_name
        self.__last_name = last_name
        self.__password = password
        self.__suspended = False
        self.__role = []

    def get(self, var):
        if var =="user_name":
            return self.__user_name
        elif var =="first_name":
            return self.__first_name
        elif var =="last_name":
            return self.__last_name
        elif var =="suspended":
            return self.__suspended
        elif var =="role":
            return self.__role
        else: print("quelle info voulez-vous ?")


jhon = User("jdoe", "Jhon", "Doe", "123456")

print(jhon.get("user_name"))
