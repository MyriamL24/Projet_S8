# -*- coding: utf-8 -*-
import psycopg2
import base64

#username = ''
#pswd = base64.b64encode('')


def connexion(Req, username, pswd):
    
    try :
            conn = psycopg2.connect(dbname =  username, host = "dbserver", user = username,  password = base64.b64decode(pswd))
    except:
            print "Impossible de se connecter à la base de données" 

    cur = conn.cursor()

    try :
            cur.execute(Req)
            column_name = [desc[0] for desc in cur.description]
    except:
            print "Impossible d'executer la requête"

    data = cur.fetchall()

    conn.close()
    cur.close()

    return data, column_name


