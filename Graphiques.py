# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import matplotlib.pyplot as plt
from PIL import Image as NewImage
from Tkinter import *
import libnDat
import numpy
import Reporting

histo = " "
courbe = " "


def alert():
    showinfo("alerte", "Bravo!")


def affichage_Image(fichier):
    W_image = Toplevel()
    fenetre = Canvas(W_image, width="600", height ="500")
    global img
    img = PhotoImage(file=fichier+".gif")

    fenetre.create_image(300, 250, image=img)
    fenetre.pack()

    Butt_Quit = Button(W_image, text="Quitter", command=W_image.destroy)
    Butt_Quit.pack(side=RIGHT)
    Butt_Pdf = Button(W_image, text="Ajouter au PDF", command=Reporting.Insert_Image(3, fichier))
    Butt_Pdf.pack(side=RIGHT)



def diagramme_baton():
    data = libnDat.deserialize("data.pkl")
    h = []
    x = [_ for _ in range(len(data[0]))]
    for ligne in data[0]:
        h.append(ligne[0])
    width = 0.8
    plt.bar(x, h, width, color='b')

    plt.savefig('./Images/Graphes/Diag.eps')
    imgdb = NewImage.open("./Images/Graphes/Diag.eps")
    imgdb.save("./Images/Graphes/Diag.gif", "gif")
    affichage_Image("./Images/Graphes/Diag")
    imgdb.close()


def courbes():
    data = libnDat.deserialize("data.pkl")
    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
         y.append(ligne[0])
    plt.plot(x,y,color='r')

    plt.savefig('./Images/Graphes/Courbe.eps')
    imgc = NewImage.open("./Images/Graphes/Courbe.eps")
    imgc.save("./Images/Graphes/Courbe.gif", "gif")
    affichage_Image("./Images/Graphes/Courbe")
    imgc.close()


def Dot_Plot():
    data = libnDat.deserialize("data.pkl")
    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
         y.append(ligne[0])
    plt.scatter(x,y,color='r')  

    plt.savefig('./Images/Graphes/Dot.eps')
    imgd = NewImage.open("./Images/Graphes/Dot.eps")
    imgd.save("./Images/Graphes/Dot.gif", "gif")
    affichage_Image("./Images/Graphes/Dot")
    imgd.close()


def Box_Plot():
    data = libnDat.deserialize("data.pkl")
    donnee = libnDat.parse_choix(data, len(data[1])-1,len(data[1])-2)
    plt.boxplot(donnee)

    plt.savefig('./Images/Graphes/Box.eps')
    imgb = NewImage.open("./Images/Graphes/Box.eps")
    imgb.save("./Images/Graphes/Box.gif", "gif")
    affichage_Image("./Images/Graphes/Box")
    imgb.close()
