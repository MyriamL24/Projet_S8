#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import pickle
import psycopg2
import base64
import time
import os
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
    Log("Ouverture du fichier"+fich)
    pickle.dump(data, output)
    Log("Sauvegarde et sérialisation des données dans le fichier"+fich)
    output.close()
    Log("Fermeture du fichier"+fich)


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
    Log("Ouverture du fichier"+fich)
    donnees = pickle.load(pkl_file)
    Log("Dérialisation des données contenues dans le fichier"+fich)
    pkl_file.close()
    print "fichier fermé"
    Log("Fermeture du fichier"+fich)
    return donnees


# Permits to get the follow-up of operations
def Log(info):
    log = open("Logndat.txt", "a")
    Date = time.strftime('%d/%m/%y %H:%M', time.localtime())
    log.write(Date + ' : ' + info + '\n')
    log.close()

def display_help():
    try:
        os.system("firefox ./Aide/aide.html")
    except Exception:
        showerror("Alerte","Avez vous firefox d'insallé ?")

def Tex_Front_Page(file):
     file.write("\documentclass[a4paper,12pt]{report}\n"+"\usepackage[utf8]{inputenc}\n"+"\usepackage[T1]{fontenc}\n"+ "\usepackage[francais]{babel}\n" + 
        "\usepackage{graphicx} \n"+
        "\usepackage{enumitem}\n"+
        "\usepackage{underscore}\n"+
        "\usepackage{float}\n"+
        "\usepackage{array}\n"+
        "\usepackage{soul}\n"+
        "\usepackage{ulem}\n"+
        "\usepackage{amsmath}\n"+
        "\usepackage{sectsty}\n"+
        "\usepackage{geometry}\n"+
        "\usepackage{titlesec} \n"+
        "\usepackage{titletoc}\n"+
        "\usepackage{vmargin}\n"+
        "\usepackage{verbatim}\n"+
        "\usepackage{fancyvrb}\n"+
        "\usepackage{fancyhdr}\n"+
        "\usepackage{eurosym}\n"+
        "\usepackage{color}\n"+
        "\\newcommand{\HRule}{\\rule{\linewidth}{0.5mm}}\n"+
        "\makeatletter\n"+
        "\setlength{\headheight}{11.0pt}\n"+
        "\\renewcommand{\headrulewidth}{1pt}\n"+
        "\\titlespacing*{\chapter}\n"+
        "  {0pt}     % retrait à gauche\n"+
        "  {0pt}     % espace avant\n"+
        "  {30pt}    % espace après\n"+
        "   [0pt]    % retrait à droite\n"+
        "% Style du titre de chapitre\n"+
        "\\titleformat{\chapter}[frame]{\huge\\normalfont\sc}{\\filright\\footnotesize\enspace CHAPITRE \\thechapter\enspace}{8pt}{\\filcenter}{}\n"+
        "% Style de titre de section\n"+
        "\\titleformat{\subsection}[hang]{\\bfseries\sc}{\Large\\thesubsection}{1em}{}\n"+
        "% Mise en place du Sommaire\n"+
        "\\titlecontents{chapter}[3em]{\\addvspace{1em plus 0pt}\\bfseries\Large}{\contentslabel{2em}}{\hspace{-1.3em}}{\hfill\contentspage}[\\addvspace{3pt}]\n"+
        "\\begin{document}\n"+
        "%titre\n"+
        "\\begin{center}\n"+
        "\LARGE{Compte rendu statistique} \\\n"+
        "\end{center}\n")
    
