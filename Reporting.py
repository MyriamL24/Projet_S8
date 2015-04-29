# -*- coding: utf-8 -*-
from Tkinter import *
from tkMessageBox import *
import anydbm
import Pmw
import Evenement


def Placement(filename, rajout, descript = '', TypeObj, tagg):
        if TypeObj == 1
        print tagg, string 
        with open(filename, 'r+') as file:
            text = file.read()
            i = text.index(tagg)
            file.write(text[:i + len(tagg)] + "\n" + string + text[i + len(tagg):])


def W_Title_Pdf(TypeObj):    

    def Get_Titles():
            Section = str(Section_Pdf.get("1.0",END))
            Descrip= str(Text_Section.get("1.0",END))
            Placement('file.tex', Descrip, TypeObj, Section)
            W_Entry.destroy()

    def Seriz_Titles(Nam_Title):
            if Nam_Title in List_Title:
                showerror("Alerte","Nom de titre déjà utilisé")
            elif (Nam_Title == ''):
                showerror("Alerte","Veuillez entrer un titre")                         
            else:
                List_Title[Nam_Title] = Section_Pdf.get("1.0", END).encode('utf8')
                Evenement.Log(("Titre enregistré :"+ Nam_Title+ ":" + List_Title[Nam_Title]))

    def Get_Titles_Plus():     
            Nam_Title = Section_Pdf.get("1.0", END).encode('utf8')                        
            Seriz_Titles (Nam_Title)
            L_Titles.setlist(List_Title)
            """if Nam_Title not in List_Title:
                List_Title.append(Nam_Title)
                L_Titles.setlist(List_Title)"""

    W_Entry=Toplevel()
    List_Title=anydbm.open('sommairePDF.dbm', 'c')

    Frame_Titles = Frame(W_Entry, bg="gray")
    Frame_Titles.pack(side=LEFT, fill=Y)

    Section_Pdf=Text(Frame_Titles, heigh=2, width=55) 
    Section_Pdf.pack(side=TOP, padx=1, pady=3)
    Section_Pdf.insert(INSERT, "A quel emplacement voulez-vous insérer votre objet ?")

    Text_Section=Text(Frame_Titles, heigh=6, width=70, font=("arial",9))
    Text_Section.pack(side=TOP,padx=1 )
    Text_Section.insert(INSERT, "Entrez votre description")

    Frame_Butt_Valid_Pdf= Frame(W_Entry) 
    Frame_Butt_Valid_Pdf.pack(side=BOTTOM)

    Butt_Valid_Pdf=Button(Frame_Butt_Valid_Pdf,text='OK', relief=GROOVE, command=Get_Titles)
    Butt_Valid_Pdf.pack(side=RIGHT, pady=2, padx=2)

    Butt_Plus_Title=Button(Frame_Butt_Valid_Pdf, text="+", relief=GROOVE, command=Get_Titles_Plus)
    Butt_Plus_Title.pack(side=LEFT, padx=5, pady=2)

    L_Titles=Pmw.ScrolledListBox(W_Entry,      
                        items=List_Title,
                        labelpos='n',
                        label_text='Titres enregistrés',
                        listbox_height=5)
    L_Titles.pack()"""