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

import random

airport = airportFunctions.Airport()

# Variables globales
mainColor = 'white'
buttonColor = "#C0C0C0"


class PrincipalWindow:

    def __init__(self, root):

        # FENÊTRE PRINCIPALE

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
            bg=mainColor)  # création de listBox et de la scrollbar associée
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
            command=lambda: self.addRandomPlane('arrival')).pack(
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
            bg=mainColor)  # création de listBox et de la scrollbar associée
        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor=mainColor,
            orient=VERTICAL)
        self.listBoxDeparture = Listbox(
            listBoxArea,
            height=25,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.listBoxDeparture.bind(
            "<<ListboxSelect>>",
            self.checkPlaneDelete)
        self.listBoxDeparture.bind(
            "<Double-Button-1>",
            self.infoDeparturePlane)
        for plane in airport.departureList: self.listBoxDeparture.insert(END, plane.getID())
        scrollbar.config(command=self.listBoxDeparture.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxDeparture.pack()

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
            command=lambda: self.addRandomPlane('departure')).pack(
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
            bg=mainColor)  # création de listBox et de la scrollbar associée
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
            bg=mainColor)  # création de listBox et de la scrollbar associée
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
        Label(setTime, bg=mainColor, text='min').pack(side=LEFT)
        Button(
            setTime,
            text='Step',
            relief=GROOVE,
            bg=buttonColor,
            command=lambda: self.stepButton(
                self.nbrMin.get())).pack(
            side=RIGHT)

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
        textDep = "Departure: {}".format(
            airport.departureRunway)
        textLabelDep = textDep.ljust(15, ' ')
        self.departureLabel = Label(
            departureFrame,
            bd=3,
            bg=mainColor,
            text=textLabelDep)
        self.departureLabel.pack(side=LEFT)
        Button(
            departureFrame,
            text='-',
            relief=GROOVE,
            width=1,
            bg=buttonColor,
            command=lambda: self.minusRunway("departure")).pack(side=RIGHT)
        Button(
            departureFrame,
            text='+',
            relief=GROOVE,
            width=1,
            bg=buttonColor,
            command=lambda: self.plusRunway("departure")).pack(side=RIGHT)

        arrivalFrame = Frame(mainLabel, bd=6, bg=mainColor)
        arrivalFrame.pack(side=TOP)
        textArr = "Arrival: {}".format(
            airport.arrivalRunway)
        textLabelArr = textArr.ljust(15, ' ')
        self.arrivalLabel = Label(
            arrivalFrame,
            bd=3,
            bg=mainColor,
            text=textLabelArr)
        self.arrivalLabel.pack(side=LEFT)
        Button(
            arrivalFrame,
            text='-',
            relief=GROOVE,
            width=1,
            bg=buttonColor,
            command=lambda: self.minusRunway("arrival")).pack(side=RIGHT)
        Button(
            arrivalFrame,
            text='+',
            relief=GROOVE,
            width=1,
            bg=buttonColor,
            command=lambda: self.plusRunway("arrival")).pack(side=RIGHT)

        mixteFrame = Frame(mainLabel, bd=6, bg=mainColor)
        mixteFrame.pack(side=TOP)
        textMix = "Mixte: {}".format(airport.mixteRunway)
        textLabelMix = textMix.ljust(15, ' ')
        self.mixteLabel = Label(
            mixteFrame,
            bd=3,
            bg=mainColor,
            text=textLabelMix)
        self.mixteLabel.pack(side=LEFT)
        Button(
            mixteFrame,
            text='-',
            relief=GROOVE,
            width=1,
            bg=buttonColor,
            command=lambda: self.minusRunway("mixte")).pack(side=RIGHT)
        Button(
            mixteFrame,
            text='+',
            relief=GROOVE,
            width=1,
            bg=buttonColor,
            command=lambda: self.plusRunway("mixte")).pack(side=RIGHT)



    # FONCTIONS


    # Plane
    def addPlane(self, planeList):
        '''
        fenêtre demandant les informations de l'avion à ajouter
        valable pour les départs et les arrivées
        '''
        self.addWindow = Toplevel(bg=mainColor)
        self.addWindow.title("Add Plane")

        addFrame = Frame(
            self.addWindow,
            bd=15,
            bg=mainColor)  # frame principale
        addFrame.pack()

        Label(
            addFrame,
            bd=4,
            bg=mainColor,
            text='Airline').grid(
            row=0,
            column=0)
        airline = Menubutton(
            addFrame,
            text="Airline",
            bd=2,
            bg=mainColor,
            relief=RAISED,
            width=13)
        airline.grid(row=0, column=1)

        Label(
            addFrame,
            bd=4,
            bg=mainColor,
            text='Model').grid(
            row=1, column=0)
        modelChoice = Menubutton(
            addFrame,
            text="Model",
            bd=2,
            bg=mainColor,
            relief=RAISED,
            width=13)
        modelChoice.grid(row=1, column=1)
        modelChoice.menu = Menu(modelChoice, tearoff=0)
        modelChoice["menu"]  =  modelChoice.menu
        modelChoice.grid()

        for model in airport.modelList:
            print(model)
            modelVar = model
            modelChoice.add_checkbutton(label=model.getName, variable=modelVar)



        Label(addFrame, bd=4, bg=mainColor, text='ID').grid(row=2, column=0)
        IDnumber = Entry(
            addFrame,
            bd=2,
            bg=mainColor,
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=13)
        IDnumber.grid(row=2, column=1)
        
        Label(
            addFrame,
            bd=4,
            bg=mainColor,
            text='Passengers').grid(
            row=3,
            column=0)
        passengers = Entry(
            addFrame,
            bd=2,
            bg=mainColor,
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=13)
        passengers.grid(row=3, column=1)

        if planeList == "departure":
            Label(
                addFrame,
                bd=4,
                bg=mainColor,
                text='Time').grid(
                row=5,
                column=0)
            timeFrame = Frame(
                addFrame,
                bd=4,
                bg=mainColor)  # frame secondaire, contient l'entrée de l'heure
            timeFrame.grid(row=5, column=1)
            heure = Entry(
                timeFrame,
                bd=2,
                bg=mainColor,
                textvariable=int,
                justify=CENTER,
                relief=SUNKEN,
                width=6)
            heure.grid(row=0, column=0)
            minute = Entry(
                timeFrame,
                bd=2,
                bg=mainColor,
                textvariable=int,
                justify=CENTER,
                relief=SUNKEN,
                width=6)
            minute.grid(row=0, column=1)
        
        else:
            heure = None
            minute = None

        Button(
            addFrame,
            text="Add",
            relief=GROOVE,
            bg='#C0C0C0',
            command=lambda: self.getPlane(
                IDletter,
                IDnumber,
                airline,
                passengers,
                heure,
                minute,
                planeList)).grid(
            row=7,
            column=1)

    def getPlane(self, IDletter, IDnumber, company, passengers, heure, min, planeList):
        print("pinky pinky")


    def addRandomPlane(self, planeList):
        '''
        Ajoute un avion aléatoire au départ
        '''
        IDletter = False
        model = False
        if len(airport.airlinesDico) == 0:
            text = "Il n'y a aucune compangie enregistrée, \nveuillez en ajouter une via le bouton 'Company'"
            message = messagebox.showwarning('No airlines', text)
        else:
            listKeyAirlines = airport.airlinesDico.keys()
            IDletter = random.choice(list(listKeyAirlines))

        if len(airport.modelList) == 0:
            text = "Il n'y a aucun modèle enregistré, \nveuillez en ajouter un via le bouton 'Model'"
            message = messagebox.showwarning('No model', text)
        else:
            indice = random.randint(0, len(airport.modelList) - 1)
            model = airport.modelList[indice]

        if IDletter and model:
            if planeList == "departure":
                plane = airport.randomPlane(IDletter, model, airport.departureList)
                self.listBoxDeparture.insert(END, plane.getID())
            else:
                plane = airport.randomPlane(IDletter, model, airport.arrivalList)
                self.listBoxArrivals.insert(END, plane.getID())

            text = "L'avion {} a été ajouté".format(plane.getID())
            message = messagebox.showinfo('Plane Added', text)


    def infoArrivalPlane(self):
        pass
    def infoDeparturePlane(self):
        pass
    def infoHistoryPlane(self):
        pass

    def checkPlaneDelete(self):
        pass
    def deletePlaneButton(self):
        pass

    # Fonctions de modifications des pistes (runways)
    def plusRunway(self, runway):
        '''
        Incrémente d'un la valeur de la piste passée en paramètre 
        '''
        if runway == 'departure':
            airport.departureRunway += 1
            text = "Departure: {}".format(airport.departureRunway)
            textLabel = text.ljust(15, ' ')
            self.departureLabel.configure(text=textLabel)

        elif runway == 'arrival':
            airport.arrivalRunway += 1
            text = "Arrival: {}".format(airport.arrivalRunway)
            textLabel = text.ljust(15, ' ')
            self.arrivalLabel.configure(text=textLabel)

        elif runway == 'mixte':
            airport.mixteRunway += 1
            text = "Mixte: {}".format(airport.mixteRunway)
            textLabel = text.ljust(15, ' ')
            self.mixteLabel.configure(text=textLabel)

    def minusRunway(self, runway):
        '''
        Décrémente d'un la valeur de la piste pasée en paramètre
        '''
        if runway == 'departure':
            airport.departureRunway -= 1
            if airport.departureRunway < 0:
                airport.departureRunway = 0
            text = "Departure: {}".format(airport.departureRunway)
            textLabel = text.ljust(15, ' ')
            self.departureLabel.configure(text=textLabel)

        elif runway == 'arrival':
            airport.arrivalRunway -= 1
            if airport.arrivalRunway < 0:
                airport.arrivalRunway = 0
            text = "Arrival: {}".format(airport.arrivalRunway)
            textLabel = text.ljust(15, ' ')
            self.arrivalLabel.configure(text=textLabel)

        elif runway == 'mixte':
            airport.mixteRunway -= 1
            if airport.mixteRunway < 0:
                airport.mixteRunway = 0
            text = "Mixte: {}".format(airport.mixteRunway)
            textLabel = text.ljust(15, ' ')
            self.mixteLabel.configure(text=textLabel)

 
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

    #Statistiques
    def showStat(self):
        '''
        Affiche les statistiques de l'aéroport
        '''
        statWindow = Toplevel(bg=mainColor)
        statWindow.title("Statistics")

        principal = LabelFrame(
            statWindow,
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

    # Historique des avions
    def showHistory(self):
        '''
        Affiche la liste "history" dans une nouvelle fenêtre
        '''
        historyWindow = Toplevel(bg=mainColor)
        historyWindow.title("History")
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
            bg=mainColor)  # création de listBox et de la scrollbar associée
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

    # Help
    def showHelp(self):
        '''
        Permet d'afficher la fenêtre d'aide du programme
        ''' 
        help = Toplevel(root, bg=mainColor)
        help.title("Help")
        Label(
            help,
            bd=6,
            bg=mainColor,
            text="Bienvenue dans le simulateur de gestion d'aéroport",
            font=tkFont.Font(
                size=9)).pack(
            side=TOP)

        textFile = open("help.txt", "r")
        text = ''
        
        line = textFile.readline()

        while line != '':
            if line[0] != '#':
                text += line
            line = textFile.readline()

        message = Message(
            help,
            text=text,
            bd=5,
            bg=mainColor,
            anchor=CENTER)
        message.pack()

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