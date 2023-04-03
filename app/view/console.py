#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')

import view.display as display
import controller.data_reader as data

class Console:

    def __init__(self):
        self.menu_path = ['STOP_SIGNAL']



    ### Affichage des menus ###

    # Entrer dans un menu
    def set_menu(self, menu, msg=''):
        if menu == 'STOP_SIGNAL':
            os.system('cls')
            print('Thank you and enjoy your coffee!')
            return

        if not self.menu_path[-1] == menu:
            self.menu_path.append(menu)
        menu_data = self.menu_path[-1]()
        display.show_menu(menu_data, msg)

        input_type = 'choice'

        valid_input = [field['option'][option]['key'] for field in menu_data['fields'] for option in range(len(field['option']))]
        
        for key in valid_input:
            if len(key) > 1:
                input_type = 'text'
                break

        submitted_input = self.request_input(type=input_type, msg='Please enter a key to navigate:')
        if input_type is "choice" and not submitted_input.lower() in valid_input:
            self.set_message(f'{display.md.RED}Invalid choice, please try again.')
            return

        self.interpret_choice(menu_data, submitted_input)

    # Retourner au menu précédent
    def previous_menu(self):
        if len(self.menu_path) > 1:
            self.menu_path.pop()
            self.set_menu(self.menu_path[-1])
        else:
            self.set_menu(self.menu_path[-1])

    # Afficher un message sur le menu
    def set_message(self, msg='Empty message'):
        self.set_menu(self.menu_path[-1], msg)

    # Demander à l'utilisateur de saisir une entrée
    def request_input(self, type='text', msg=''):
        if type == 'choice':
            return display.choice_input(msg)
        elif type == 'secret':
            return display.secret_input(msg)
        else:
            return display.text_input(msg)

    # Interpréter la réponse de l'utilisateur 
    def interpret_choice(self, menu, submitted_input):
        for field in menu['fields']:
            for option in field['option']:
                if option['key'].lower() == submitted_input.lower():
                    option['action']()
                    return True
        return False


    ### Manipulation des menus ###

    # Fonctions pour créer des options dans un menu
    def add_option(self, menu, field_index, name='', key='', action=[]):
        menu['fields'][field_index]['option'].append({
            'name': str(name),
            'key': str(key),
            'action': action,
        })
        return menu
    
    # Fonctions pour supprimer des options dans un menu
    def remove_option(self, menu, field_index, option_index):
        menu['fields'][field_index]['option'].pop(option_index)
        return menu

    # Fonctions pour créer des champs dans un menu
    def add_field(self, menu, title='', text=''):
        if menu == {}:
            menu = {
                'title': 'DevExpert administration console',
                'fields': []
            }
        menu['fields'].append({
            'title': title,
            'text': text,
            'option': []
        })
        return menu
    
    # Fonctions pour supprimer des champs dans un menu
    def remove_field(self, menu, field_index):
        menu['fields'].pop(field_index)
        return menu



    ### Données des menus ###

    # Menu de démarrage
    def start_menu(self, menu={}):
        menu = self.add_field(menu, title='Welcome', text='')
        menu = self.add_option(menu, 0, name='Dev menu', key='1', action=lambda:self.set_menu(lambda:self.dev_menu()))
        menu = self.add_option(menu, 0, name='Show hello', key='2', action=lambda:self.set_message('Hello!'))
        
        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Quit', key='q', action=lambda:self.previous_menu())
        return menu

    # Menu devloppeur
    def dev_menu(self, menu={}):
        menu = self.add_field(menu, title='Dev menu', text='')
        menu = self.add_option(menu, 0, name='Show all users', key='1', action=lambda:self.set_menu(lambda:self.user_list_menu()))

        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Back', key='b', action=lambda:self.previous_menu())
        return menu

    # Menu de liste d'utilisateurs
    def user_list_menu(self, menu={}, users = {}):
        users = data.get_user_list()

        if users != {}:
            menu = self.add_field(menu, title='User list', text='')
            key_index = 1
            for user_id, user_data in users.items():
                menu = self.add_option(menu, 0, name=user_data['first_name'] + ' ' + user_data['last_name'], key=str(key_index), action=lambda user_id=user_id: self.set_menu(lambda: self.user_menu(user_id)))
                key_index += 1
        else:
            menu = self.add_field(menu, title='User list', text='No user found.')

        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Back', key='b', action=lambda:self.previous_menu())
        return menu

    # Menu d'utilisateur
    def user_menu(self, user_id, menu={}):
        user = data.get_user(user_id)
        menu = self.add_field(menu, title=user['first_name']+' '+user['last_name'], text="ID: "+str(user['id']))

        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Back', key='b', action=lambda:self.previous_menu())
        return menu

    # Menu de confirmation
    def confirmation_menu(self, menu={}, title='',field_title='',field_text='',yes_action=['y','yes',[]],no_action=['n','no',[]]):
        if no_action[2] == []:
            no_action[2] = lambda: self.previous_menu()
        if yes_action[2] == []:
            yes_action[2] = lambda: [self.previous_menu(),self.set_message(f'{display.md.YELLOW}No action has been associated with the selected answer.')]
        menu = self.add_field(menu, title=field_title, text=field_text)
        menu = self.add_option(menu, 0, name=yes_action[1], key=yes_action[0], action=yes_action[2])
        menu = self.add_option(menu, 0, name=no_action[1], key=no_action[0], action=no_action[2])
        return menu