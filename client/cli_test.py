#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import controller
import curses

def start_menu():
    print("1. Login")
    print("2. Quit")
    choice = input("Choice: ")
    if choice == "1":
        login_menu()
    elif choice == "2":
        quit()
    else:
        start_menu()

def login_menu():
    print("Login")
    workspace_name = input("Workspace name: ")
    user_name = input("User name: ")
    password = input("Password: ")
    controller.login(workspace_name, user_name, password)
    if controller.api.auth.check_token(controller.token):
        print("Logged in")
        main_menu()
    else:
        print("Login failed")
        if input("Retry? (y/n): ") == "y":
            login_menu()
        else:
            start_menu()

def main_menu():
    print("Main menu")
    print("1. nothing")
    print("2. logout")
    choice = input("Choice: ")
    if choice == "1":
        main_menu()
    elif choice == "2":
        controller.logout()
        print("Logged out")
        start_menu()
    else:
        main_menu()

start_menu()