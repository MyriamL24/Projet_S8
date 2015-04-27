# -*- coding: utf-8 -*-
from Tkinter import *
from scipy.stats import *
import Stock, parse
from tkMessageBox import *

def Shapiro():    
    data = Stock.deserialize("data.pkl")    
    res =  shapiro(data[0])
    if res[1] >= 0.05:
        result = " Test de Shapiro \n\nLa population suit une loi normale\n W : "+str(res[0])+"\n p.value : "+str(res[1])
    else :
        result = "Test de Shapiro \n\nLa population ne suit pas une loi normale\n W : "+str(res[0])+"\n p.value : "+str(res[1])
    W_Result = Toplevel()
    txt=Text(W_Result,width=50,height=5)
    txt.pack()
    txt.insert(END,result)    
    Button(W_Result, text="Ajouter au PDF", command=alert).pack(side = LEFT, fill = X)
    Button(W_Result, text="Quitter", command = W_Result.destroy).pack(side = RIGHT, fill = X)

def Wilcoxon():
    data =  Stock.deserialize("data.pkl")
    liste = parse.parse_choix(data,1,0)  
    res = wilcoxon(liste[1], liste[4])
    result = " Test des rangs signés de Wilcoxon \n T : "+str(res[0])+"\n p.value : "+str(res[1])    
    W_Result = Toplevel()
    txt=Text(W_Result,width=50,height=5)
    txt.pack()
    txt.insert(END,result)    
    Button(W_Result, text="Ajouter au PDF", command=alert).pack(side = LEFT, fill = X)
    Button(W_Result, text="Quitter", command = W_Result.destroy).pack(side = RIGHT, fill = X)

def Student() :

    data =  Stock.deserialize("data.pkl")
    liste = parse.parse_choix(data,1,0)  
    res = ttest_ind(pop1, pop2)
    result = " Test de student T : "+str(res[0])+"\n p.value : "+str(res[1])
    W_Result = Toplevel()
    txt=Text(W_Result,width=50,height=5)
    txt.pack()
    txt.insert(END,result)    
    Button(W_Result, text="Ajouter au PDF", command=alert).pack(side = LEFT, fill = X)
    Button(W_Result, text="Quitter", command = W_Result.destroy).pack(side = RIGHT, fill = X)


def Kruskall_wallis():
    res = mstats.kruskalwallis(liste)
    if res[1] >= 0.05:
        result = " Test de Shapiro \nLa population suit une loi normale\n W : "+str(res[0])+"\n p.value : "+str(res[1])
    else :
        result = "Test de Shapiro \nLa population ne suit pas une loi normale\n W : "+str(res[0])+"\n p.value : "+str(res[1])
    return result

def alert():
    showinfo("alerte", "Bravo!")
