#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')

import view.display as display
import controller.ctrl as ctrl

class Console:
    def __init__(self):
        self.menus = {
            "START MENU": {
                "title": "Start menu",
                "corps": [
                    {
                        "title": "Welcome to the DevExpert user management software",
                        "text": "",
                        "option": [
                            {
                                "name": "Dev menu",
                                "key": "1",
                                "action": lambda: self.set_menu("DEV MENU"),
                                "set_menu": ["DEV MENU",""]
                            },
                            {
                                "name": "Show hello",
                                "key": "2",
                                "action": lambda: self.say("Hello!"),
                                "set_menu": ["START MENU","Hello!"]
                            },
                            {
                                "name": "Quit",
                                "key": "q",
                                "action": "",
                                "set_menu": ["EXIT"]
                            }
                        ]
                    }
                ]
            },
            "DEV MENU": {
                "title": "Dev menu",
                "corps": [
                    {
                        "title": "Dev options",
                        "text": "",
                        "option": [
                            {
                                "name": "Show all users",
                                "key": "1",
                                "action": "",
                                "set_menu": ["DEV MENU","Not finished :("]
                            },
                            {
                                "name": "Back to start Menu",
                                "key": "q",
                                "action": "",
                                "set_menu": ["START MENU"]
                            }
                        ]
                    }
                ]
            }
        }

    def say(self, msg="Hello!"):
        print(msg)

    def set_menu(self, menu, msg=""):

        display.show_menu(self.menus[menu], msg)

        if menu == "DEV MENU":
            pass
        elif menu == "START MENU":
            pass
        
        self.interpret_choice(menu,msg,display.wait_input("Please enter the number of your choice:\n"))

    def interpret_choice(self, menu, msg="",user_choice=""):
        for option_field in self.menus[menu]['corps']:
            for option in option_field['option']:
                if user_choice == option['key']:
                    option['action']
                    if option['set_menu'] == []:
                        self.set_menu(menu,msg)
                        return
                    elif option['set_menu'][0] == "EXIT":
                        display.clear()
                        if len(option['set_menu']) == 2:
                            print(option['set_menu'][1])
                        return
                    else:
                        if len(option['set_menu']) == 2:
                            self.set_menu(option['set_menu'][0],option['set_menu'][1])
                            return
                        else:
                            self.set_menu(option['set_menu'][0])
                            return
        self.set_menu(menu,"Invalid choice, please try again.")


console = Console()
console.set_menu("START MENU")