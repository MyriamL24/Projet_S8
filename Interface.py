#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART


from Tkinter import *
from tkMessageBox import *
import Stock
import Pmw


Fn_P = Tk()
Pmw.initialise(Fn_P)

Fn_P.title('Better bet on Bacon\'')
Fn_P.geometry("650x200+50+50")
Fn_P.resizable(width=False, height=False)


Var_Rq = Stock.deserialize("requetes.pkl")

def alert():
    showinfo("alerte", "Bravo!")

def Rq_List():
    fen = Toplevel()
    fen.title = ("Requetes")
    combo = Pmw.ComboBox(fen, labelpos = N,
                         label_text = 'Choisissez la requete',
                         scrolledlist_items = Var_Rq,
                         listheight = 150,
                         selectioncommand = Click_Rq_Insert)
    combo.grid(row = 2, columnspan = 2, padx = 10, pady = 10)

def Click_Rq_Insert(tag):
    Rq.delete("1.0", END)
    Rq.insert(INSERT, Var_Rq[tag])

def Click_Rq_Valid():
	Rq.tag_add(SEL, "1.0", END)
	if len(Rq.get("1.0", END)) == 1:
		Label_Error_Txt.set("Requête non-envoyée : Champs requête vide")
    

def Seriz_Rq(Nam_Rq):
	Var_Rq = Stock.deserialize("requetes.pkl")
	print Var_Rq.keys()
	if Nam_Rq not in Var_Rq.keys() :
		print "Michel is alive"
		Var_Rq[Nam_Rq] = Rq.get("1.0", END)
		Stock.serialize('requetes.pkl', Var_Rq)
		print rVar_Rq
	else :
		showerror("Alerte","Nom de requête déjà utilisé")


def Fn_Nam_Rq():

	def Get_Nam_Rq():
		Nam_Rq=Entry_Nam_Rq.get()
		Fn_Entry.destroy()
		Seriz_Rq(Nam_Rq)
		

	Fn_Entry = Toplevel()
	label_Nam_Rq = Label(Fn_Entry, text='Entrez le nom de la requete')
	label_Nam_Rq.grid(row=0,column=0)
	Entry_Nam_Rq = Entry(Fn_Entry,width=20)
	Entry_Nam_Rq.grid(row=1,column=0)
	Entry_Nam_Rq.bind("<Return>", Get_Nam_Rq)
	Butt_Valid_Nam=Button(Fn_Entry, text='Ok',relief=GROOVE, command=Get_Nam_Rq)
	Butt_Valid_Nam.grid(row=1,column=1)

def Click_Rq_Save():
	if len(Rq.get("1.0", END)) != 1:
		Fn_Nam_Rq()
	else:
	  	Label_Error_Txt.set("Requête non-enregistrée : Champs requête vide")


def Click_Rq_Erase():
    Rq.delete("1.0", END)
    Label_Error_Txt.set("Clear")



# Barre de Menu

menubar = Menu(Fn_P)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouvelle requête...", command=Rq_List)
menu1.add_command(label="Ouvrir requête...", command=alert)
menu1.add_command(label="Enregistrer", command=alert)
menu1.add_command(label="Enregistrer sous...", command=alert)
menu1.add_command(label="Exporter en PDF...", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=Fn_P.destroy)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command=alert)
menu2.add_command(label="Copier", command=alert)
menu2.add_command(label="Coller", command=alert)
menu2.add_command(label="Selectionner tout", command=alert)
menu2.add_separator()
menu2.add_command(label="Ajouter au PDF", command=alert)
menubar.add_cascade(label="Editer", menu=menu2)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command=alert)

menu4 = Menu(menubar, tearoff=0)
menu4.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu4)

Fn_P.config(menu=menubar)

Ico_Save2 = PhotoImage(file='./Images/Ico_Save2.gif')
Ico_Check2 = PhotoImage(file='./Images/Ico_Check2.gif')
Ico_Cross2 = PhotoImage(file='./Images/Ico_Cross2.gif')

Frame_Error = Frame(Fn_P, heigh=15, relief=SUNKEN)
Frame_Error.pack(side=BOTTOM, fill=BOTH)

Label_Error_Txt = StringVar()
Label_Error = Label(Frame_Error, textvariable=Label_Error_Txt)
Label_Error.pack(side=LEFT)
Label_Error_Txt.set("Barre d'information")

Frame_Rq = Frame(Fn_P, bg="red")
Frame_Rq.pack(side=LEFT, fill=Y)

Label_Rq = Label(Frame_Rq, text="Requête")
Label_Rq.pack(side=TOP)

Rq = Text(Frame_Rq, heigh=7, width=50, font=("arial", 9))
Rq.pack(side=TOP)
Rq.insert(INSERT, "Entrez votre requête")

Frame_Butt = Frame(Frame_Rq, bg="green")
Frame_Butt.pack(side=BOTTOM, fill=X, pady=2)

Butt_Rq_Erase = Button(
    Frame_Butt, image=Ico_Cross2, relief=GROOVE, command=Click_Rq_Erase)
Butt_Rq_Erase.pack(side=RIGHT, padx=2)
Bal_Rq_Erase = Pmw.Balloon(Butt_Rq_Erase)
Bal_Rq_Erase.bind(Butt_Rq_Erase, 'Effacer le champs')

Butt_Rq_Save = Button(Frame_Butt, image=Ico_Save2, relief=GROOVE, command=Click_Rq_Save)
Butt_Rq_Save.pack(side=RIGHT,padx=2)#grid(row=0, column=1, pady=2, padx=2)
Bal_Rq_Save = Pmw.Balloon(Butt_Rq_Save)
Bal_Rq_Save.bind(Butt_Rq_Save, 'Enregistrer la requête')

Butt_Valid_Rq = Button(Frame_Butt, image=Ico_Check2, relief=GROOVE, command=Click_Rq_Valid)
Butt_Valid_Rq.pack(side=RIGHT,padx=2)#grid(row=0, column=0, pady=2, padx=2)
Bal_Rq_Valid = Pmw.Balloon(Butt_Valid_Rq)
Bal_Rq_Valid.bind(Butt_Valid_Rq, 'Valider la requête')


Combo = Pmw.ComboBox(Fn_P, dropdown=0, 
	label_text = 'Requêtes z\'enregistrées:',
	labelpos = 'n', scrolledlist_items = Var_Rq, listheight = 20, selectioncommand = Click_Rq_Insert)
Combo.pack()

Butt_Exit = Button(Fn_P, text="Quitter", command=Fn_P.destroy)
Butt_Exit.pack(side=RIGHT)


Fn_P.mainloop()