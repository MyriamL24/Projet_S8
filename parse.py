# -*- coding: utf8 -*-
import Tkinter as tk
import ttk

def parse_choix(data, col, param):
    Liste = []
    tmp = []
    variable = data[0][0][col]
    for ligne in data[0] :
        if ligne[col] == variable:
            tmp.append(ligne[param])
        else :
            variable = ligne[col]
            Liste.append(tmp)
            tmp = []
            tmp.append(ligne[param])
    return Liste
