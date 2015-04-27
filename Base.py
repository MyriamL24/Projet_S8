# -*- coding: utf-8 -*-
import psycopg2
import base64
from tkMessageBox import *

#username = ''
#pswd = base64.b64encode('')


def connexion(Req, username, pswd):

    print base64.b64decode(pswd)
    
    try:
        conn = psycopg2.connect(dbname=username, host="dbserver", user=username,  password=base64.b64decode(pswd))
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
        showerror("Alerte","Aucun résultats")
        pass


    conn.close()
    cur.close()

    return data, column_name


