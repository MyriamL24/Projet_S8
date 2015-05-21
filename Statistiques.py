# -*- coding: utf-8 -*-

# Ce programme est sous licence GPL : http://www.gnu.org/licenses/gpl-3.0.txt
# Les auteurs sont : Amal DAHMANI, Myriam LOPEZ et Kevin JAMART

from Tkinter import *
from scipy.stats import *
from tkMessageBox import *
import anydbm
import LibnDat
import Reporting
import Pmw

List_Tab_Results = []
Stock = anydbm.open('Stock.dbm', 'c')


# Displaying results in a lovely new window
def Display_results(result):

    def Exit_Results_Display():
        Tab_Results.delete(Pmw.SELECT)
        if Tab_Results.index(Pmw.END, forInsert=True) == 0:
            W_Results.destroy()
            List_Tab_Results[:] = []

    Name_Tab_Results = 'Results ' + str(len(List_Tab_Results))

    Stock[Name_Tab_Results] = result

    if len(List_Tab_Results) == 0:
        global W_Results, Tab_Results

        # Creation of the new window
        W_Results = Toplevel()
        W_Results.title("Results")

        # Update the number of the Tab in the List_Tab_Name list
        List_Tab_Results.append(Name_Tab_Results)

        Tab_Results = Pmw.NoteBook(W_Results)
        Tab_Results.pack(fill="both", expand=1, padx=10, pady=10)

        # First Tab of the new window
        Tab = Tab_Results.add(Name_Tab_Results)
        Tab_Results.tab(Name_Tab_Results).focus_set()

        Title_Results = Pmw.Group(Tab, tag_text='Results')
        Title_Results.pack(fill='both', expand=1, padx=6, pady=6)

        Label_Results = Label(
            Title_Results.interior(), text=result)
        Label_Results.pack(padx=2, pady=2, expand='yes', fill='both')

        Butt_Results_PDF = Button(
            W_Results, text="Ajouter au PDF", command=lambda: Reporting.Insert_PDF(3, Stock[str(Tab_Results.getcurselection())]))
        Butt_Results_PDF.pack(side=LEFT, fill=X)

        Butt_Results_Exit = Button(
            W_Results, text="Fermer", command=Exit_Results_Display)
        Butt_Results_Exit.pack(side=RIGHT, fill=X)

        Tab_Results.setnaturalsize()

    else:

        # Update the number of the Tab in the List_Tab_Name list
        List_Tab_Results.append(Name_Tab_Results)

        # First Tab of the new window
        Tab = Tab_Results.add(Name_Tab_Results)
        Tab_Results.selectpage(Name_Tab_Results)

        Title_Results = Pmw.Group(Tab, tag_text='Results')
        Title_Results.pack(fill='both', expand=1, padx=6, pady=6)

        Label_Results = Label(
            Title_Results.interior(), text=result)
        Label_Results.pack(padx=2, pady=2, expand='yes', fill='both')

        Tab_Results.setnaturalsize()


# Shapiro's test using scipy module
def Shapiro(ref):

    data = LibnDat.deserialize(ref)

    try:
        res = shapiro(data[0])
        # Formating results
        if res[1] >= 0.05:
            result = " Test de Shapiro \n\nLa population suit une loi normale\n W : " + \
                str(res[0]) + "\n p.value : " + str(res[1]) + '\n'
        else:
            result = "Test de Shapiro \n\nLa population ne suit pas une loi normale\n W : " + \
                str(res[0]) + "\n p.value : " + str(res[1]) + '\n'
    except ValueError:
        showerror("Alerte",
            "Test Shapiro impossible :\n\n" \
            "Shapiro, test de normalité d'un echantillon")
        return

    Display_results(result)


# Wilcoxon's test using scipy module IndexError
def Wilcoxon(ref):

    data = LibnDat.deserialize(ref)

    # Ordering datas
    try:
        liste = LibnDat.parse_choix(data, 1, 0)
    except IndexError:
        showerror("Alerte",
            "Test Wilcoxon impossible :\n\n" \
            "Mauvaise selection de données")
        return

    # Test and formating the results
    try:
        res = wilcoxon(liste[0], liste[1])
        result = " Test des rangs signés de Wilcoxon \n\n T : " + \
            str(res[0]) + "\n p.value : " + str(res[1])
    except TypeError:
        showerror("Alerte",
            "Test Wilcoxon impossible :\n\n" \
            "Mauvaise selection de données")
        return

    Display_results(result)


# Students's test using scipy module
def Student(ref):

    data = LibnDat.deserialize(ref)

    # Ordering datas
    try:
        liste = LibnDat.parse_choix(data, 1, 0)
    except Exception:
        showerror("Alerte",
            "Test Student impossible :\n\n" \
            "Mauvaise selection de données")
        return


    # Test and formating the results
    try:
        res = ttest_ind(liste[0], liste[1])
        result = " Test de student \n\n T : " + \
            str(res[0]) + "\n p.value : " + str(res[1])
    except Exception:
        showerror("Alerte",
            "Test Student impossible :\n\n" \
            "Mauvaise selection de données")
        return

    Display_results(result)


# Kruskall_Wallis's test using scipy module
def Kruskall_wallis(ref):

    data = LibnDat.deserialize(ref)

    # Ordering datas
    try:
        donnees = LibnDat.parse_choix(data, len(data[1]) - 1, len(data[1]) - 2)
    except Exception:
        showerror("Alerte",
            "Test Kruskall-Wallis impossible :\n\n" \
            "Mauvaise selection de données")

    # Test and formating the results
    try:
        res = mstats.kruskalwallis(*donnees)
        result = "Test de Kruskall-Wallis \n\n W : " + \
            str(res[0]) + "\n p.value : " + str(res[1])
    except Exception:
        showerror("Alerte",
            "Test Kruskall-Wallis impossible :\n\n" \
            "Mauvaise selection de données")

    Display_results(result)


# Pearson's test using scipy module
def Pearson(ref):

    data = LibnDat.deserialize(ref)

    # Ordering datas
    try:
        liste = LibnDat.parse_choix(data, 1, 0)
    except Exception:
        showerror("Alerte",
            "Test Pearson impossible :\n\n" \
            "Mauvaise selection de données")

    # Test and formating the results
    try:
        result = pearsonr(liste[0], liste[1])
    except Exception:
        showerror("Alerte",
            "Test Pearson impossible :\n\n" \
            "Mauvaise selection de données")

    Display_results(result)
