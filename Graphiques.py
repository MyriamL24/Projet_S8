# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

import matplotlib.pyplot as plt
from PIL import Image as NewImage
from Tkinter import *
import libnDat
import Reporting
import Pmw

List_Images = []


def alert():
    showinfo("alerte", "Bravo!")


# Function to display images

def Display_Image(fichier, L):

    # Part for the exit button

    def Exit_Graph_Display():
        Tab_Graph.delete(Pmw.SELECT)
        if Tab_Graph.index(Pmw.END, forInsert=True) == 0:
            W_Image.destroy()
            L[:] = []

    Name_Tab_Graph = 'Fig. ' + str(len(L))

    # Based on the Lenght of the List_Images (contains ref. to the images),
    # Open a new window (Toplevel) or a new Tab

    if len(L) == 0:

        # Opens New window

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
        Butt_Pdf = Button(
            W_Image, text="Ajouter au PDF",
            command=lambda: Reporting.Insert_PDF(3))
        Butt_Pdf.pack(side=RIGHT)

    else:

        # Opens New Tab

        Graph = Tab_Graph.add(Name_Tab_Graph)
        Tab_Graph.selectpage(Name_Tab_Graph)

        Display = Canvas(Graph, width="600", height="500")
        L.append(PhotoImage(file=fichier))
        Display.create_image(300, 250, image=L[-1])
        Display.image = L[-1]
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

    plt.savefig("./Images/Graphes/Diag" + str(len(List_Images)) + ".eps")
    plt.clf()
    img = NewImage.open(
        "./Images/Graphes/Diag" + str(len(List_Images)) + ".eps")
    img.save("./Images/Graphes/Diag" + str(len(List_Images)) + ".gif", "gif")

    Display_Image(
        "./Images/Graphes/Diag" + str(len(List_Images)) + ".gif", List_Images)
    libnDat.Log("Diagram Stick")


def Curves(ref):

    data = libnDat.deserialize(ref)

    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.plot(x, y, color='r')

    plt.savefig("./Images/Graphes/Courbe" + str(len(List_Images)) + ".eps")
    plt.clf()
    img = NewImage.open(
        "./Images/Graphes/Courbe" + str(len(List_Images)) + ".eps")
    img.save("./Images/Graphes/Courbe" + str(len(List_Images)) + ".gif", "gif")

    Display_Image(
        "./Images/Graphes/Courbe" + str(len(List_Images))
        + ".gif", List_Images)
    libnDat.Log("Diagram Curves")


def Dot_Plot(ref):

    data = libnDat.deserialize(ref)

    x = [_ for _ in range(len(data[0]))]
    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.scatter(x, y, color='r')

    plt.savefig("./Images/Graphes/Dot" + str(len(List_Images)) + ".eps")
    plt.clf()
    img = NewImage.open(
        "./Images/Graphes/Dot" + str(len(List_Images)) + ".eps")
    img.save("./Images/Graphes/Dot" + str(len(List_Images)) + ".gif", "gif")

    Display_Image(
        "./Images/Graphes/Dot" + str(len(List_Images)) + ".gif", List_Images)
    libnDat.Log("Dot Plot")


def Box_Plot(ref):

    data = libnDat.deserialize(ref)

    donnee = libnDat.parse_choix(data, len(data[1]) - 1, len(data[1]) - 2)
    plt.boxplot(donnee)

    plt.savefig("./Images/Graphes/Box" + str(len(List_Images)) + ".eps")
    plt.clf()
    img = NewImage.open(
        "./Images/Graphes/Box" + str(len(List_Images)) + ".eps")
    img.save("./Images/Graphes/Box" + str(len(List_Images)) + ".gif", "gif")

    Display_Image(
        "./Images/Graphes/Box" + str(len(List_Images)) + ".gif", List_Images)
    libnDat.Log("Box Plot")


def Histogram(ref):

    data = libnDat.deserialize(ref)

    y = []
    for ligne in data[0]:
        y.append(ligne[0])
    plt.hist(y)

    plt.savefig("./Images/Graphes/Histo" + str(len(List_Images)) + ".eps")
    plt.clf()
    img = NewImage.open(
        "./Images/Graphes/Histo" + str(len(List_Images)) + ".eps")
    img.save("./Images/Graphes/Histo" + str(len(List_Images)) + ".gif", "gif")

    Display_Image(
        "./Images/Graphes/Histo" + str(len(List_Images)) + ".gif", List_Images)
    libnDat.Log("Box Plot")