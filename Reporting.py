#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

from Tkinter import *
from tkMessageBox import *
import Pmw
import anydbm
import libnDat


PDF_Titles = anydbm.open('PDF_Titles.dbm', 'c')

try:
    Tek_File = open('./Rapport/Rapport.txt', 'r+')
except IOError:
    Tek_File = open('./Rapport/Rapport.txt', 'w')


def Generate():
    os.system("pdflatex -output-directory=./Rapport file.tex")

def W_New_Section(): #case, ref):

    def Add_Section():

        Name_New_Section = str(
                Section_Type_Select.get()) + "{" + New_Section.get() + "}"

        if Name_New_Section in PDF_Titles.keys():
            showerror("Alerte", "Nom déjà utilisé")

        elif (len(Name_New_Section) == 0):
            showerror("Alerte", "Veuillez entrer un nom de section")

        else:
            PDF_Titles[Name_New_Section] = str(
                Section_Type_Select.get()) + "{" + Name_New_Section + "}"
            Section_Select.setlist(PDF_Titles)
            try:
                Section_Select.selectitem(0)
            except IndexError:
                pass
            W_New_Section.destroy()

    W_New_Section = Toplevel()

    Frame_New_Section_PDF = Frame(W_New_Section)
    Frame_New_Section_PDF.pack(side=TOP, fill=Y)

    Sections_Type = (
        '\part',
        '\chapter',
        '\section',
        '\subsection',
        '\subsubsection',
        '\paragraph',
        '\subparagraph')

    New_Section_Group = Pmw.Group(
        Frame_New_Section_PDF,
        tag_text='Nouvelle Section')
    New_Section_Group.pack()

    Section_Type_Select = Pmw.ComboBox(
        New_Section_Group.interior(),
        labelpos=None,
        fliparrow=True,
        selectioncommand=None,
        listheight=110,
        scrolledlist_items=Sections_Type)
    Section_Type_Select.grid(row=0, column=1, pady=2, padx=2)
    Section_Type_Select.selectitem(Sections_Type[0])

    New_Section = Entry(New_Section_Group.interior())
    New_Section.grid(row=0, column=0, pady=2, padx=2)
    New_Section.insert(0, " Titre")
    New_Section.focus_set()
    New_Section.select_range(0, END)

    Butt_Add_Title = Button(
        New_Section_Group.interior(),
        text='Ajouter Section', relief=GROOVE, command=Add_Section)
    Butt_Add_Title.grid(row=1, column=1, sticky=E, pady=2, padx=2)


def Del_Section():
    try:
        del PDF_Titles[Section_Select.get()]
        Section_Select.setlist(PDF_Titles)
        try:
            Section_Select.selectitem(0)
        except IndexError:
            Section_Select.clear()
    except Exception:
        showerror("Alerte", "Rien à supprimer")


def Add_to_PDF(case, ref, start, end):

    if case == 1:
        Add_Data(ref, start, end)

    if case == 2:
        Add_Graph(ref, start, end)

    if case == 3:
        Add_Results(ref, start, end)


def Parse_tex(case, ref):
    Tek_File.seek(0)

    Tek_Var = Tek_File.read()

    try:
        Tek_File.seek(0)
        i = Tek_Var.index(str(Section_Select.get()))

        start = Tek_Var[:i + len(str(Section_Select.get()))]
        end = Tek_Var[i + len(str(Section_Select.get())):]

        Add_to_PDF(case, ref, start, end)
        W_PDF_Main.destroy()

    except ValueError:
        try:
            Tek_File.seek(0)
            i = Tek_Var.index("\end{document}")

            start = Tek_Var[:i-1]
            end = Tek_Var[i-1:]

            Tek_File.write(start + "\n" + str(Section_Select.get()) + end)

            Parse_tex(case, ref)


        except ValueError:
            Tek_File.seek(0, 2)

            Tek_File.write("\end{document}")

            Parse_tex(case, ref)


def Insert_PDF(case, ref):

    if case == 1:
        W_PDF(1, ref)

    if case == 2:
        W_PDF(2, ref)

    if case == 3:
        W_PDF(3, ref)


def Add_Data(ref, start, end):
    Tek_File.seek(0)

    data = libnDat.deserialize(ref)

    Tek_File.write(start + "\n \\begin{tabular}{|")

    for k in range(len(data[1])):
        Tek_File.write("c|")

    Tek_File.write("} \n\t\\hline \n")
    for i in data[1]:
        if i == data[1][-1]:
            Tek_File.write(str(i) + " \\\ \n")
        else:
            Tek_File.write(str(i) + " & ")

    Tek_File.write("\\hline \n")

    for ligne in data[0]:
        for val in ligne:
            if val == ligne[-1]:
                Tek_File.write(str(val) + " \\\ \n")
            else:
                Tek_File.write(str(val) + " & ")

    Tek_File.write("\\hline\n \\end{tabular}\n" + '\n' + Description_Text.get("1.0", END) + '\n' + str(end))


def Add_Graph(ref, start, end):
    Tek_File.seek(0)

    Tek_File.write(
        start + "\n \\begin{figure}[H]" +
        "\n\\centering \n\\includegraphics[scale = 0.6]" +
        "{" + ref + "}\n")
    Tek_File.write("\\end{figure}\n" + Description_Text.get("1.0", END) + "\n" + str(end))


def Add_Results(ref, start, end):
    Tek_File.seek(0)

    Tek_File.write(start + "\n" + ref + "\n" + Description_Text.get("1.0", END) + "\n" + str(end))


def W_PDF(case, ref):

    global Tek_File, Section_Select, Description_Text, W_PDF_Main

    W_PDF_Main = Toplevel()

    Frame_Section_List = Frame(W_PDF_Main)
    Frame_Section_List.pack(side=TOP)

    Section_Select_Group = Pmw.Group(
        Frame_Section_List,
        tag_text='Sections')
    Section_Select_Group.pack()

    Section_Select = Pmw.ComboBox(
        Section_Select_Group.interior(),
        labelpos=None,
        fliparrow=True,
        selectioncommand=None,
        listheight=110,
        scrolledlist_items=PDF_Titles)
    Section_Select.grid(row=0, column=0, pady=2, padx=2)
    Section_Select.focus_set()
    try:
        Section_Select.selectitem(0)
    except IndexError:
        pass

    Butt_Add_Title = Button(
        Section_Select_Group.interior(),
        text='+', relief=GROOVE, justify=CENTER, command=W_New_Section)#(case, ref))
    Butt_Add_Title.config(height=1, width=2)
    Butt_Add_Title.grid(row=0, column=1, sticky=E, pady=2, padx=2)
    Ball_Add_Title = Pmw.Balloon(Butt_Add_Title)
    Ball_Add_Title.bind(Butt_Add_Title, "Ajouter une nouvelle section")

    Butt_Supp_Title = Button(
        Section_Select_Group.interior(),
        text='-', relief=GROOVE, justify=CENTER, command=Del_Section)
    Butt_Supp_Title.config(height=1, width=2)
    Butt_Supp_Title.grid(row=0, column=2, sticky=E, pady=2, padx=2)
    Ball_Supp_Title = Pmw.Balloon(Butt_Supp_Title)
    Ball_Supp_Title.bind(Butt_Supp_Title, "Supprimer une section")

    Frame_Description = Frame(W_PDF_Main)
    Frame_Description.pack(side=TOP)

    Description_Group = Pmw.Group(
        Frame_Description,
        tag_text='Description')
    Description_Group.pack()

    Description_Text = Text(
        Description_Group.interior(),
        height=5,
        width=40,
        font=("arial", 9))
    Description_Text.pack(padx=3, pady=2)

    Frame_Butt_PDF = Frame(W_PDF_Main)
    Frame_Butt_PDF.pack(side=RIGHT)

    Butt_Send_to_PDF = Button(
        Frame_Butt_PDF,
        text='Ajouter au PDF',
        relief=GROOVE,
        command=lambda: Parse_tex(case, ref))
    Butt_Send_to_PDF.pack(side=RIGHT, padx=2, pady=2)