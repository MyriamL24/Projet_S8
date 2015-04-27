# -*- coding: utf8 -*-
import Tkinter as tk
import ttk
import Base

def parse_choix(data, param, col):
    Liste = []
    tmp = []
    variable = data[0][0][col]
    for ligne in data[0] :
        if ligne[param] == variable:
            tmp.append(ligne[col])
        else :
            variable = ligne[param]
            Liste.append(tmp)
            tmp = []
            tmp.append(ligne[col])
    return Liste





