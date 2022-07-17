#!/usr/bin/python3
# coding: utf-8
import sqlite3, re, sys, os, signal, random
from termcolor import colored, cprint
from tabulate import tabulate
from time import sleep
from mailer import sendmail
import config

def def_handler(sig, frame):
    cprint(f"\n\n\t[!] Saliendo...", "red")
    sys.exit(1)

#CTRL + C
signal.signal(signal.SIGINT, def_handler)

def execute_query(query, fetch=False):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    if fetch:
        fetch = cursor.fetchall()
        return fetch
    conn.close()

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(config.DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(e)

def initialize_database():
    execute_query("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE)")

def add_user(option):
    print(option, end="\n\n")
    name = input("Favor ingresar nombre: ")
    email = input("Favor ingresar email: ")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    while not (re.fullmatch(regex, email)):
        cprint("\n\t[!] Email inválido\n", "red")
        email = input("Favor ingresar email: ")

    execute_query(f"INSERT INTO users (name, email) VALUES ('{name}','{email}')")
    cprint("\n\t[+] Participante agregado correctamente", "green")
    sleep(2)

def list_users(option):
    print(option, end="\n\n")
    users = execute_query("SELECT name, email from users", True)
    if len(users) < 1:
        cprint("\n\t[!] No se han registrado participantes", "red")
        sleep(2)
    else: 
        print(tabulate(users, headers=["Nombre","Email"], tablefmt="fancy_grid"))
        input("\n\nPresiona ENTER para continuar")

def del_user(option):
    print(option, end="\n\n")
    users = execute_query("SELECT id, name, email from users", True)

    if len(users) < 1:
        cprint("\n\t[!] No se han registrado participantes", "red")
        sleep(2)
    else: 
        print(tabulate(users, headers=["ID","Nombre","Email"], tablefmt="fancy_grid"), end="\n\n")
        user_id = input("Ingrese ID de participante a eliminar: ")
        regex = r'^\d+'
        if (re.fullmatch(regex, user_id)):
            user_id = int(user_id)

        id_array = []
        for i in range (0, len(users)):
            id_array.append(users[i][0])

        # validate input
        if user_id not in id_array:
            cprint("\n\t[!] Favor ingresar un ID válido", "red")
            sleep(2)
        else:
            execute_query(f"DELETE FROM users WHERE id = {user_id}")
            cprint("\n\t[-] Participante eliminado correctamente", "green")
            sleep(2)

def get_random(email_list):
    participant = random.choice(email_list)
    return participant

def execute_lottery(email_list):
    counter = 0
    recipient_list = []
    sending_list = []
    for user in email_list:
        while user not in sending_list:
            participant = get_random(email_list)
            while participant in recipient_list:
                participant = get_random(email_list)
            if participant != user:
                recipient_list.append(participant)
                sending_list.append(user)
            counter += 1
            # Re-run lottery if is looping
            if counter > 100:
                return False
    return recipient_list

def lottery(option, simulation=True):
    print(option, end="\n\n")
    users = execute_query("SELECT name, email from users", True)
    email_list = [] 

    if len(users) < 2:
        input(colored("\n[!] Favor ingresar un mínimo de 2 participantes ", "red"))
    else:
        for i in range(0,len(users)):
            email_list.append(users[i][1])

        result = False
        while not result:
            result = execute_lottery(email_list)

        if not simulation:
            for i in range (0, len(result)):
                print(email_list[i] + " ->  ?")
            value = input(colored("\n[+] Sorteo válido, ¿quieres enviar la notificación a los participantes? [S/N]: ", "green")).strip()
            if value == "S":
                for i in range (0, len(result)):
                    sender = execute_query(f"SELECT name from users WHERE email = '{email_list[i]}'", True)
                    recipient = execute_query(f"SELECT name from users WHERE email = '{result[i]}'", True)
                    sendmail(sender[0][0], email_list[i], recipient[0][0], result[i])
                input("\n\nPresiona ENTER para continuar ")

        else:
            for i in range (0, len(result)):
                print(email_list[i] + " -> " + result[i])
            input("\n\nPresiona ENTER para continuar ")

def menu():
    initialize_database()

    while True:
        os.system('clear')
        banner = "¡Bienvenido al sorteo de amigo secreto!"
        print(banner, "="*len(banner), sep="\n", end="\n\n")

        option_1 = "1) Agregar participante"
        option_2 = "2) Eliminar participante"
        option_3 = "3) Listar participantes"
        option_4 = "4) Simular sorteo"
        option_5 = "5) Ejecutar sorteo"
        option_6 = "6) Salir"
        
        print(option_1, option_2, option_3, option_4, option_5, option_6, sep="\n", end="\n\n")

        user_input = input("Favor seleccionar una opción: ")
        regex = r'^[1-6]'

        if (re.fullmatch(regex, user_input)):
            option = int(user_input)
            os.system('clear')

            if option == 1:
                add_user(option_1)
            if option == 2:
                del_user(option_2)
            if option == 3:
                list_users(option_3)
            if option == 4:
                lottery(option_4)
            if option == 5:
                lottery(option_5, False)
            if option == 6:
                cprint("\n[!] Saliendo...", "red")
                sys.exit()
        else:
            cprint("\n\t[!] Invalid option\n", "red")
            sleep(2)

if __name__ == '__main__':
    menu()
