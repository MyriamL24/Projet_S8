#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART


from Tkinter import *
from tkMessageBox import *
import anydbm
import base64
import Pmw
import ttk
import libnDat
import Graphiques
import Statistiques
import Reporting
import os

username = 'mlopez001006'
pswd = base64.b64encode('')

# Clearing previous tmp files such as Graphs
files = os.listdir('./Images/Graphes/')
for i in range(0, len(files)):
    os.remove('./Images/Graphes/' + files[i])
os.remove('./Stock.dbm')

W_Main = Tk()
Pmw.initialise(W_Main)

W_Main.title('Better bet on Bacon\'')
W_Main.geometry("550x250+50+50")
W_Main.resizable(width=False, height=True)

DB_Rq = anydbm.open('Requetes.dbm', 'c')
PDF_titles = anydbm.open('PDF_Titles.dbm', 'c')
Stock = anydbm.open('Stock.dbm', 'c')


List_Tab_Name = []


def Send_Data(query, user, pwd):

    def Exit_Data_Display():
        Tab_Data.delete(Pmw.SELECT)
        if Tab_Data.index(Pmw.END, forInsert=True) == 0:
            W_Data.destroy()
            List_Tab_Name[:] = []

    # Catch data into a variable
    data = libnDat.connexion(query, user, pwd)

    # Write datas into a dedicated file, each request get one file
    libnDat.serialize(
        "./Donnees/data_" + str(len(List_Tab_Name)) + ".pkl", data)

    # Allows to order names of the differents Tab chronologicaly
    Name_Tab_Data = 'Data ' + str(len(List_Tab_Name))

    # Create a reference with the name of the file linked for each request
    Stock[str(Name_Tab_Data)] = "./Donnees/data_" + \
        str(len(List_Tab_Name)) + ".pkl"

    if data:
        if len(List_Tab_Name) == 0:
            global W_Data, Tab_Data

            # Creation of the new window
            W_Data = Toplevel()
            W_Data.title("Data")
            W_Data.maxsize(width=550, height=-1)

            # Update the number of the Tab in the List_Tab_Name list
            List_Tab_Name.append(Name_Tab_Data)

            # Creation of the Tab widget
            Tab_Data = Pmw.NoteBook(W_Data)
            Tab_Data.pack(fill="both", expand=1, padx=10, pady=10)

            # First Tab of the new window
            Tab = Tab_Data.add(Name_Tab_Data)
            Tab_Data.tab(Name_Tab_Data).focus_set()

            # Creation of the area to display datas
            Frame_Data = Frame(Tab)
            Frame_Data.pack(fill=BOTH)
            Frame_Data.dataCols = data[1]
            Frame_Data.tree = ttk.Treeview(
                Frame_Data, columns=Frame_Data.dataCols, show='headings')

            # Scrollbars (i.e xsb = x scrollbar)
            xsb = ttk.Scrollbar(Frame_Data, orient=HORIZONTAL,
                                command=Frame_Data.tree.xview)
            xsb.pack(side=BOTTOM, fill=X)
            ysb = ttk.Scrollbar(
                Frame_Data, orient=VERTICAL, command=Frame_Data.tree.yview)
            ysb.pack(side=RIGHT, fill=Y)
            Frame_Data.tree.pack(fill=BOTH, anchor=S)
            Frame_Data.tree['yscroll'] = ysb.set
            Frame_Data.tree['xscroll'] = xsb.set
            Frame_Data.tree.pack(fill=BOTH, anchor=S)
            Frame_Data.tree['yscroll'] = ysb.set
            Frame_Data.tree['xscroll'] = xsb.set

            # Displaying datas
            for c in Frame_Data.dataCols:
                Frame_Data.tree.heading(c, text=c.title())

            for item in data[0]:
                Frame_Data.tree.insert('', 'end', values=item)

            # Add line in Log file
            libnDat.Log(("Query sent : " + query))

            Tab_Data.setnaturalsize()

            # Creation of Data Menubar
            Menubar_Data = Menu(Frame_Data)

            menu1 = Menu(Menubar_Data, tearoff=0)
            menu1.add_command(label="Shapiro", command=lambda: Statistiques.Shapiro(Stock[str(Tab_Data.getcurselection())]))
            menu1.add_command(label="Student", command=lambda: Statistiques.Student(Stock[str(Tab_Data.getcurselection())]))
            menu1.add_command(
                label="Kruskall-Wallis", command=lambda: Statistiques.Kruskall_wallis(Stock[str(Tab_Data.getcurselection())]))

            menu1.add_command(label="Wilcoxon", command=lambda: Statistiques.Wilcoxon(Stock[str(Tab_Data.getcurselection())]))
            menu1.add_command(label="Pearson", command=lambda: Statistiques.Pearson(Stock[str(Tab_Data.getcurselection())]))
            Menubar_Data.add_cascade(label="Statistiques", menu=menu1)

            menu2 = Menu(Menubar_Data, tearoff=0)
            menu2.add_command(
                label="Diagramme en bâtons", command=lambda: Graphiques.Diagram_Stick(Stock[str(Tab_Data.getcurselection())]))
            menu2.add_command(label="Courbe", command=lambda: Graphiques.Curves(Stock[str(Tab_Data.getcurselection())]))
            menu2.add_command(
                label="Boite a moustaches", command=lambda: Graphiques.Box_Plot(Stock[str(Tab_Data.getcurselection())]))
            menu2.add_command(label="DotPlot", command=lambda: Graphiques.Dot_Plot(Stock[str(Tab_Data.getcurselection())]))
            menu2.add_command(label="Histogram", command=lambda: Graphiques.Histogram(Stock[str(Tab_Data.getcurselection())]))
            Menubar_Data.add_cascade(label="Graphiques", menu=menu2)

            W_Data.config(menu=Menubar_Data)

            # Buttons Exit W_Data (Data Window)
            Butt_Quit = Button(
                W_Data, text="Fermer", command=Exit_Data_Display)
            Butt_Quit.pack(side=RIGHT)

            # Add to the latex file
            Butt_Pdf = Button(
                W_Data, text="Ajouter au PDF",
                command=lambda: Reporting.Insert_PDF(1, Stock[str(Tab_Data.getcurselection())]))
            Butt_Pdf.pack(side=RIGHT)

        else:

            # New Tab creation happens when Data window already exist
            Tab = Tab_Data.add(Name_Tab_Data)
            Tab_Data.selectpage(Name_Tab_Data)

            # Update the number of the Tab in the List_Tab_Name list
            List_Tab_Name.append(Name_Tab_Data)

            # Creation of the area to display datas
            Frame_Data = Frame(Tab)
            Frame_Data.pack()
            Frame_Data.dataCols = data[1]
            Frame_Data.tree = ttk.Treeview(
                Frame_Data, columns=Frame_Data.dataCols, show='headings')

            # Scrollbars
            xsb = ttk.Scrollbar(
                Frame_Data, orient=HORIZONTAL, command=Frame_Data.tree.xview)
            xsb.pack(side=BOTTOM, fill=X)
            ysb = ttk.Scrollbar(
                Frame_Data, orient=VERTICAL, command=Frame_Data.tree.yview)
            ysb.pack(side=RIGHT, fill=Y)
            Frame_Data.tree.pack()
            Frame_Data.tree['yscroll'] = ysb.set
            Frame_Data.tree['xscroll'] = xsb.set
            Frame_Data.tree.pack()
            Frame_Data.tree['yscroll'] = ysb.set
            Frame_Data.tree['xscroll'] = xsb.set

            # Displaying datas
            for c in Frame_Data.dataCols:
                Frame_Data.tree.heading(c, text=c.title())

            for item in data[0]:
                Frame_Data.tree.insert('', 'end', values=item)
            libnDat.Log(("Query sent : " + query))

            Tab_Data.setnaturalsize()

    else:

        # In case the query send back no data
        showerror("Alerte", "Impossible de se connecter à la base")
        libnDat.Log("Query NOT sent")


# Save query in order to use it later
def Seriz_Rq(Name_Rq):

    # Check if the name of the new query does already exist
    # if yes, pop-up a new window to get a new name for the query
    if Name_Rq in DB_Rq.keys():
        showerror("Alerte", "Nom de requête déjà utilisé")
        W_Name_Rq()

    # Check if the new query has a proper name aka length != 0
    elif (len(Name_Rq) == 0):
        showerror("Alerte", "Veuillez entrer un nom de requête")
        W_Name_Rq()

    # Update flat file containing previously saved queries
    else:
        DB_Rq[Name_Rq] = Rq.get("1.0", END).encode('utf8')
        Label_Error_Txt.set("Requête enregistrée...")
        libnDat.Log(("Query saved : \"" + Name_Rq + "\" : " + DB_Rq[Name_Rq]))


# Delete a query
def Del_Rq():
    try:
        del DB_Rq[List_Rq.getvalue()[0]]
        List_Rq.setlist(DB_Rq)
    except IndexError:
        pass


# Pop-up a new window to add a name and save new query
def W_Name_Rq():

    # Catch the new query's name, update the list_Rq (displays saved
    # queries list)
    def Add_Name_Rq():

        Name_Rq = Entry_Name_Rq.get()
        Seriz_Rq(Name_Rq)
        List_Rq.setlist(DB_Rq)
        W_Entry.destroy()

    # New window
    W_Entry = Toplevel()
    label_Name_Rq = Label(W_Entry, text='Entrez le nom de la requete')
    label_Name_Rq.grid(row=0, column=0)

    Entry_Name_Rq = Entry(W_Entry, width=20)
    Entry_Name_Rq.grid(row=1, column=0)
    Entry_Name_Rq.bind("<Return>", Add_Name_Rq)

    Butt_Valid_Nam = Button(
        W_Entry, text='Ok', relief=GROOVE,
        command=Add_Name_Rq)
    Butt_Valid_Nam.grid(row=1, column=1)


# Catch saved query on click and send it to the query field
def Click_Rq_Insert():
    try:
        # First delete query field occupation
        Rq.delete("1.0", END)
        Rq.insert(INSERT, DB_Rq[List_Rq.getvalue()[0]])
    except IndexError:
        showerror("Alerte", "Aucune requête sélectionnée")


# Function to send on click the query
def Click_Rq_Valid():
    query = Rq.get("1.0", END)
    Rq.tag_add(SEL, "1.0", END)

    # Check the presence of query
    if len(query) == 1:
        Label_Error_Txt.set("Requête non-envoyée : Champs requête vide")
    else:
        Send_Data(query, username, pswd)


# Function to check if there is a query to save then send it to save
def Click_Rq_Save():
    if len(Rq.get("1.0", END)) != 1:
        W_Name_Rq()
    else:
        Label_Error_Txt.set("Requête non-enregistrée : Champs requête vide")


# Clear the query field
def Click_Rq_Erase():
    Rq.delete("1.0", END)
    Label_Error_Txt.set("Clear")


# Exit function to close the program
def Exit():
    DB_Rq.close()
    PDF_titles.close()
    W_Main.destroy()


# Main Menubar
Menubar_Main = Menu(W_Main)

menu1 = Menu(Menubar_Main, tearoff=0)
menu1.add_command(label="Quitter", command=Exit)
Menubar_Main.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(Menubar_Main, tearoff=0)
menu2.add_command(label="Editer le PDF", command=Reporting.Generate)
Menubar_Main.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(Menubar_Main, tearoff=0)
Menubar_Main.add_cascade(label="Aide", menu=menu3)

W_Main.config(menu=Menubar_Main)

Ico_Save2 = PhotoImage(file='./Images/Icones/Ico_Save2.gif')
Ico_Check2 = PhotoImage(file='./Images/Icones/Ico_Check2.gif')
Ico_Cross2 = PhotoImage(file='./Images/Icones/Ico_Cross2.gif')


# Frames Main Window (W_Main)
Frame_Error = Frame(W_Main, heigh=15)
Frame_Error.pack(side=BOTTOM, fill=BOTH)

Frame_Rq = Frame(W_Main)
Frame_Rq.pack(side=LEFT, fill=Y)

Frame_Butt = Frame(Frame_Rq)
Frame_Butt.pack(side=BOTTOM, fill=X, pady=2)

List_Rq = Pmw.ScrolledListBox(W_Main,
                              items=DB_Rq,
                              labelpos='n',
                              label_text='Requêtes enregistrées',
                              listbox_height=11,
                              selectioncommand=Click_Rq_Insert)

List_Rq.pack()


# What's in the different frames
Label_Error_Txt = StringVar()
Label_Error = Label(Frame_Error,
                    textvariable=Label_Error_Txt, font=("arial", 8))
Label_Error.pack(side=LEFT)
Label_Error_Txt.set("Barre d'information")

Label_Rq = Label(Frame_Rq, text="Requête")
Label_Rq.pack(side=TOP, anchor=N)

Rq = Text(Frame_Rq, heigh=7, width=50, font=("arial", 9))
Rq.pack(side=TOP, padx=3)
Rq.insert(INSERT, "Entrez votre requête")

# Buttons
Butt_Exit = Button(Frame_Error, text="Quitter", relief=FLAT, command=Exit)
Butt_Exit.pack(side=RIGHT, padx=2, pady=2)

Butt_Del = Button(W_Main, text="Supprimer", command=Del_Rq)
Butt_Del.pack(side=BOTTOM, padx=3)

Butt_Rq_Clear = Button(
    Frame_Butt, image=Ico_Cross2, relief=GROOVE, command=Click_Rq_Erase)
Butt_Rq_Clear.pack(side=RIGHT, padx=2)
Bal_Rq_Clear = Pmw.Balloon(Butt_Rq_Clear)
Bal_Rq_Clear.bind(Butt_Rq_Clear, 'Effacer le champ')

Butt_Rq_Save = Button(
    Frame_Butt, image=Ico_Save2, relief=GROOVE, command=Click_Rq_Save)
Butt_Rq_Save.pack(side=RIGHT, padx=2)
Bal_Rq_Save = Pmw.Balloon(Butt_Rq_Save)
Bal_Rq_Save.bind(Butt_Rq_Save, 'Enregistrer la requête')

Butt_Rq_Valid = Button(
    Frame_Butt, image=Ico_Check2, relief=GROOVE, command=Click_Rq_Valid)
Butt_Rq_Valid.pack(side=RIGHT, padx=2)
Bal_Rq_Valid = Pmw.Balloon(Butt_Rq_Valid)
Bal_Rq_Valid.bind(Butt_Rq_Valid, 'Valider la requête')


W_Main.mainloop()