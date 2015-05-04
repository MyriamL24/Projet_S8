# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import matplotlib.pyplot as plt
from PIL import Image as NewImage
from Tkinter import *
import libnDat
import Reporting
import Pmw

L = []


def alert():
    showinfo("alerte", "Bravo!")


def Display_Image(fichier, L):

    def Exit_Graph_Display():
        W_Image.destroy()
        L[:] = []

    Name_Tab_Graph = 'Fig. ' + str(len(L))

    if len(L) == 0:
        global W_Image, Tab_Graph
        W_Image = Toplevel()
        Tab_Graph = Pmw.NoteBook(W_Image)
        Tab_Graph.pack(fill="both", expand=1, padx=10, pady=10)

        Graph = Tab_Graph.add(Name_Tab_Graph)
        Tab_Graph.tab(Name_Tab_Graph).focus_set()

        Display = Canvas(Graph, width="600", height="500")
        L.append(PhotoImage(file=fichier))
        Display.create_image(300, 250, image=L[-1])
        Display.image = L[-1]
        Display.pack()

        Tab_Graph.setnaturalsize()

        Butt_Quit = Button(W_Image, text="Fermer", command=Exit_Graph_Display)
        Butt_Quit.pack(side=RIGHT)
        Butt_Pdf = Button(W_Image, text="Ajouter au PDF", command=Reporting.Insert_Image)
        Butt_Pdf.pack(side=RIGHT)

    else:

        Graph = Tab_Graph.add(Name_Tab_Graph)
        Tab_Graph.tab(Name_Tab_Graph).focus_set()

        Display = Canvas(Graph, width="600", height="500")
        L.append(PhotoImage(file=fichier))
        Display.create_image(300, 250, image=L[-1])
        Display.image = L[-1]
        Display.pack()

        Tab_Graph.setnaturalsize()

def Diagram_Stick():
    data = libnDat.deserialize("data.pkl")
    h = []
    x = [_ for _ in range(len(data[0]))]
    for ligne in data[0]:
        h.append(ligne[0])
    width = 0.8
    plt.bar(x, h, width, color='b')

    plt.savefig('./Images/Graphes/Diag.eps')
    plt.clf()
    img = NewImage.open("./Images/Graphes/Diag.eps")
    img.save("./Images/Graphes/Diag.gif", "gif")
    Display_Image("./Images/Graphes/Diag.gif", L)
    libnDat.Log("Diagram Stick")


def Curves():
    data = libnDat.deserialize("data.pkl")
    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.plot(x, y, color='r')

    plt.savefig('./Images/Graphes/Courbe.eps')
    plt.clf()
    img = NewImage.open("./Images/Graphes/Courbe.eps")
    img.save("./Images/Graphes/Courbe.gif", "gif")
    Display_Image("./Images/Graphes/Courbe.gif", L)
    libnDat.Log("Diagram Curves")


def Dot_Plot():
    data = libnDat.deserialize("data.pkl")
    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.scatter(x, y, color='r')

    plt.savefig('./Images/Graphes/Dot.eps')
    plt.clf()
    img = NewImage.open("./Images/Graphes/Dot.eps")
    img.save("./Images/Graphes/Dot.gif", "gif")
    Display_Image("./Images/Graphes/Dot.gif", L)
    libnDat.Log("Dot Plot")


def Box_Plot():
    data = libnDat.deserialize("data.pkl")
    donnee = libnDat.parse_choix(data, len(data[1])-1, len(data[1])-2)
    plt.boxplot(donnee)

    plt.savefig('./Images/Graphes/Box.eps')
    plt.clf()
    img = NewImage.open("./Images/Graphes/Box.eps")
    img.save("./Images/Graphes/Box.gif", "gif")
    Display_Image("./Images/Graphes/Box.gif", L)
    libnDat.Log("Box Plot")


def histogramme():
    data = libnDat.deserialize("data.pkl")

    y = []
    for ligne in data[0]:
         y.append(ligne[0])
    plt.hist(y)
    
    plt.savefig('./Images/Graphes/Box.eps')
    plt.clf()
    img = NewImage.open("./Images/Graphes/Box.eps")
    img.save("./Images/Graphes/Box.gif", "gif")
    Display_Image("./Images/Graphes/Box")
    libnDat.Log("Box Plot")