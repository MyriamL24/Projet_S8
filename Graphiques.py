# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import matplotlib.pyplot as plt
from PIL import Image as NewImage
from Tkinter import *
import numpy, Tkinter
import Stock, parse

histo = " "
courbe = " "

def alert():
    showinfo("alerte", "Bravo!")

def affichage_Image(fichier):
    
    W_image = Toplevel()
    fenetre = Canvas(W_image, width="600", height ="500")
    titi = PhotoImage(file = fichier) 
    fenetre.create_image(300,250,image = titi)
    fenetre.pack()
    Butt_Pdf = Button(W_image, text="Ajouter au PDF", command=alert)
    Butt_Pdf.pack(side=BOTTOM)
    Butt_Quit = Button(W_image, text="Quitter", command = W_image.destroy)
    Butt_Quit.pack()
    #W_image.mainloop()
    
def diagramme_baton():
    data =  Stock.deserialize("data.pkl")
    h = []
    x = [_ for _ in range(len(data[0]))]
    for ligne in data[0]:
        h.append(ligne[0])
     
    fig = plt.figure()
    width = 0.8
    plt.bar(x, h, width, color = 'b')
    plt.savefig('histogram.eps')
    histo = "histogram.eps"
    #plt.show()
    img = NewImage.open("histogram.eps")    
    img.save("figure.gif", "gif")
    affichage_Image("figure.gif")

def courbes():
    data = Stock.deserialize("data.pkl")
    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
         y.append(ligne[0])

#diagramme_baton()
#affichage_Image()
