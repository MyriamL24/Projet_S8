#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

'''This module is the first executed file. It permits to display the aim of Stat'nDat's GUI.'''

from Tkinter import *
from tkMessageBox import *
import anydbm
import Pmw
import ttk
import LibnDat
import Graphiques
import Statistiques
import Reporting
import os

username = 'mlopez001006'
pswd = ' '
fichier=open("chemins.txt", "r")

path1 = fichier.readline().rstrip()
if not os.path.exists(path1):
    os.makedirs(path1)

path2 = fichier.readline().rstrip()
if not os.path.exists(path2):
    os.makedirs(path2)

path3 = fichier.readline().rstrip()
if not os.path.exists(path3):
    os.makedirs(path3)

path4 = fichier.readline().rstrip()
# Clearing previous tmp files such as Graphs
files = os.listdir(path1)
for i in range(0, len(files)):
    os.remove(path1 + files[i])
os.remove(path4)

titre = fichier.readline().rstrip()
dimensions = fichier.readline().rstrip()

w_main = Tk()
Pmw.initialise(w_main)

w_main.title(titre)
w_main.geometry(dimensions)
w_main.resizable(width=False, height=True)

requ = fichier.readline().rstrip()
pdftit = fichier.readline().rstrip()
donnstoc = fichier.readline().rstrip()

db_rq = anydbm.open(requ, 'c')
pdf_titles = anydbm.open(pdftit, 'c')
stock = anydbm.open(donnstoc, 'c')

fichier.close()
list_tab_name = []


def Send_Data(query, user, pwd):
    '''Called  by 'click_Rq_valid', this function can send the query to PGSQL and displays then all datas'''

    def Exit_Data_Display():
        '''Close the tab of displayed data'''
        tab_data.delete(Pmw.SELECT)
        if tab_data.index(Pmw.END, forInsert=True) == 0:
            W_Data.destroy()
            list_tab_name[:] = []

    # Catch data into a variable
    data = LibnDat.connexion(query, user, pwd)

    fichier=open("chemins.txt", "r")
    fichier.seek(113)
    path5 = fichier.readline().rstrip()
    fichier.close()

    # Write datas into a dedicated file, each request get one file
    LibnDat.serialize(path5 + str(len(list_tab_name)) + ".pkl", data)

    # Allows to order names of the differents Tab chronologicaly
    Name_Tab_Data = 'Data ' + str(len(list_tab_name))

    # Create a reference with the name of the file linked for each request
    stock[str(Name_Tab_Data)] = path5 + \
        str(len(list_tab_name)) + ".pkl"

    if data:
        if len(list_tab_name) == 0:
            global W_Data, tab_data

            # Creation of the new window
            W_Data = Toplevel()
            W_Data.title("Data")
            W_Data.maxsize(width=550, height=-1)

            # Update the number of the Tab in the list_tab_name list
            list_tab_name.append(Name_Tab_Data)

            # Creation of the Tab widget
            tab_data = Pmw.NoteBook(W_Data)
            tab_data.pack(fill="both", expand=1, padx=10, pady=10)

            # First Tab of the new window
            Tab = tab_data.add(Name_Tab_Data)
            tab_data.tab(Name_Tab_Data).focus_set()

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
            LibnDat.Log(("Query sent : " + query))

            tab_data.setnaturalsize()

            # Creation of Data Menubar
            Menubar_Data = Menu(Frame_Data)

            menu1 = Menu(Menubar_Data, tearoff=0)
            menu1.add_command(label="Shapiro", command=lambda: Statistiques.Shapiro(stock[str(tab_data.getcurselection())]))
            menu1.add_command(label="Student", command=lambda: Statistiques.Student(stock[str(tab_data.getcurselection())]))
            menu1.add_command(
                label="Kruskall-Wallis", command=lambda: Statistiques.Kruskall_wallis(stock[str(tab_data.getcurselection())]))

            menu1.add_command(label="Wilcoxon", command=lambda: Statistiques.Wilcoxon(stock[str(tab_data.getcurselection())]))
            menu1.add_command(label="Pearson", command=lambda: Statistiques.Pearson(stock[str(tab_data.getcurselection())]))
            Menubar_Data.add_cascade(label="Statistiques", menu=menu1)

            menu2 = Menu(Menubar_Data, tearoff=0)
            menu2.add_command(
                label="Diagramme en bâtons", command=lambda: Graphiques.Diagram_Stick(stock[str(tab_data.getcurselection())]))
            menu2.add_command(label="Courbe", command=lambda: Graphiques.Curves(stock[str(tab_data.getcurselection())]))
            menu2.add_command(
                label="Boite a moustaches", command=lambda: Graphiques.Box_Plot(stock[str(tab_data.getcurselection())]))
            menu2.add_command(label="DotPlot", command=lambda: Graphiques.Dot_Plot(stock[str(tab_data.getcurselection())]))
            menu2.add_command(label="Histogram", command=lambda: Graphiques.Histogram(stock[str(tab_data.getcurselection())]))
            Menubar_Data.add_cascade(label="Graphiques", menu=menu2)

            W_Data.config(menu=Menubar_Data)

            # Buttons Exit W_Data (Data Window)
            Butt_Quit = Button(
                W_Data, text="Fermer", command=Exit_Data_Display)
            Butt_Quit.pack(side=RIGHT)

            # Add to the latex file
            Butt_Pdf = Button(
                W_Data, text="Ajouter au PDF",
                command=lambda: Reporting.Insert_PDF(1, stock[str(tab_data.getcurselection())]))
            Butt_Pdf.pack(side=RIGHT)

        else:

            # New Tab creation happens when Data window already exist
            Tab = tab_data.add(Name_Tab_Data)
            tab_data.selectpage(Name_Tab_Data)

            # Update the number of the Tab in the list_tab_name list
            list_tab_name.append(Name_Tab_Data)

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
            LibnDat.Log(("Query sent : " + query))

            tab_data.setnaturalsize()

    else:

        # In case the query send back no data
        showerror("Alerte", "Impossible de se connecter à la base")
        LibnDat.Log("Query NOT sent")


# Save query in order to use it later
def Seriz_Rq(Name_Rq):
    '''Save query in order to use it later'''
    '''Check if the name of the new query does already exist if yes, pop-up a new window to get a new name for the query'''
    # Check if the name of the new query does already exist
    # if yes, pop-up a new window to get a new name for the query
    if Name_Rq in db_rq.keys():
        showerror("Alerte", "Nom de requête déjà utilisé")
        W_Name_Rq()

    # Check if the new query has a proper name aka length != 0
    elif (len(Name_Rq) == 0):
        showerror("Alerte", "Veuillez entrer un nom de requête")
        W_Name_Rq()

    # Update flat file containing previously saved queries
    else:
        db_rq[Name_Rq] = Rq.get("1.0", END).encode('utf8')
        Label_Error_Txt.set("Requête enregistrée...")
        LibnDat.Log(("Query saved : \"" + Name_Rq + "\" : " + db_rq[Name_Rq]))


# Delete a query
def Del_Rq():
    '''Delete selected query out from the combobox query list'''
    try:
        del db_rq[List_Rq.getvalue()[0]]
        List_Rq.setlist(db_rq)
    except IndexError:
        pass


# Pop-up a new window to add a name and save new query
def W_Name_Rq():
    '''Pop-up a new window to add a name and save new query'''
    # Catch the new query's name, update the list_Rq (displays saved
    # queries list)
    def Add_Name_Rq():
        '''Catch the new query's name, update the list_rq (displays saved queries list)'''
        Name_Rq = Entry_Name_Rq.get()
        Seriz_Rq(Name_Rq)
        List_Rq.setlist(db_rq)
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
    '''Catch saved query on click and send it to the query field'''
    try:
        # First delete query field occupation
        Rq.delete("1.0", END)
        Rq.insert(INSERT, db_rq[List_Rq.getvalue()[0]])
    except IndexError:
        showerror("Alerte", "Aucune requête sélectionnée")


# Function to send on click the query
def Click_Rq_Valid():
    '''Function to send on click the query : Called by validation-button, on main window of GUI, this function calls then 'send_data' who send query to database and gets results'''
    query = Rq.get("1.0", END)
    Rq.tag_add(SEL, "1.0", END)

    # Check the presence of query
    if len(query) == 1:
        Label_Error_Txt.set("Requête non-envoyée : Champs requête vide")
    else:
        Send_Data(query, username, pswd)


# Function to check if there is a query to save then send it to save
def Click_Rq_Save():
    '''Function to check if there is a query to save then send it to save. Adds a new query to the combobox query list'''
    if len(Rq.get("1.0", END)) != 1:
        W_Name_Rq()
    else:
        Label_Error_Txt.set("Requête non-enregistrée : Champs requête vide")


# Clear the query field
def Click_Rq_Erase():
    '''Clear the query field'''
    Rq.delete("1.0", END)
    Label_Error_Txt.set("Clear")


# Exit function to close the program
def Exit():
    '''Exit function to close the program'''
    db_rq.close()
    pdf_titles.close()
    w_main.destroy()


# Main Menubar
menubar_main = Menu(w_main)

menu1 = Menu(menubar_main, tearoff=0)
menu1.add_command(label="Quitter", command=Exit)
menubar_main.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar_main, tearoff=0)
menu2.add_command(label="Editer le PDF", command=Reporting.Generate)
menubar_main.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar_main, tearoff=0)
menu3.add_command(label="Aide", command=LibnDat.display_help)
menubar_main.add_cascade(label="Aide", menu=menu3)

w_main.config(menu=menubar_main)

fichier=open("chemins.txt", "r")

fichier.seek(129)

path6 = fichier.readline().rstrip()
path7 = fichier.readline().rstrip()
path8 = fichier.readline().rstrip()

fichier.close()

Ico_Save2 = PhotoImage(file=path6)
Ico_Check2 = PhotoImage(file=path7)
Ico_Eraser2 = PhotoImage(file=path8)


# Frames Main Window (w_main)
Frame_Error = Frame(w_main, heigh=15)
Frame_Error.pack(side=BOTTOM, fill=BOTH)

Frame_Rq = Frame(w_main)
Frame_Rq.pack(side=LEFT, fill=Y)

Frame_Butt = Frame(Frame_Rq)
Frame_Butt.pack(side=BOTTOM, fill=X, pady=2)

List_Rq = Pmw.ScrolledListBox(w_main,
                              items=db_rq,
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

Butt_Del = Button(w_main, text="Supprimer", command=Del_Rq)
Butt_Del.pack(side=BOTTOM, padx=3)

Butt_Rq_Clear = Button(
    Frame_Butt, image=Ico_Eraser2, relief=GROOVE, command=Click_Rq_Erase)
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


w_main.mainloop()
