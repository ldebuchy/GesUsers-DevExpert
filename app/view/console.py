#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys

sys.path.insert(1, f'{os.path.dirname(__file__)}/../../app')

import view.display as display
import controller.data as data
from controller.auth import *
import controller.auth as auth

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

        input_type = menu_data['input']['input_type']

        valid_input = [field['option'][option]['key'] for field in menu_data['fields'] for option in range(len(field['option']))]
        
        for key in valid_input:
            if len(key) > 1:
                input_type = 'text'
                break

        submitted_input = self.request_input(type=input_type, msg=menu_data['input']['input_text'])
        if input_type == "choice" and not submitted_input.lower() in valid_input:
            self.set_message(f'{display.md.YELLOW}Invalid choice, please try again.')
            return
        
        if input_type == "choice":
            self.interpret_choice(menu_data, submitted_input)
            return

        # Actions personnalisées pour les menus
        if menu_data['fields'][0]['title'] == 'Create user':
            if menu_data['input']['input_request'] == 'firstname':
                self.set_menu(lambda:self.create_user_menu(firstname=submitted_input,input_request='lastname'))
                return
            elif menu_data['input']['input_request'] == 'lastname':
                self.set_menu(lambda:self.create_user_menu(firstname=menu_data['input']['firstname'],lastname=submitted_input,input_request='password'))
                return
            elif menu_data['input']['input_request'] == 'password':
                new_user = data.u.User()
                new_user.first_name = menu_data['input']['firstname']
                new_user.last_name = menu_data['input']['lastname']
                new_user.set_password(submitted_input)
                new_user.generate_id()
                new_user.generate_username()
                new_user.save()
                self.set_menu(lambda:self.user_list_menu,msg=f'{display.md.GREEN} User created successfully! {display.md.RESET} Username: {new_user.user_name} Password: {submitted_input}')
                return

        if menu_data['fields'][0]['title'] == 'Welcome':
            if menu_data['input']['input_request'] == 'username':
                self.set_menu(lambda:self.start_menu(username=submitted_input,input_request='password'))
                return
            elif menu_data['input']['input_request'] == 'password':
                login_okay = auth.login(menu_data['input']['username'],submitted_input)
                if login_okay[0] and login_okay[1]:
                    self.set_menu(lambda:self.dashboard_menu(),msg=f'{display.md.GREEN}Login successful!')
                    return
                elif login_okay[0] and not login_okay[1]:
                    if data.get_user(login_okay[2])['suspended']:
                        self.set_menu(lambda:self.start_menu(), msg=f'{display.md.RED}User suspended, please contact an administrator.')
                        return
                    else:
                        self.set_menu(lambda:self.start_menu(), msg=f'{display.md.RED}Incorrect password, please try again.')
                        return
                elif login_okay[0] == False:
                    self.set_menu(lambda:self.start_menu(), msg=f'{display.md.RED}User not found, please try again.')
                    return
                else:
                    self.set_menu(lambda:self.start_menu(), msg=f'{display.md.RED}Unknown error, please try again.')
                return

            else:
                self.set_message(f'{display.md.YELLO}Invalid choice, please try again.')
                return
                

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
        if menu == None:
            menu = {}
        if 'title' not in menu:
            menu['title'] = 'DevExpert administration console'
        if 'fields' not in menu:
            menu['fields'] = []
        if 'input' not in menu:
            menu['input'] = {
                'input_text': 'Please enter a key to navigate:',
                'input_type': 'choice',
                'input_request': 'option'
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
    def start_menu(self, menu=None, username='', password='', input_request=''):
        menu = self.add_field(menu, title='Welcome', text='')
        menu = self.add_option(menu, 0, name='Login', key='1', action=lambda:self.set_menu(lambda:self.start_menu(username=username,password=password,input_request='username')))

        
        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Quit', key='q', action=lambda:self.set_menu('STOP_SIGNAL'))

        menu['input']['username'] = username

        if input_request == 'username':
            menu['input']['input_text'] = 'Username:\n'
            menu['input']['input_type'] = 'text'
            menu['input']['input_request'] = 'username'
        elif input_request == 'password':
            menu['input']['input_text'] = 'Password:\n'
            menu['input']['input_type'] = 'secret'
            menu['input']['input_request'] = 'password'
        return menu

    def dashboard_menu(self, menu=None):
        menu = self.add_field(menu, title='Dashboard', text='Welcome in the dashboard '+ data.get_user(auth.session)['first_name'] + ' ' + data.get_user(auth.session)['last_name'])
        menu = self.add_option(menu, 0, name='Show all users', key='1', action=lambda:self.set_menu(lambda:self.user_list_menu()))
        menu = self.add_option(menu, 0, name='Browse documents', key='2', action=lambda:self.set_menu(lambda:self.document_list_menu()))
        
        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Logout', key='l', action=lambda:[auth.logout(),self.set_menu(lambda:self.start_menu())])

        return menu

    # Menu de liste d'utilisateurs
    def user_list_menu(self, menu=None, users = {}):
        users = data.get_user_list()

        if users != {}:
            menu = self.add_field(menu, title='User list', text='')
            menu = self.add_option(menu, 0, name='Search', key='s')
            menu = self.add_option(menu, 0, name='Create', key='c', action=lambda:self.set_menu(lambda:self.user_create_menu()))
            menu = self.add_field(menu, title='', text='')
            key_index = 1
            for user_id, user_data in users.items():
                if user_data['suspended']:
                    menu = self.add_option(menu, 1, name=user_data['first_name'] + ' ' + user_data['last_name'] + f"{display.md.END} {display.md.RED}[Suspended]", key=str(key_index), action=lambda user_id=user_id: self.set_menu(lambda: self.user_menu(user_id)))
                else:
                    menu = self.add_option(menu, 1, name=user_data['first_name'] + ' ' + user_data['last_name'], key=str(key_index), action=lambda user_id=user_id: self.set_menu(lambda: self.user_menu(user_id)))
                key_index += 1
        else:
            menu = self.add_field(menu, title='User list', text='No user found.')

        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 2, name='Back', key='b', action=lambda:self.previous_menu())
        return menu

    def role_list_menu(self, menu=None, roles = {}):
        roles = data.get_role_list()

        if roles != {}:
            menu = self.add_field(menu, title='Role list', text='')
            key_index = 1
            for role_id, role_data in roles.items():
                menu = self.add_option(menu, 0, name=role_data['name'], key=str(key_index), action=lambda role_id=role_id: self.set_menu(lambda: self.user_menu(role_id)))
                key_index += 1
        else:
            menu = self.add_field(menu, title='Role list', text='No role found.')

        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Back', key='b', action=lambda:self.previous_menu())
        return menu

    # Menu d'utilisateur
    def user_menu(self, user_id, menu=None):
        user = data.get_user(user_id)

        if user['suspended']:
            menu = self.add_field(menu, title=user['first_name']+' '+user['last_name'] + f"{display.md.END} {display.md.RED}[Suspended]", text="ID: "+str(user['id']))
            menu = self.add_field(menu, title='', text='')
        else:
            menu = self.add_field(menu, title=user['first_name']+' '+user['last_name'], text="ID: "+str(user['id']))
            menu = self.add_field(menu, title='', text='')

        menu = self.add_option(menu, 1, name='change first and last name', key='1', action=lambda:self.previous_menu())
        menu = self.add_option(menu, 1, name='change the user name', key='2', action=lambda:self.previous_menu())
        menu = self.add_option(menu, 1, name='reset password', key='3', action=lambda:self.previous_menu())
        menu = self.add_option(menu, 1, name='change roles', key='4', action=lambda:self.previous_menu())
        if user['suspended']:
            menu = self.add_option(menu, 1, name='unsuspend account', key='5', action=lambda:[user.reactivate(), self.set_message(f'{display.md.GREEN}User reactivated.')])
        else:
            menu = self.add_option(menu, 1, name='suspend account', key='5', action=lambda:[data.u.import_users()[user_id].suspend() , self.set_message(f'{display.md.GREEN}User suspended.')])
        menu = self.add_option(menu, 1, name='delete account', key='6', action=lambda:self.previous_menu())

        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 2, name='Back', key='b', action=lambda:self.previous_menu())
        return menu

    # Menu de confirmation
    def confirmation_menu(self, menu=None, title='',field_title='',field_text='',yes_action=['y','yes',[]],no_action=['n','no',[]]):
        if no_action[2] == []:
            no_action[2] = lambda: self.previous_menu()
        if yes_action[2] == []:
            yes_action[2] = lambda: [self.previous_menu(),self.set_message(f'{display.md.YELLOW}No action has been associated with the selected answer.')]
        menu = self.add_field(menu, title=field_title, text=field_text)
        menu = self.add_option(menu, 0, name=yes_action[1], key=yes_action[0], action=yes_action[2])
        menu = self.add_option(menu, 0, name=no_action[1], key=no_action[0], action=no_action[2])
        return menu
    
    def delete_user_menu(self, user_id, menu=None):
        user = data.get_user(user_id)
        menu = self.add_field(menu, title='Delete user', text='')
        menu = self.add_field(menu, title='Are you sure you want to delete this user?', text='')
        menu = self.add_option(menu, 1, name='Yes', key='y', action=lambda:[data.u.import_users()[user_id].delete(), self.set_message(f'{display.md.GREEN}User deleted.'), self.previous_menu()])
        menu = self.add_option(menu, 1, name='No', key='n', action=lambda:self.previous_menu())
        return menu
    
    def user_create_menu(self, menu=None, firstname='', lastname='', password='', input_request='username'):
        menu = self.add_field(menu, title='Create user', text='')
        menu = self.add_option(menu, 0, name='First name:'+ firstname, key='1', action=lambda:self.set_menu(lambda:self.user_create_menu(firstname=firstname, lastname=lastname, password=password,input_request='firstname')))
        menu = self.add_option(menu, 0, name='Last name:' + lastname, key='2', action=lambda:self.set_menu(lambda:self.user_create_menu(firstname=firstname, lastname=lastname, password=password,input_request='lastname')))
        menu = self.add_option(menu, 0, name='Password:' + password, key='3', action=lambda:self.set_menu(lambda:self.user_create_menu(firstname=firstname, lastname=lastname, password=password,input_request='password')))

        menu = self.add_field(menu, title='', text='')
        menu = self.add_option(menu, 1, name='Create', key='c', action=lambda:self.previous_menu())
        menu = self.add_option(menu, 1, name='Back', key='b', action=lambda:self.previous_menu())

        menu['input']['input_text'] = 'Fill in the form:\n'

        if input_request == 'firstname':
            menu['input']['input_text'] = 'First name:\n'
            menu['input']['input_type'] = 'text'
            menu['input']['input_request'] = 'firstname'
        elif input_request == 'lastname':
            menu['input']['input_text'] = 'Last name:\n'
            menu['input']['input_type'] = 'text'
            menu['input']['input_request'] = 'lastname'
        elif input_request == 'password':
            menu['input']['input_text'] = 'Password:\n'
            menu['input']['input_type'] = 'password'
            menu['input']['input_request'] = 'password'
        return menu