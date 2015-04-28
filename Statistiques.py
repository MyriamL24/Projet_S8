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
    res = wilcoxon(liste[0], liste[1])
    result = " Test des rangs signés de Wilcoxon \n\n T : "+str(res[0])+"\n p.value : "+str(res[1])    
    W_Result = Toplevel()
    txt=Text(W_Result,width=50,height=5)
    txt.pack()
    txt.insert(END,result)    
    Button(W_Result, text="Ajouter au PDF", command=alert).pack(side = LEFT, fill = X)
    Button(W_Result, text="Quitter", command = W_Result.destroy).pack(side = RIGHT, fill = X)

def Student() :
    data =  Stock.deserialize("data.pkl")
    liste = parse.parse_choix(data,1,0)
    res = ttest_ind(liste[0], liste[1])
    result = " Test de student \n\n T : "+str(res[0])+"\n p.value : "+str(res[1])
    W_Result = Toplevel()
    txt=Text(W_Result,width=50,height=5)
    txt.pack()
    txt.insert(END,result)    
    Button(W_Result, text="Ajouter au PDF", command=alert).pack(side = LEFT, fill = X)
    Button(W_Result, text="Quitter", command = W_Result.destroy).pack(side = RIGHT, fill = X)


def Kruskall_wallis():
    data =  Stock.deserialize("data.pkl")
    liste = parse.parse_choix(data,len(data[1])-1,len(data[1])-2)
    
    res = mstats.kruskalwallis(liste)
    """result = " Test de Kruskall-Wallis \n\n W : "+str(res[0])+"\n p.value : "+str(res[1])
    W_Result = Toplevel()
    txt=Text(W_Result,width=50,height=5)
    txt.pack()
    txt.insert(END,result)    
    Button(W_Result, text="Ajouter au PDF", command=alert).pack(side = LEFT, fill = X)
    Button(W_Result, text="Quitter", command = W_Result.destroy).pack(side = RIGHT, fill = X)"""

def alert():
    showinfo("Alerte", "Coucou!")
    
Kruskall_wallis()
