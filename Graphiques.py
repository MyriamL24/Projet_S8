# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import matplotlib.pyplot as plt
from PIL import Image as NewImage
from Tkinter import *
import libnDat
import Reporting
import Pmw
import anydbm

List_Images = []
Stock = anydbm.open('Stock.dbm', 'c')


def alert():
    showinfo("alerte", "Bravo!")


# Fuction to display images

def Display_Image(fichier):

    # Part for the exit button

    def Exit_Graph_Display():
        Tab_Graph.delete(Pmw.SELECT)
        if Tab_Graph.index(Pmw.END, forInsert=True) == 0:
            W_Image.destroy()
            List_Images[:] = []

    Name_Tab_Graph = 'Fig. ' + str(len(List_Images))

    Stock[Name_Tab_Graph] = fichier


    # Based on the Lenght of the List_Images (contains ref. to the images),
    # Open a new window (Toplevel) or a new Tab

    if len(List_Images) == 0:

        # Opens New window

        global W_Image, Tab_Graph
        W_Image = Toplevel()

        Tab_Graph = Pmw.NoteBook(W_Image)
        Tab_Graph.pack(fill="both", expand=1, padx=10, pady=10)

        Graph = Tab_Graph.add(Name_Tab_Graph)
        Tab_Graph.tab(Name_Tab_Graph).focus_set()

        Display = Canvas(Graph, width="600", height="500")
        List_Images.append(PhotoImage(file=fichier))
        Display.create_image(300, 250, image=List_Images[-1])
        Display.image = List_Images[-1]
        Display.pack()

        Tab_Graph.setnaturalsize()

        Butt_Quit = Button(W_Image, text="Fermer", command=Exit_Graph_Display)
        Butt_Quit.pack(side=RIGHT)
        Butt_Pdf = Button(
            W_Image, text="Ajouter au PDF",
            command=lambda: Reporting.Insert_PDF(2, Stock[str(Tab_Graph.getcurselection())]))
        Butt_Pdf.pack(side=RIGHT)

    else:

        # Opens New Tab

        Graph = Tab_Graph.add(Name_Tab_Graph)
        Tab_Graph.selectpage(Name_Tab_Graph)

        Display = Canvas(Graph, width="600", height="500")
        List_Images.append(PhotoImage(file=fichier))
        Display.create_image(300, 250, image=List_Images[-1])
        Display.image = List_Images[-1]
        Display.pack()

        Tab_Graph.setnaturalsize()


def Diagram_Stick(ref):

    data = libnDat.deserialize(ref)

    h = []
    x = [_ for _ in range(len(data[0]))]
    for ligne in data[0]:
        h.append(ligne[0])
    width = 0.8
    plt.bar(x, h, width, color='b')

    Name_Diag = "./Images/Graphes/Diag_" + str(len(List_Images))

    plt.savefig(Name_Diag + ".eps")
    plt.clf()

    img = NewImage.open(Name_Diag + ".eps")
    img.save(Name_Diag + ".gif", "gif")

    Display_Image((str(Name_Diag) + ".gif"))
    libnDat.Log("Diagram Stick")


def Curves(ref):

    data = libnDat.deserialize(ref)

    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.plot(x, y, color='r')

    Name_Curves = "./Images/Graphes/Courbe_" + str(len(List_Images))

    plt.savefig(Name_Curves + ".eps")
    plt.clf()
    img = NewImage.open(Name_Curves + ".eps")

    img.save(Name_Curves + ".gif", "gif")

    Display_Image((str(Name_Curves) + ".gif"))
    libnDat.Log("Diagram Curves")


def Dot_Plot(ref):

    data = libnDat.deserialize(ref)

    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.scatter(x, y, color='r')

    Name_Dot_Plot = "./Images/Graphes/Dot_" + str(len(List_Images))

    plt.savefig(Name_Dot_Plot + ".eps")
    plt.clf()

    img = NewImage.open(Name_Dot_Plot + ".eps")
    img.save(Name_Dot_Plot + ".gif", "gif")

    Display_Image((str(Name_Dot_Plot) + ".gif"))


def Box_Plot(ref):

    data = libnDat.deserialize(ref)

    donnee = libnDat.parse_choix(data, len(data[1]) - 1, len(data[1]) - 2)
    plt.boxplot(donnee)

    Name_Box_Plot = "./Images/Graphes/Box_" + str(len(List_Images))

    plt.savefig(Name_Box_Plot + ".eps")
    plt.clf()
    img = NewImage.open(Name_Box_Plot + ".eps")
    img.save(Name_Box_Plot + ".gif", "gif")

    Display_Image((str(Name_Box_Plot) + ".gif"))
    libnDat.Log("Box Plot")


def Histogram(ref):

    data = libnDat.deserialize(ref)

    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.hist(y)

    Name_Histo = "./Images/Graphes/Histo_" + str(len(List_Images)) 

    plt.savefig(Name_Histo + ".eps")
    plt.clf()
    img = NewImage.open(Name_Histo + ".eps")
    img.save(Name_Histo + ".gif", "gif")

    Display_Image((str(Name_Histo) + ".gif"))
    libnDat.Log("Box Plot")