#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import pickle
import psycopg2
import base64
import time
from tkMessageBox import *


# Connexion to database
def connexion(Req, username, pswd):
    try:
        conn = psycopg2.connect(
            dbname=username, host="dbserver",
            user=username, password=base64.b64decode(pswd))
        cur = conn.cursor()
    except Exception:
        showerror('Alert',"Impossible de se connecter à la base de données")
        return
    try:
        cur.execute(Req)
        column_name = [desc[0] for desc in cur.description]
    except:
        showerror('Alerte',"Impossible d'executer la requête")
        return
    try:
        data = cur.fetchall()
    except Exception:
        showerror("Alerte", "Aucun résultats")
        return
    conn.close()
    cur.close()

    return data, column_name


# Allows to save in a pickle flat file
def serialize(fich, data):
    output = open(fich, 'w')
    pickle.dump(data, output)
    output.close()


# Used to order datas to perform stats on
def parse_choix(data, col, param):
    Liste = []
    tmp = []
    variable = data[0][0][col]
    for ligne in data[0]:
        if ligne[col] == variable:
            tmp.append(ligne[param])
        else:
            variable = ligne[col]
            Liste.append(tmp)
            tmp = []
            tmp.append(ligne[param])
    return Liste


# Allows to read serialized files
def deserialize(fich):
    pkl_file = open(fich, 'r')
    requetes = pickle.load(pkl_file)
    pkl_file.close()
    return requetes


# Permits to get the follow-up of operations
def Log(info):
    log = open("Logndat.txt", "a")
    Date = time.strftime('%d/%m/%y %H:%M', time.localtime())
    log.write(Date + ' : ' + info + '\n')
    log.close()