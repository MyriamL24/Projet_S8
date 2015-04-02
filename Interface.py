#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART


from Tkinter import *
from tkMessageBox import *
import Pmw
import time


Fn_P = Tk()
Pmw.initialise(Fn_P)

Fn_P.title('Better bet on Bacon\'')
Fn_P.geometry("500x400+50+50")
Fn_P.resizable(width=False, height=False)


def alert():
    showinfo("alerte", "Bravo!")


def Click_Rq_Valid():
    if len(Rq.get("1.0", END)) == 1:
        Label_Error_Txt.set("Requête non-envoyée : Champs requête vide")
    else:
        Label_Error_Txt.set(Rq.get("1.0", END))
        Rq.tag_add(SEL, "1.0", END)


def Click_Rq_Erase():
    Rq.delete("1.0", END)
    Label_Error_Txt.set("Clear")


def Click_Rq_Save():
    SaveRq = open("Requete.txt", "a")
    Date = time.strftime('%d/%m/%y %H:%M', time.localtime())
    if len(Rq.get("1.0", END)) != 1:
        try:
            SaveRq.write(Date + '\n' + Rq.get("1.0", END) + '\n')
            Rq.tag_add(SEL, "1.0", END)
            Label_Error_Txt.set("Requête enregistrée...")
        except UnicodeEncodeError:
            Label_Error_Txt.set(
                "Requête non-enregistrée : Champs requête vide")
            Rq.delete("1.0", END)
    else:
        Label_Error_Txt.set(
            "Requête non-enregistrée : Champs requête vide")
    SaveRq.close()


def afficher_log():  # Fonctionne
    Parse = open("Requete.txt", "r")
    ligne = Parse.readlines()
    Parse.close()
    FNK = Toplevel()
    for l in ligne:
        Label(FNK, text=l).pack()


def erase_log():
    log = open("Requete.txt", "w")
    log.write('')
    log.close()


def graph():
    Fn_G = Toplevel()
    Fn_G.title('Cheese is for weak')
    Fn_G.geometry("500x500+50+50")

    Butt_Quit_G = Button(Fn_G, text='Fermer', command=Fn_G.destroy)
    Butt_Quit_G.pack(side=BOTTOM)

    Frame_B = Frame(Fn_G, bg='#d1d6e7')
    Frame_B.pack(side=RIGHT, fill=Y, pady=2)

    Frame_Res = Frame(Fn_G, heigh=250, bg='#ff8259')
    Frame_Res.pack(side=TOP, fill=BOTH, padx=2, pady=2)

    Frame_G = Frame(Fn_G, heigh=250, bg='#468499', relief=SUNKEN)
    Frame_G.pack(side=BOTTOM, fill=BOTH, padx=2, pady=2)

    Butt_Lines = Button(Frame_B, image=Ico_Lines)
    Butt_Lines.grid(row=0, column=0)
    Bal_Lines = Pmw.Balloon(Butt_Lines)
    Bal_Lines.bind(Butt_Lines, 'Graphique : Courbe')

    Butt_Histogramme = Button(Frame_B, image=Ico_Histogramme)
    Butt_Histogramme.grid(row=1, column=0)
    Bal_Histogramme = Pmw.Balloon(Butt_Histogramme)
    Bal_Histogramme.bind(Butt_Histogramme, 'Graphique : Histogramme')

    Butt_Scatter = Button(Frame_B, image=Ico_Scatter)
    Butt_Scatter.grid(row=2, column=0)
    Bal_Scatter = Pmw.Balloon(Butt_Scatter)
    Bal_Scatter.bind(Butt_Scatter, 'Graphique : Nuage de points')

# Barre de Menu

menubar = Menu(Fn_P)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouvelle requête...", command=alert)
menu1.add_command(label="Ouvrir requête...", command=alert)
menu1.add_command(label="Enregistrer", command=alert)
menu1.add_command(label="Enregistrer sous...", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=Fn_P.destroy)
menubar.add_cascade(label="Requete", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command=alert)
menu2.add_command(label="Copier", command=alert)
menu2.add_command(label="Coller", command=alert)
menubar.add_cascade(label="Editer", menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu3)

Fn_P.config(menu=menubar)

# Barre de bouton
Frame_Ico = Frame(Fn_P)
Frame_Ico.pack(side=TOP, fill=X)

Ico_Save = PhotoImage(file='./Images/save.gif')
Ico_Save2 = PhotoImage(file='./Images/save2.gif')
Ico_PDF = PhotoImage(file='./Images/doc_pdf.gif')
Ico_Rq = PhotoImage(file='./Images/Rq.gif')
Ico_Open = PhotoImage(file='./Images/open.gif')
Ico_Nex = PhotoImage(file='./Images/nex.gif')
Ico_Print = PhotoImage(file='./Images/printer.gif')
Ico_Check2 = PhotoImage(file='./Images/tick3.gif')
Ico_Cross = PhotoImage(file='./Images/cross.gif')
Ico_Cross2 = PhotoImage(file='./Images/cross2.gif')
Ico_Up = PhotoImage(file='./Images/Up3.gif')
Ico_Separator = PhotoImage(file='./Images/separator.gif')
Ico_Student = PhotoImage(file='./Images/student.gif')
Ico_Fisher = PhotoImage(file='./Images/fish.gif')
Ico_Kruskall = PhotoImage(file='./Images/kruskall.gif')
Ico_Lines = PhotoImage(file='./Images/Stat.gif')
Ico_Histogramme = PhotoImage(file='./Images/chart_bar.gif')
Ico_Scatter = PhotoImage(file='./Images/chart_bull.gif')

Butt_Nex = Button(Frame_Ico, image=Ico_Nex)
Butt_Nex.grid(row=0, column=0)
Bal_Nex = Pmw.Balloon(Butt_Nex)
Bal_Nex.bind(Butt_Nex, 'Nouvelle Requete')

Butt_Open = Button(Frame_Ico, image=Ico_Open)
Butt_Open.grid(row=0, column=1)
Bal_Open = Pmw.Balloon(Butt_Open)
Bal_Open.bind(Butt_Open, 'Ouvrir')

Butt_Save = Button(Frame_Ico, image=Ico_Save)
Butt_Save.grid(row=0, column=2)
Bal_Save = Pmw.Balloon(Butt_Save)
Bal_Save.bind(Butt_Save, 'Sauvegarder')

Butt_Sep = Button(Frame_Ico, image=Ico_Separator, relief=FLAT)
Butt_Sep.grid(row=0, column=3)

Butt_Student = Button(Frame_Ico, image=Ico_Student, command=graph)
Butt_Student.grid(row=0, column=4)
Bal_Student = Pmw.Balloon(Butt_Student)
Bal_Student.bind(Butt_Student, 'Test : Student')

Butt_Fisher = Button(Frame_Ico, image=Ico_Fisher, command=graph)
Butt_Fisher.grid(row=0, column=5)
Bal_Fisher = Pmw.Balloon(Butt_Fisher)
Bal_Fisher.bind(Butt_Fisher, 'Test : Fisher')

Butt_Kruskall = Button(Frame_Ico, image=Ico_Kruskall, command=graph)
Butt_Kruskall.grid(row=0, column=6)
Bal_Kruskall = Pmw.Balloon(Butt_Kruskall)
Bal_Kruskall.bind(Butt_Kruskall, 'Test : Kruskall Wallis')

Butt_Sep2 = Button(Frame_Ico, image=Ico_Separator, relief=FLAT)
Butt_Sep2.grid(row=0, column=7)

Butt_Lines = Button(Frame_Ico, image=Ico_Lines, command=graph)
Butt_Lines.grid(row=0, column=8)
Bal_Lines = Pmw.Balloon(Butt_Lines)
Bal_Lines.bind(Butt_Lines, 'Graphique : Courbe')

Butt_Histogramme = Button(
    Frame_Ico, image=Ico_Histogramme, command=graph)
Butt_Histogramme.grid(row=0, column=9)
Bal_Histogramme = Pmw.Balloon(Butt_Histogramme)
Bal_Histogramme.bind(Butt_Histogramme, 'Graphique : Histogramme')

Butt_Scatter = Button(Frame_Ico, image=Ico_Scatter, command=graph)
Butt_Scatter.grid(row=0, column=10)
Bal_Scatter = Pmw.Balloon(Butt_Scatter)
Bal_Scatter.bind(Butt_Scatter, 'Graphique : Nuage de points')

Butt_Sep3 = Button(Frame_Ico, image=Ico_Separator, relief=FLAT)
Butt_Sep3.grid(row=0, column=11)

Butt_Log = Button(Frame_Ico, image=Ico_Rq, command=afficher_log)
Butt_Log.grid(row=0, column=12, sticky=W)

Butt_Log_Erase = Button(Frame_Ico, image=Ico_Cross, command=erase_log)
Butt_Log_Erase.grid(row=0, column=13, sticky=W)

# Bouton Quitter Fenetre principale
Butt_Exit = Button(Fn_P, text="Quitter", command=Fn_P.destroy)
Butt_Exit.pack(side=BOTTOM, pady=2)

# Fenetre Requete
Frame_Rq = Frame(Fn_P)
Frame_Rq.pack(side=TOP, pady=5, fill=BOTH)

Label_Rq = Label(Frame_Rq, text="Requête")
Label_Rq.pack(side=LEFT)

Rq = Text(Frame_Rq, heigh=5, width=50, font=("arial", 9))
Rq.pack(side=LEFT)
Rq.insert(INSERT, "Entrez votre requête")

Frame_Error = Frame(Fn_P, bg="#a7c8db", heigh=25, relief=RAISED)
Frame_Error.pack(side=TOP, fill=BOTH)

Label_Error_Txt = StringVar()
Label_Error = Label(Frame_Error, textvariable=Label_Error_Txt)
Label_Error.pack()
Label_Error_Txt.set("Barre d'information")

Frame_Rq_Butt = Frame(Frame_Rq)
Frame_Rq_Butt.pack(side=BOTTOM, padx=5)

Butt_Rq_Valid = Button(
    Frame_Rq_Butt, image=Ico_Check2, relief=GROOVE, command=Click_Rq_Valid)
Butt_Rq_Valid.pack(side=LEFT)
Bal_Rq_Valid = Pmw.Balloon(Butt_Rq_Valid)
Bal_Rq_Valid.bind(Butt_Rq_Valid, 'Valider')

Butt_Rq_Erase = Button(
    Frame_Rq_Butt, image=Ico_Cross2, relief=GROOVE, command=Click_Rq_Erase)
Butt_Rq_Erase.pack(side=LEFT)
Bal_Rq_Erase = Pmw.Balloon(Butt_Rq_Erase)
Bal_Rq_Erase.bind(Butt_Rq_Erase, 'Effacer')

Butt_Rq_Save = Button(
    Frame_Rq_Butt, image=Ico_Save2, relief=GROOVE, command=Click_Rq_Save)
Butt_Rq_Save.pack(side=LEFT)
Bal_Rq_Save = Pmw.Balloon(Butt_Rq_Valid)
Bal_Rq_Save.bind(Butt_Rq_Save, 'Enregistrer')

# Fenetre Resultat de Requete

Frame_Res = Frame(Fn_P, bd=1, relief=SUNKEN)
Frame_Res.pack(side=BOTTOM, pady=5)

Label_Res = Label(Frame_Res, text="Résultat")
Label_Res.pack(side=TOP, pady=2)

Frame_Res_Canvas = Canvas(Frame_Res, width=440)
Frame_Res_Canvas.pack(fill=Y)

Fn_P.mainloop()
