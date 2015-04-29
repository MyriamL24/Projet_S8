#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import pickle
import psycopg2
import base64
from tkMessageBox import *




def connexion(Req, username, pswd):
    try:
        conn = psycopg2.connect(dbname=username, host="dbserver", user=username, password=base64.b64decode(pswd))
        cur = conn.cursor()
    except Exception:
            print "Impossible de se connecter à la base de données"
            return
    try:
            cur.execute(Req)
            column_name = [desc[0] for desc in cur.description]
    except:
            print "Impossible d'executer la requête"
    try:
        data = cur.fetchall()
    except Exception:
        showerror("Alerte", "Aucun résultats")
        pass
    conn.close()
    cur.close()

    return data, column_name


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


def deserialize(fich):
    pkl_file = open(fich, 'r')
    requetes = pickle.load(pkl_file)
    pkl_file.close()
    return requetes


def serialize(fich, data):
    output = open(fich, 'w')
    pickle.dump(data, output)
    output.close()




