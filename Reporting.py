# -*- coding: utf-8 -*-
from Tkinter import *
from tkMessageBox import *
import anydbm
import Pmw
import libnDat
import os


def Generate():
    os.system("pdflatex -output-directory=./Rapport file.tex")


def Placement(filename, rajout, descript, TypeObj, tagg):
    print tagg, descript, rajout

# Dans le cas de l'insertion des données : construction d'un tableau
    if TypeObj == 1:
        data = libnDat.deserialize(rajout)
        with open(filename, 'r+') as file:
            text = file.read()
            i = text.index(tagg)
            deb = text[:i + len(tagg)]
            fin = text[i + len(tagg):]
            file.seek(0)
            file.write(deb + "\n \\begin{tabular}{|")
            for i in range(len(data[1])):
                file.write("c|")
            file.write("} \n\t\\hline \n")
            for i in data[1]:
                if i == data[1][-1]:
                    file.write(str(i) + " \\\ \n")
                else:
                    file.write(str(i) + " & ")
            file.write("\\hline \n")
            for ligne in data[0]:
                for val in ligne:
                    if val == ligne[-1]:
                        file.write(str(val) + " \\\ \n")
                    else:
                        file.write(str(val) + " & ")
            file.write("\\hline\n \\end{tabular}\n" + descript + str(fin))

# Dans le cas de l'insertion d'un graphique donc image.gif
    if TypeObj == 3:
        # print 'titi'
        with open(filename, 'r+') as file:
            # print 'toto'
            text = file.read()
            i = text.index(tagg)
            deb = text[:i + len(tagg)]
            fin = text[i + len(tagg):]
            file.seek(0)
            # print rajout,"WHJZRKAZJL"

            file.write(
                deb + "\n \\begin{figure}[H]",
                "\n\\centering \n\\includegraphics[scale = 0.6]",
                "{" + rajout + "}\n")
            file.write("\\end{figure}\n" + descript + "\n" + str(fin))

# Dans le cas de l'insertion des résultats d'un test statistique, donc
# chaine de caractère simple
    if TypeObj == 2:
        with open(filename, 'r+') as file:
            text = file.read()
            i = text.index(tagg)
            deb = text[:i + len(tagg)]
            fin = text[i + len(tagg):]
            file.seek(0)
            file.write(deb + "\n" + rajout + "\n" + descript + "\n" + str(fin))


def W_Title_Pdf(TypeObj, rajout):

    def Get_Titles():
        Section = str(Section_Pdf.get("1.0", END).encode('utf-8'))
        Descrip = str(Text_Section.get("1.0", END).encode('utf-8'))
        Placement('./Rapport/file.tex', rajout, Descrip, TypeObj, Section)
        # print TypeObj
        W_PDF.destroy()

    def Seriz_Titles(Nam_Title):
        if Nam_Title in List_Title:
            showerror("Alerte", "Nom de titre déjà utilisé")
        elif (Nam_Title == ''):
            showerror("Alerte", "Veuillez entrer un titre")
        else:
            List_Title[Nam_Title] = str(
                Section_Pdf.get("1.0", END).encode('utf8') + "\n")
            libnDat.Log("Titre enregistré :" + Nam_Title)

    def Get_Titles_Plus():
        Nam_Title = Section_Pdf.get("1.0", END).encode('utf8')
        Seriz_Titles(Nam_Title)
        L_Titles.setlist(List_Title)

    def Click_Title_Insert():
        try:
            Section_Pdf.delete("1.0", END)
            Section_Pdf.insert(INSERT, List_Title[L_Titles.getvalue()[0]])
        except IndexError:
            showerror("Alerte", "Aucun emplacement sélectionné")

    W_PDF = Toplevel()
    List_Title = anydbm.open('./Rapport/Sommaire.dbm', 'c')

    Frame_Titles = Frame(W_PDF)
    Frame_Titles.pack(side=LEFT, fill=Y)

    Section_Pdf = Text(Frame_Titles, heigh=2, width=50)
    Section_Pdf.pack(side=TOP, padx=1, pady=3)
    Section_Pdf.insert(INSERT, "Rapport")
    Section_Pdf.focus_set()
    Section_Pdf.tag_add(SEL, "1.0", END)

    Text_Section = Text(Frame_Titles, heigh=6, width=50, font=("arial", 9))
    Text_Section.pack(side=TOP, padx=3, pady=2)

# Text_Section.insert(INSERT, "Entrez votre description")

    Frame_Butt_Valid_Pdf = Frame(W_PDF)
    Frame_Butt_Valid_Pdf.pack(side=BOTTOM)

    Butt_Valid_Pdf = Button(
        Frame_Butt_Valid_Pdf, text='OK', relief=GROOVE, command=Get_Titles)
    Butt_Valid_Pdf.pack(side=RIGHT, pady=2, padx=2)

    Butt_Plus_Title = Button(
        Frame_Butt_Valid_Pdf, text="+", relief=GROOVE, command=Get_Titles_Plus)
    Butt_Plus_Title.pack(side=LEFT, padx=5, pady=2)

    L_Titles = Pmw.ScrolledListBox(W_PDF,
                                   items=List_Title,
                                   labelpos='n',
                                   label_text='Titres enregistrés',
                                   listbox_height=5,
                                   selectioncommand=Click_Title_Insert)
    L_Titles.pack(padx=2, pady=2)


def Insert_PDF(case):
    PDF_Titles = anydbm.open('Stock.dbm', 'r')

    if case == 1:
        data = PDF_Titles['data']
        print data
        W_Title_Pdf(1, data)

    if case == 2:
        result = PDF_Titles['result']
        W_Title_Pdf(2, result)

    if case == 3:
        img = PDF_Titles['img']
        W_Title_Pdf(3, str(img))

    PDF_Titles.close()