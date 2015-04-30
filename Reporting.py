# -*- coding: utf-8 -*-
from Tkinter import *
from tkMessageBox import *
import anydbm
import Pmw
import libnDat


def Placement(filename, rajout, descript, TypeObj, tagg):
    print tagg, descript

    # Dans le cas de l'insertion des données : construction d'un tableau
    if TypeObj == 1 :
        data = rajout
        with open(filename, 'r+') as file:
            text = file.read()
            i = text.index(tagg)
            deb = text[:i + len(tagg)]
            fin = text[i + len(tagg):]
            file.write(deb + "\n \\begin{tabular}{|")
            for i in range(len(data[1])):
                file.write("c|")
            file.write("} \n\t\\hline \n")
            for i in data[1]:
                if i == data[1][len(data)-1]:
                    file.write(str(i) +" \\\ \n")
                else: 
                    file.write(str(i) + " & ")
            file.write("\\hline \n")
            for ligne in data[0]:
                for val in ligne :
                    if val == ligne[len(ligne)-1]:
                        file.write(str(val) +" \\\ \n")
                    else :
                        file.write(str(val) + " & ")
            file.write("\\hline\n \\end{tabular}\n" + descript + str(fin))
        
# Dans le cas de l'insertion d'un graphique donc image.gif
    if TypeObj == 2 :
        with open(filename, 'r+') as file:
            text = file.read()
            i = text.index(tagg)
            deb = text[:i + len(tagg)]
            fin = text[i + len(tagg):]  

            #file.      

            file.write(deb + "\n \\begin{figure}[H] \n\\centering \n\\includegraphics[scale = 0.6]{rajout}\n")
            file.write("\\end{figure}\n" + descript + "\n" + str(fin))

# Dans le cas de l'insertion des résultats d'un test statistique, donc chaine de caractère simple
    if TypeObj == 3 :
        with open(filename, 'r+') as file:
            text = file.read()
            i = text.index(tagg)
            deb = text[:i + len(tagg)]
            fin = text[i + len(tagg):]
            file.write(deb + "\n" + rajout + "\n" + descript + "\n" +str(fin))

def W_Title_Pdf(TypeObj, rajout):   

    def Get_Titles():
            Section = str(Section_Pdf.get("1.0",END).encode('utf-8'))
            print Section
            Descrip= str(Text_Section.get("1.0",END).encode('utf-8'))
            Placement('file.tex', rajout, Descrip, TypeObj, Section)
            W_Entry.destroy()

    def Seriz_Titles(Nam_Title):
            if Nam_Title in List_Title:
                showerror("Alerte","Nom de titre déjà utilisé")
            elif (Nam_Title == ''):
                showerror("Alerte","Veuillez entrer un titre")                         
            else:
                List_Title[Nam_Title] = Section_Pdf.get("1.0", END).encode('utf8')
                libnDat.Log("Titre enregistré :"+ Nam_Title)

    def Get_Titles_Plus():     
            Nam_Title = Section_Pdf.get("1.0", END).encode('utf8')                        
            Seriz_Titles (Nam_Title)
            L_Titles.setlist(List_Title)

    def Click_Title_Insert():
        try:
            Section_Pdf.delete("1.0", END)
            Section_Pdf.insert(INSERT, List_Title[L_Titles.getvalue()[0]])
        except IndexError:
            showerror("Alerte", "Aucun emplacement sélectionné")

            
    W_Entry=Toplevel()
    List_Title=anydbm.open('sommairePDF.dbm', 'c')

    Frame_Titles = Frame(W_Entry, bg="gray")
    Frame_Titles.pack(side=LEFT, fill=Y)

    Section_Pdf=Text(Frame_Titles, heigh=2, width=55) 
    Section_Pdf.pack(side=TOP, padx=1, pady=3)
    Section_Pdf.insert(INSERT, "A quel emplacement voulez-vous insérer votre objet ?")

    Text_Section=Text(Frame_Titles, heigh=6, width=70, font=("arial",9))
    Text_Section.pack(side=TOP,padx=1 )
    #Text_Section.insert(INSERT, "Entrez votre description")

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
                        listbox_height=5,
                        selectioncommand=Click_Title_Insert)
    L_Titles.pack()


def Insert_Table():
    data = libnDat.deserialize("data.pkl")
    W_Title_Pdf(1, data)

def Insert_Result():
    W_Title_Pdf(2, )

def Insert_Image(nb, image):
    W_Title_Pdf(nb, image)