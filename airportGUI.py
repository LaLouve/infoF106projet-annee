'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: AirportGUI.py
'''

import airportFunctions
from plane import Plane
from airline import Airline
from model import Model

# outils d'interface graphique
from tkinter import *

# permet la mise en forme des textes des label, boutons, ect. par exemple
# changer la taille et la police d'écriture
import tkinter.font as tkFont
# permet l'affichage de messages d'erreur
from tkinter import messagebox 
# permet de selectionner un fichier pour la sauvegarde/restauration
import tkinter.filedialog as filedialog

from random import randint

airport = airportFunctions.Airport()

# Variables globales
mainColor = "white"
buttonColor = "#C0C0C0"


class PrincipalWindow:

    def __init__(self, root):
        self.root = root

        # désactivation du bouton "del" dans la colone des départs
        # /!\ root.bind("<Button-1>", self.checkPlaneDelete)

        # Menu
        menuBar = Menu(root)

        saveMenu = Menu(menuBar, tearoff=0)
        saveMenu.add_command(label='Save', command=self.saveSystem)
        saveMenu.add_command(label='Load', command=self.loadSystem)

        menuBar.add_cascade(label="Save", menu=saveMenu)

        menuBar.add_command(label="Statistics", command=self.showStat)

        menuBar.add_command(label="History", command=self.showHistory)

        menuBar.add_command(label="Help", command=self.showHelp)
        root.config(menu=menuBar)


        # colonne 1 
        column1 = Frame(root, bd=3, bg=mainColor)
        column1.pack(side=LEFT)
        Label(
            column1,
            bd=7,
            bg=mainColor,
            text="ARRIVALS",
            font=tkFont.Font(
                size=12)).pack()

        listBoxArea = Frame(
            column1,
            bd=8,
            bg=mainColor)  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.listBoxArrivals = Listbox(
            listBoxArea,
            height=25,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.listBoxArrivals.bind("<Double-Button-1>", self.infoArrivalPlane)
        for plane in airport.arrivalList:
            self.listBoxArrivals.insert(END, plane.getID())
        scrollbar.config(command=self.listBoxArrivals.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxArrivals.pack()

        Button(
            column1,
            text="Add",
            relief=GROOVE,
            bg=buttonColor,
            command=lambda: self.addPlane('arrival')).pack(
            side=LEFT)
        Button(
            column1,
            text="Add Random",
            relief=GROOVE,
            bg=buttonColor,
            command=self.addArrivalRandom).pack(
            side=LEFT)


        # colonne 2 
        column2 = Frame(root, bd=3, bg=mainColor)  # création de la colonne
        column2.pack(side=LEFT)
        Label(
            column2,
            bd=7,
            bg=mainColor,
            text="DEPARTURES",
            font=tkFont.Font(
                size=12)).pack()

        listBoxArea = Frame(
            column2,
            bd=8,
            bg=mainColor)  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor=mainColor,
            orient=VERTICAL)
        self.listBoxAirlines = Listbox(
            listBoxArea,
            height=25,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.listBoxAirlines.bind(
            "<<ListboxSelect>>",
            self.checkPlaneDelete)
        self.listBoxAirlines.bind(
            "<Double-Button-1>",
            self.infoDeparturePlane)
        for plane in airport.departureList: self.listBoxAirlines.insert(END, plane.getID())
        scrollbar.config(command=self.listBoxAirlines.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxAirlines.pack()

        Button(
            column2,
            text="Add",
            relief=GROOVE,
            bg=buttonColor,
            command=lambda: self.addPlane('departure')).pack(
            side=LEFT)
        Button(
            column2,
            text="Add Random",
            relief=GROOVE,
            bg=buttonColor,
            command=self.addDepartureRandom).pack(
            side=LEFT)
        self.delPlaneButton = Button(
            column2,
            text="Del",
            relief=GROOVE,
            bg=buttonColor,
            state=DISABLED,
            command=self.deletePlaneButton)
        self.delPlaneButton.pack(side=LEFT)


        # colonne 3
        column3 = Frame(root, bd=6, bg=mainColor)
        column3.pack(side=LEFT)

        # Partie haute de la troisième colonne, contient les compagnies
        column3top = Frame(column3, bg=mainColor)
        column3top.pack(side=TOP)
        Label(
            column3top,
            bd=7,
            bg=mainColor,
            text="AIRLINES",
            font=tkFont.Font(
                size=12)).pack()

        listBoxArea = Frame(
            column3top,
            bd=8,
            bg=mainColor)  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.listBoxAirlines = Listbox(
            listBoxArea,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.listBoxAirlines.bind(
            "<<ListboxSelect>>",
            self.checkAirlineDelete)
        self.listBoxAirlines.bind(
            "<Double-Button-1>",
            self.infoAirline)
        for airlineID in airport.airlinesDico:
            airline = airport.airlinesDico[airlineID] 
            self.listBoxAirlines.insert(END, airline.getName())
        scrollbar.config(command=self.listBoxAirlines.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxAirlines.pack()

        Button(
            column3top,
            text="Add",
            relief=GROOVE,
            bg=buttonColor,
            command=self.addAirline()).pack(side=LEFT)

        self.delAirlineButton = Button(
            column3top,
            text="Del",
            relief=GROOVE,
            bg=buttonColor,
            state=DISABLED,
            command=self.delAirline())
        self.delAirlineButton.pack(side=LEFT)

        # Partie basse de la troisème colonne, contient les modèles
        column3bottom = Frame(column3, bg=mainColor)
        column3bottom.pack(side=TOP)
        Label(
            column3bottom,
            bd=7,
            bg=mainColor,
            text="MODELS",
            font=tkFont.Font(
                size=12)).pack()

        listBoxArea = Frame(
            column3bottom,
            bd=8,
            bg=mainColor)  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor=mainColor,
            orient=VERTICAL)
        self.listBoxModel = Listbox(
            listBoxArea,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.listBoxModel.bind(
            "<<ListboxSelect>>",
            self.checkModelDelete)
        self.listBoxModel.bind(
            "<Double-Button-1>",
            self.infoModel)
        for model in airport.modelList:
            self.listBoxModel.insert(END, model.getName())
        scrollbar.config(command=self.listBoxModel.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxModel.pack()

        Button(
            column3bottom,
            text="Add",
            relief=GROOVE,
            bg=buttonColor,
            command=self.addModel()).pack(side=LEFT)

        self.delModelButton = Button(
            column3bottom,
            text="Del",
            relief=GROOVE,
            bg=buttonColor,
            state=DISABLED,
            command=self.delModel())
        self.delModelButton.pack(side=LEFT)


        # colonne 4 
        column4 = Frame(root, bd=6, bg=mainColor)
        column4.pack()

        # partie haute de la quatrième colonne, contient l'heure et le bouton
        # step
        column4top = Frame(column4, bg=mainColor)
        column4top.pack(side=TOP)
        self.generalTime = self.time(airport.tick)
        self.clock = Label(
            column4top,
            bd=6,
            bg=mainColor,
            text=self.generalTime,
            font=tkFont.Font(
                size=16))
        self.clock.pack(side=TOP)

        setTime = Frame(
            column4top,
            bd=4,
            bg=mainColor)  # entrée du temps et bouton step
        setTime.pack()
        self.nbrMin = Entry(
            setTime,
            bg=mainColor,
            justify=CENTER,
            relief=SUNKEN,
            bd=2,
            width=6)
        self.nbrMin.pack(side=LEFT)
        Label(setTime, bg=mainColor, text='min').pack(side=RIGHT)
        Button(
            column4top,
            text='Step',
            relief=GROOVE,
            width=6,
            bg=buttonColor,
            command=lambda: self.stepButton(
                self.nbrMin.get())).pack(
            side=BOTTOM)

        # partie centrale, permet l'espacement des parties haute et basse
        column4Mid = Frame(column4, height=25, bg=mainColor)
        column4Mid.pack(side=TOP)

        # partie basse de la quatrième colonne, contient les informations
        # des pistes
        column4bottom = Frame(column4, bg=mainColor)
        column4bottom.pack(side=BOTTOM)

        mainLabel = LabelFrame(
            column4bottom,
            bd=4,
            relief=RIDGE,
            bg=mainColor,
            text='Runways',
            font=tkFont.Font(
                size=10))
        mainLabel.pack()

        departureFrame = Frame(mainLabel, bd=6, bg=mainColor)
        departureFrame.pack(side=TOP)
        textDep = "Departure runways: {}".format(
            airport.departureRunway)
        textLabelDep = textDep.ljust(25, ' ')
        self.departureLabel = Label(
            departureFrame,
            bd=3,
            bg=mainColor,
            text=textLabelDep)
        self.departureLabel.pack(side=RIGHT)
        self.departureLabel.bind(
            "<Double-Button-1>",
            self.mod_depRunway_button)

        arrivalFrame = Frame(mainLabel, bd=6, bg=mainColor)
        arrivalFrame.pack(side=TOP)
        textArr = "Arrival runways: {}".format(
            airport.arrivalRunway)
        textLabelArr = textArr.ljust(29, ' ')
        self.arrivalLabel = Label(
            arrivalFrame,
            bd=3,
            bg=mainColor,
            text=textLabelArr)
        self.arrivalLabel.pack(side=RIGHT)
        self.arrivalLabel.bind("<Double-Button-1>", self.mod_arrRunway_button)

        mixteFrame = Frame(mainLabel, bd=6, bg=mainColor)
        mixteFrame.pack(side=TOP)
        textMix = "Mixte runways: {}".format(airport.mixteRunway)
        textLabelMix = textMix.ljust(27, ' ')
        self.mixteLabel = Label(
            mixteFrame,
            bd=3,
            bg=mainColor,
            text=textLabelMix)
        self.mixteLabel.pack(side=RIGHT)
        self.mixteLabel.bind("<Double-Button-1>", self.mod_mixRunway_button)


    def infoArrivalPlane(self):
        pass
    def infoDeparturePlane(self):
        pass
    def infoHistoryPlane(self):
        pass
    def addArrivalRandom(self):
        pass
    def addDepartureRandom(self):
        pass
    def checkPlaneDelete(self):
        pass
    def deletePlaneButton(self):
        pass
    '''
    >>>> mettre tout ça sur deux fonctions une + une -
    >>>> avec le nom de runway en param
    >>>> mettre un bouton + et un - à chaque runway
    >>>> ou deux boutons pour tous et devoir selectionner celle qu'on veut 
    '''
    def mod_depRunway_button(self):
        pass
    def mod_arrRunway_button(self):
        pass
    def mod_mixRunway_button(self):
        pass

    def showHelp(self):
        pass  
    def historyButton(self):
        pass
    def addAirline(self):
        pass
    def delAirline(self):
        pass
    def checkAirlineDelete(self):
        pass
    def infoAirline(self):
        pass
    def addModel(self):
        pass
    def delModel(self):
        pass
    def checkModelDelete(self):
        pass
    def infoModel(self):
        pass

        
    def showStat(self):
        '''
        Affiche les statistiques de l'aéroport
        '''
        self.statWindow = Toplevel(bg=mainColor)

        principal = LabelFrame(
            self.statWindow,
            bd=4,
            relief=RIDGE,
            bg=mainColor,
            text='Statistics',
            font=tkFont.Font(
                size=11))
        principal.pack()

        text = "\n- Nombre total d'avions: {}"\
            "\n\n- Nombre d'avions au décollage\nou ayant décollés: {}"\
            "\n\n- Nombre d'avions à l'atterrissage\nou ayant atterri: {}"\
            "\n\n- Nombre total de passagers: {}"\
            "\n\n- Nombre de crashs: {}"\
            "\n\n- Nombre de morts lors des crashs: {}"\
            "\n\n- Nombre de compagnies: {}"\
            "\n\n- Nombre de modèles d'avions: {}".format(airport.statPlaneGlobal,
                                                          airport.statPlaneDep,
                                                          airport.statPlaneArr,
                                                          airport.statPassengers,
                                                          airport.statCrash,
                                                          airport.statDeath,
                                                          airport.statAirlines,
                                                          airport.statModel)
        message = Message(
            principal,
            text=text,
            bd=5,
            bg=mainColor,
            anchor=CENTER)
        message.pack()

    def showHistory(self):
        '''
        Affiche la liste "history" dans une nouvelle fenêtre
        '''
        historyWindow = Toplevel(bg=mainColor)
        column = Frame(
            historyWindow,
            bd=3,
            bg=mainColor)  # création de la colonne
        column.pack(side=LEFT)
        Label(
            column,
            bd=7,
            bg=mainColor,
            text='History',
            font=tkFont.Font(
                size=12)).pack()

        listBoxArea = Frame(
            column,
            bd=8,
            bg=mainColor)  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.listBoxHistory = Listbox(
            listBoxArea,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.listBoxHistory.bind("<Double-Button-1>", self.infoHistoryPlane)
        for plane in airport.historyList:
            text = (str(plane.getID()).ljust(12, ' ') + str(plane.getStatut()))
            self.listBoxHistory.insert(END, text)
        scrollbar.config(command=self.listBoxHistory.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxHistory.pack()

    # fonction de sauvegarde/restauration
    def saveSystem(self, event=None):
        '''
        Permet de sauvegarder le système
        '''
        fileName = filedialog.asksaveasfilename(
            filetypes=[("Fichier txt", "*.txt"), ("Tous", "*")], initialfile="save.txt", parent=self.root)
        if fileName:
            if airport.saveSystem(fileName):
                messagebox.showinfo("Sauvegarde", "Sauvegarde réussie.")
            else:
                messagebox.showwarning(
                    "Sauvegarde",
                    "Problème pendant la sauvegarde.")

    def loadSystem(self, event=None):
        '''
        Permet de charger une sauvegarde
        '''
        fileName = filedialog.askopenfilename(
            filetypes=[("Fichier txt", "*.txt"), ("Tous", "*")], initialfile="save.txt", parent=self.root)
        if fileName:
            if airport.loadSystem(fileName):
                messagebox.showinfo("Chargement", "Chargement réussit.")
                self.root.destroy()
                root = Tk()
                root.title("Airport Simulator")
                root.configure(background=mainColor)
                root.resizable(width=FALSE, height=FALSE)
                self.__init__(root)
            else:
                messagebox.showwarning(
                    "Chargement",
                    "Problème pendant la chargement.")


    # Fonctions de formatage d'affichage
    def time(self, tick):
        '''
        Afiche le nombre "tick" au format '00h00' 
        '''
        return (str(tick // 60).rjust(2, '0') + "h" + str(tick % 60).rjust(2, '0'))




if __name__ == "__main__":
    root = Tk()
    PrincipalWindow(root)
    root.title("Airport Simulator")
    root.configure(background=mainColor)
    root.resizable(width=FALSE, height=FALSE)
    root.mainloop()