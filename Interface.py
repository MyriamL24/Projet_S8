#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART


from Tkinter import *
from tkMessageBox import *
import anydbm
import base64
import Pmw
import time
import ttk
import libnDat
import Graphiques
import Statistiques
import Reporting

username = 'mlopez001006'
pswd = base64.b64encode('')

W_P = Tk()
Pmw.initialise(W_P)

W_P.title('Better bet on Bacon\'')
W_P.geometry("550x250+50+50")
W_P.resizable(width=False, height=True)


db_Rq = anydbm.open('Requetes.dbm', 'c')


# Fonction alert : fonction qui sert de palliatif avant implémentation finale
def alert():
    showinfo("alerte", "Bravo!")


def Log(info):
    log = open("Log.txt", "a")
    Date = time.strftime('%d/%m/%y %H:%M', time.localtime())
    log.write(Date + ' : ' + info+'\n')
    log.close()


# def Login():

#     def Valid_Login(*w):
#         username = Entry_Nam_User.get()
#         pswd = base64.b64encode(Entry_Pswd.get())
#         if len(username) == 0:
#             showerror("Alerte", "Entrez vos identifiants")
#             Log("Login Error")
#         else:
#             Log("Login "+username)
#             Send_Dat(), username, pswd)
#             W_Login.destroy()

#     W_Login = Toplevel()
#     W_Login.title("Connexion")

#     label_Nam_User = Label(W_Login, text='Username ')
#     label_Nam_User.grid(row=0, column=0)
#     Entry_Nam_User = Entry(W_Login, width=20)
#     Entry_Nam_User.grid(row=0, column=1)

#     label_Pswd = Label(W_Login, text='Password ')
#     label_Pswd.grid(row=1, column=0)
#     Entry_Pswd = Entry(W_Login, width=20, show='*')
#     Entry_Pswd.grid(row=1, column=1)

#     Entry_Pswd.bind("<Return>", Valid_Login)

#     Butt_Valid_Nam = Button(
#         W_Login, text='Ok', relief=GROOVE, command=Valid_Login)
#     Butt_Valid_Nam.grid(row=1, column=2)


def Send_Dat(query, user, pwd):
        data = libnDat.connexion(query, user, pwd)
        libnDat.serialize("data.pkl", data)

        if data:
            # Création d'une fenêtre tkinter
            W_Data = Toplevel()
            W_Data.title("Data")
            W_Data.geometry("550x260+50+50")


            Frame_Data = Frame(W_Data)
            Frame_Data.pack()
            Frame_Data.dataCols = data[1]
            Frame_Data.tree = ttk.Treeview(Frame_Data, columns=Frame_Data.dataCols, show='headings')

            #Scrollbars
            xsb = ttk.Scrollbar(Frame_Data,orient=HORIZONTAL, command=Frame_Data.tree.xview)
            xsb.pack(side=BOTTOM, fill=X)
            ysb = ttk.Scrollbar(Frame_Data,orient=VERTICAL, command=Frame_Data.tree.yview)
            ysb.pack(side=RIGHT, fill=Y)

            Frame_Data.tree.pack()
            
            Frame_Data.tree['yscroll'] = ysb.set
            Frame_Data.tree['xscroll'] = xsb.set

            Frame_Data.tree.pack()

            Frame_Data.tree['yscroll'] = ysb.set
            Frame_Data.tree['xscroll'] = xsb.set

            for c in Frame_Data.dataCols:
                Frame_Data.tree.heading(c, text=c.title())

            for item in data[0]:
                Frame_Data.tree.insert('', 'end', values=item)
            Log(("Query sent : "+query))

            menubar = Menu(W_Data)

            menu1 = Menu(menubar, tearoff=0)
            menu1.add_command(label="Shapiro", command=Statistiques.Shapiro)
            menu1.add_command(label="Student", command=Statistiques.Student)
            menu1.add_command(label="Kruskall-Wallis", command=Statistiques.Kruskall_wallis)
            menu1.add_command(label="Wilcoxon", command=Statistiques.Wilcoxon)
            menu1.add_command(label="Corrélation", command=alert)
            menubar.add_cascade(label="Statistiques", menu=menu1)

            menu2 = Menu(menubar, tearoff=0)
            menu2.add_command(label="Diagramme en bâtons", command=Graphiques.diagramme_baton)
            menu2.add_command(label="Courbe", command=Graphiques.courbes)
            menu2.add_command(label="Histogramme", command=alert)
            menu2.add_command(label="Boite a moustaches", command=alert)
            menu2.add_command(label="DotPlot", command=Graphiques.Dot_Plot)
            menubar.add_cascade(label="Graphiques", menu=menu2)

            W_Data.config(menu=menubar)

            Button(W_Data, text="Ajouter au PDF", command=Reporting.Insert_Table()).pack(side = LEFT, fill = X)

        else:
            showerror("Alerte", "Impossible de se connecter à la base")
            Log("Query NOT sent")

def Click_Rq_Insert():
    try:
        Rq.delete("1.0", END)
        Rq.insert(INSERT, db_Rq[List_Rq.getvalue()[0]])
    except IndexError:
        showerror("Alerte", "Aucune requête sélectionnée")


def Click_Rq_Valid():
    query = Rq.get("1.0", END)
    Rq.tag_add(SEL, "1.0", END)
    if len(query) == 1:
        Label_Error_Txt.set("Requête non-envoyée : Champs requête vide")
    else:
        Send_Dat(query, username, pswd)


def Seriz_Rq(Nam_Rq):
    if Nam_Rq in db_Rq.keys():
        showerror("Alerte", "Nom de requête déjà utilisé")
        W_Nam_Rq()
    elif (Nam_Rq == ''):
        showerror("Alerte", "Veuillez entrer un nom de requête")
    else:
        db_Rq[Nam_Rq] = Rq.get("1.0", END).encode('utf8')
        Label_Error_Txt.set("Requête enregistrée...")
        Log(("Query saved : \""+Nam_Rq+"\" : "+db_Rq[Nam_Rq]))


def Del_Rq():
    try:
        del db_Rq[List_Rq.getvalue()[0]]
        List_Rq.setlist(db_Rq)
    except IndexError:
        pass


def W_Nam_Rq():

    def Get_Nam_Rq(*tag):
        Nam_Rq = Entry_Nam_Rq.get()
        Seriz_Rq(Nam_Rq)
        List_Rq.setlist(db_Rq)
        W_Entry.destroy()

    W_Entry = Toplevel()
    label_Nam_Rq = Label(W_Entry, text='Entrez le nom de la requete')
    label_Nam_Rq.grid(row=0, column=0)
    Entry_Nam_Rq = Entry(W_Entry, width=20)
    Entry_Nam_Rq.grid(row=1, column=0)
    Entry_Nam_Rq.bind("<Return>", Get_Nam_Rq)
    Butt_Valid_Nam = Button(
        W_Entry, text='Ok', relief=GROOVE, command=Get_Nam_Rq)
    Butt_Valid_Nam.grid(row=1, column=1)


def Click_Rq_Save():
    if len(Rq.get("1.0", END)) != 1:
        W_Nam_Rq()
    else:
        Label_Error_Txt.set("Requête non-enregistrée : Champs requête vide")


def Click_Rq_Erase():
    Rq.delete("1.0", END)
    Label_Error_Txt.set("Clear")


def Exit():
    db_Rq.close()
    W_P.destroy()

# Barre de Menu

menubar = Menu(W_P)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Ouvrir requête...", command=alert)
menu1.add_command(label="Enregistrer", command=alert)
menu1.add_command(label="Enregistrer sous...", command=alert)
menu1.add_command(label="Exporter en PDF...", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=Exit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command=alert)
menu2.add_command(label="Copier", command=alert)
menu2.add_command(label="Coller", command=alert)
menu2.add_command(label="Selectionner tout", command=alert)
menu2.add_separator()
menu2.add_command(label="Ajouter au PDF", command=alert)
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu3)

W_P.config(menu=menubar)

Ico_Save2 = PhotoImage(file='./Images/Icones/Ico_Save2.gif')
Ico_Check2 = PhotoImage(file='./Images/Icones/Ico_Check2.gif')
Ico_Cross2 = PhotoImage(file='./Images/Icones/Ico_Cross2.gif')

# Frames Fenetre Principale (W_P)

Frame_Error = Frame(W_P, heigh=15, bg="pink")
Frame_Error.pack(side=BOTTOM, fill=BOTH)

Frame_Rq = Frame(W_P, bg="red")
Frame_Rq.pack(side=LEFT,fill=Y)

Frame_Butt = Frame(Frame_Rq, bg="green")
Frame_Butt.pack(side=BOTTOM, fill=X, pady=2)

List_Rq = Pmw.ScrolledListBox(W_P,
                items=db_Rq,
                labelpos='n',
                label_text='Requêtes enregistrées',
                listbox_height = 11,
                selectioncommand=Click_Rq_Insert)

List_Rq.pack()

# Contenu des differentes Frames

Label_Error_Txt = StringVar()
Label_Error = Label(Frame_Error, textvariable=Label_Error_Txt)
Label_Error.pack(side=LEFT)
Label_Error_Txt.set("Barre d'information")

Label_Rq = Label(Frame_Rq, text="Requête")
Label_Rq.pack(side=TOP, anchor=N)

Rq = Text(Frame_Rq, heigh=7, width=50, font=("arial", 9))
Rq.pack(side=TOP, padx=3)
Rq.insert(INSERT, "Entrez votre requête")

Butt_Exit = Button(Frame_Error, text="Quitter", relief=FLAT, command=Exit)
Butt_Exit.pack(side=RIGHT, padx=2, pady=2)

Butt_Del = Button(W_P, text="Supprimer", command=Del_Rq)
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


W_P.mainloop()