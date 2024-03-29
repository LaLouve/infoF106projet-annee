# -*- coding: utf8 -*-
'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: AirportGUI.py
'''

import airportFunctions
from datetime import datetime
from plane import Plane
from airline import Airline
from model import Model
from day import Day

# outils d'interface graphique
from tkinter import *


# permet la mise en forme des textes des label, boutons, ect. par exemple
# changer la taille et la police d'écriture
import tkinter.font as tkFont

# permet l'affichage de messages d'erreur
from tkinter import messagebox

# permet de selectionner un fichier pour la sauvegarde/restauration
import tkinter.filedialog as filedialog

# Permet d'avoir des menus déroulants
from tkinter import ttk

import random

airport = airportFunctions.Airport()

# Variables globales
mainColor = "white"
buttonColor = "#C0C0C0"


class PrincipalWindow:

    def __init__(self, root):
        '''
        self.wait = temps en milisecondes entre chaque appel de self.step()
        60000 = 1minute

        Pour accelerer la simulation il suffit de changer 60000 par
        1000 (= 1seconde). Dans ce cas l'heure et la date affichées dans
        l'interface ne changent pas, l'heure et le jour sont affichés dans
        le terminal à la place
        '''
        self.wait = 60000
        self.debugMode = False

        # Récupération des valeurs de temps réel
        date = airport.realDay()
        airport.currentDay = airport.dayToObjetDay(date)

        time = airport.realTime()
        airport.tick = airport.timeToTick(time)

        # FENÊTRE PRINCIPALE

        self.root = root

        # Menu
        menuBar = Menu(root)

        saveMenu = Menu(menuBar, tearoff=0)
        saveMenu.add_command(label='Save', command=self.saveSystem)
        saveMenu.add_command(label='Load', command=self.loadSystem)
        saveMenu.add_command(label='Clear', command=self.clearSystem)

        historyMenu = Menu(menuBar, tearoff=0)
        historyMenu.add_command(label="History", command=self.showHistory)
        historyMenu.add_command(label="Log", command=self.showLog)

        menuBar.add_cascade(label="Files", menu=saveMenu)
        menuBar.add_cascade(label="History", menu=historyMenu)

        menuBar.add_command(label="Statistics", command=self.showStat)
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
            height=38,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)

        # désactive les boutons del des autres colones lorsqu'un élément est
        # sélectionné dans celle-ci
        self.listBoxArrivals.bind("<<ListboxSelect>>", self.listBoxSelected)
        # active le double-clic pour obtenir les infos d'un avion
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
            command=lambda: self.addPlane('arrival')).pack(side=LEFT)
        Button(
            column1,
            text="Add Random",
            relief=GROOVE,
            bg=buttonColor,
            command=lambda: self.addRandomPlane("arrival")).pack(
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
        self.listBoxDepartures = Listbox(
            listBoxArea,
            height=38,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)

        # active la sélection à la souris pour supprimer un avion
        self.listBoxDepartures.bind("<<ListboxSelect>>", self.checkPlaneDelete)
        # active le double-clic pour obtenir les infos d'un avion
        self.listBoxDepartures.bind(
            "<Double-Button-1>",
            self.infoDeparturePlane)

        for plane in airport.departureList:
            self.listBoxDepartures.insert(END, plane.getID())

        scrollbar.config(command=self.listBoxDepartures.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxDepartures.pack()

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
            command=lambda: self.addRandomPlane("departure")).pack(
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
            height=16,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)

        # Liste des ID des compangnies, simplifie la sélection dans la listbox
        self.airlinesList = []
        for airlineID in airport.airlinesDico:
            self.airlinesList.append(airlineID)
            airline = airport.airlinesDico[airlineID]
            self.listBoxAirlines.insert(END, airline.getName())

        # active la sélection à la souris pour supprimer une compangnie
        self.listBoxAirlines.bind("<<ListboxSelect>>", self.checkAirlineDelete)
        # active le double clic pour obtenir la liste d'avions d'une compagnie
        self.listBoxAirlines.bind("<Double-Button-1>", self.showInfoAirline)

        scrollbar.config(command=self.listBoxAirlines.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxAirlines.pack()

        Button(
            column3top,
            text="Add",
            relief=GROOVE,
            bg=buttonColor,
            command=self.addAirline).pack(side=LEFT)

        self.delAirlineButton = Button(
            column3top,
            text="Del",
            relief=GROOVE,
            bg=buttonColor,
            state=DISABLED,
            command=self.delAirline)
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
            height=16,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)

        # active la sélection à la souris pour supprimer un modèle
        self.listBoxModel.bind("<<ListboxSelect>>", self.checkModelDelete)
        # active le double-clic pour obtenir les informations d'un modèle
        self.listBoxModel.bind("<Double-Button-1>", self.showInfoModel)

        self.listNameModel = []
        for model in airport.modelList:
            name = model.getName()
            self.listNameModel.append(name)
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
            command=self.addModel).pack(side=LEFT)

        self.delModelButton = Button(
            column3bottom,
            text="Del",
            relief=GROOVE,
            bg=buttonColor,
            state=DISABLED,
            command=self.delModel)
        self.delModelButton.pack(side=LEFT)

        # colonne 4
        column4 = Frame(root, bd=6, width=20, bg=mainColor)
        column4.pack()

        # partie haute de la quatrième colonne, contient l'heure et le bouton
        # step
        column4top = Frame(column4, bg=mainColor)
        column4top.pack(side=TOP)

        generalDay = airport.affDay(airport.currentDay)
        self.affichageDay = Label(
            column4top,
            bd=6,
            bg=mainColor,
            text=generalDay,
            font=tkFont.Font(size=16))
        self.affichageDay.pack(side=TOP)

        generalTime = airport.affTime(airport.tick)
        self.clock = Label(
            column4top,
            bd=6,
            bg=mainColor,
            text=generalTime,
            font=tkFont.Font(size=16))
        self.clock.pack(side=TOP)

        if airport.weatherClear:
            color = "green"
        else:
            color = "red"
        generalMeteo = airport.affMeteo(airport.weatherClear)
        self.affichageMeteo = Label(
            column4top,
            bd=6,
            bg=mainColor,
            fg=color,
            text=generalMeteo,
            font=tkFont.Font(size=12))
        self.affichageMeteo.pack(side=TOP)

        # partie intermédiaire, permet l'espacement des parties haute et
        # centrale
        column4int = Frame(column4, height=10, bg=mainColor)
        column4int.pack(side=TOP)

        # partie centrale de la quatrième colonne, contient les informations
        # des pistes
        column4mid = Frame(column4, bg=mainColor)
        column4mid.pack(side=TOP)

        mainLabel = LabelFrame(
            column4mid,
            bd=4,
            width=20,
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
        self.departureLabel = Label(
            departureFrame,
            bd=3,
            bg=mainColor,
            text=textDep,
            width=10)
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
        textArr = "Arrival:      {}".format(
            airport.arrivalRunway)
        self.arrivalLabel = Label(
            arrivalFrame,
            bd=3,
            bg=mainColor,
            text=textArr,
            width=10)
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
        textMix = "Mixte:       {}".format(airport.mixteRunway)
        self.mixteLabel = Label(
            mixteFrame,
            bd=3,
            bg=mainColor,
            text=textMix,
            width=10)
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

        # partie intermédiaire, permet l'espacement des parties haute et basse
        column4int2 = Frame(column4, height=10, bg=mainColor)
        column4int2.pack(side=TOP)

        # Partie basse, affiche les notifiactions du programmes
        self.column4bottom = Frame(column4, bg=mainColor)
        self.column4bottom.pack(side=BOTTOM)

        self.notifFrame = LabelFrame(
            self.column4bottom,
            bd=4,
            width=20,
            relief=RIDGE,
            bg=mainColor,
            text='Notifications',
            font=tkFont.Font(size=10))
        self.notifFrame.pack()

        self.notifList = []  # Liste de toutes les notifications
        self.notifDisplayList = [
            '',
            '',
            '',
            '',
            '']  # Liste des notif affichées
        self.textColor = 'black'
        self.textColorFirst = 'green'
        self.listSize = 5

        self.displayNotif()

        self.waitStep(self.root)

    # FONCTIONS
    # Plane
    def addPlane(self, planeList):
        '''
        fenêtre demandant les informations de l'avion à ajouter
        valable pour les départs et les arrivées
        '''
        listBox = None

        self.addPlaneWindow = Toplevel(bg=mainColor)
        self.addPlaneWindow.resizable(width=FALSE, height=FALSE)
        self.addPlaneWindow.title("Add Plane")

        Label(
            self.addPlaneWindow,
            bd=7,
            bg=mainColor,
            text="ADD PLANE",
            font=tkFont.Font(
                size=12)).pack(side=TOP)

        # Choix de la compagnie
        airlineFrame = Frame(self.addPlaneWindow,
                             bd=4,
                             bg=mainColor)
        airlineFrame.pack()

        Label(airlineFrame,
              bd=4,
              bg=mainColor,
              text='Airline ').pack(side=LEFT)

        airlineID = ttk.Combobox(
            airlineFrame,
            values=self.airlinesList,
            width=13,
            state="readonly")
        airlineID.configure(background=mainColor)
        airlineID.pack(side=RIGHT)

        # Choix du modèle
        modelFrame = Frame(self.addPlaneWindow,
                           bd=4,
                           bg=mainColor)
        modelFrame.pack()

        Label(modelFrame,
              bd=4,
              bg=mainColor,
              text='Model ').pack(side=LEFT)

        modelName = ttk.Combobox(
            modelFrame,
            values=self.listNameModel,
            width=13,
            state="readonly")
        modelName.configure(background=mainColor)
        modelName.pack(side=RIGHT)

        # Entrèe de l'ID
        IDframe = Frame(self.addPlaneWindow,
                        bd=4,
                        bg=mainColor)
        IDframe.pack()

        Label(IDframe,
              bd=4,
              bg=mainColor,
              text="ID (4 digits)").pack(side=LEFT)

        IDnumber = Entry(IDframe,
                         bd=2,
                         bg=mainColor,
                         textvariable=int,
                         justify=CENTER,
                         relief=SUNKEN,
                         width=10)
        IDnumber.delete(0, 100)
        IDnumber.pack(side=RIGHT)

        # Entrée du nombre de passagers
        passengerFrame = Frame(self.addPlaneWindow,
                               bd=4,
                               bg=mainColor)
        passengerFrame.pack()

        Label(passengerFrame,
              bd=4,
              bg=mainColor,
              text="Passengers ").pack(side=LEFT)
        passengers = Entry(passengerFrame,
                           bd=2,
                           bg=mainColor,
                           textvariable=int,
                           justify=CENTER,
                           relief=SUNKEN,
                           width=10)
        passengers.delete(0, 100)
        passengers.pack(side=RIGHT)

        if planeList == "departure":
            dateFrame = Frame(self.addPlaneWindow,
                              bd=4,
                              bg=mainColor)
            dateFrame.pack()

            Label(dateFrame,
                  bd=4,
                  bg=mainColor,
                  text='Date').pack(side=LEFT)

            dayList = []
            for i in range(1, 32, 1):
                dayList.append(i)
            day = ttk.Combobox(
                dateFrame,
                values=dayList,
                width=3,
                state="readonly")
            day.configure(background=mainColor)
            day.pack(side=LEFT)

            monthList = []
            for i in range(1, 13, 1):
                monthList.append(i)
            month = ttk.Combobox(
                dateFrame,
                values=monthList,
                width=3,
                state="readonly")
            month.configure(background=mainColor)
            month.pack(side=LEFT)

            yearList = []
            for i in range(2015, 2021, 1):
                yearList.append(i)
            year = ttk.Combobox(
                dateFrame,
                values=yearList,
                width=5,
                state="readonly")
            year.configure(background=mainColor)
            year.pack(side=LEFT)

            timeFrame = Frame(self.addPlaneWindow,
                              bd=4,
                              bg=mainColor)
            timeFrame.pack()

            Label(timeFrame,
                  bd=4,
                  bg=mainColor,
                  text='Time ').pack(side=LEFT)

            entryTimeFrame = Frame(timeFrame,
                                   bd=4,
                                   bg=mainColor)
            entryTimeFrame.pack(side=RIGHT)

            heure = Entry(entryTimeFrame,
                          bd=2,
                          bg=mainColor,
                          textvariable=int,
                          justify=CENTER,
                          relief=SUNKEN,
                          width=7)
            heure.delete(0, 100)
            heure.pack(side=LEFT)
            minute = Entry(
                entryTimeFrame,
                bd=2,
                bg=mainColor,
                textvariable=int,
                justify=CENTER,
                relief=SUNKEN,
                width=7)
            minute.delete(0, 100)
            minute.pack(side=RIGHT)

            listBox = self.listBoxDepartures

        else:
            listBox = self.listBoxArrivals
            heure = None
            minute = None
            date = None
            year = None
            month = None
            day = None

        Button(self.addPlaneWindow,
               text="Add",
               relief=GROOVE,
               bg=buttonColor,
               command=lambda: self.getPlane(
                   IDnumber,
                   airlineID,
                   passengers,
                   modelName,
                   heure,
                   minute,
                   year,
                   month,
                   day,
                   listBox)).pack(side=BOTTOM)

    def getPlane(
            self,
            IDnumberObject,
            airlineIDobject,
            passengers,
            modelObject,
            heure,
            minute,
            yearObject,
            monthObject,
            dayObject,
            listBox):
        IDnumber = IDnumberObject.get()
        IDletter = airlineIDobject.get()
        nbrPassengers = passengers.get()
        modelName = modelObject.get()

        airlineOK = False
        modelOK = False
        IDok = False
        passengerOK = False
        timeOK = False

        # Vérification de la compagnie

        if IDletter != '':

            airline = airport.airlinesDico[IDletter]
            airlineName = airline.getName()

            airlineOK = True

        else:
            text = "Vous n'avez pas sélectionné de compangie.\
                    \nVeuillez en sélectionner."
            messagebox.showerror('Error', text)

        # Vérification du modèle

        if modelName != '':

            for objet in airport.modelList:
                if objet.getName() == modelName:
                    model = objet
                    modelOK = True

                    maxPassengers = model.getPassenger()
                    fuel = model.getFuel()
                    consumption = model.getConso()

        else:
            text = "Vous n'avez pas sélectionné de modèle.\
                    \nVeuillez en sélectionner."
            messagebox.showerror('Error', text)

        # Vérification de l'ID

        if IDnumber.isdigit():

            if len(IDnumber) == 4:

                ID = (str(IDletter) + str(IDnumber))

                if airport.checkID(ID):
                    IDok = True

                else:
                    text = "Cet ID est déjà utilisé par un avion.\
                            \nVeuillez le changer."
                    messagebox.showerror('Error', text)

            else:
                text = "L'ID entré n'est pas composé d'exactement 4 chiffres!\
                        \nVeuillez vérifier."
                messagebox.showerror('Error', text)
        else:
            text = "L'ID entré n'est pas composé de chiffres!\
                    \nVeuillez vérifier."
            messagebox.showerror('Error', text)

        # Vérification du nombre de passagers

        if nbrPassengers.isdigit():

            if int(nbrPassengers) <= maxPassengers:
                passengerOK = True

            else:
                text = "Le nombre de passagers dépasse la capacité maximale du modèle d'avion sélectionné.\
                        \nCapacité max : {}".format(
                    maxPassengers)
                messagebox.showerror('Error', text)
        else:
            text = "Le nombre de passagers entré n'est pas un nombre!\
                    \nVeuillez vérifier."
            messagebox.showerror('Error', text)

        # Vérification de la date
        if yearObject is not None and monthObject is not None and dayObject is not None:
            year = yearObject.get()
            month = monthObject.get()
            day = dayObject.get()

            if year != '' and month != '' and day != '':
                date = Day(year, month, day)
                dateTuple = (year, month, day)

                dateOK = airport.dateOK(date)

            else:
                date = None

        # Vérification de l'heure

        if heure is not None and minute is not None:
            strHeure = str(heure.get())
            strMinute = str(minute.get())
            statut = 'In Time'

            if strHeure.isdigit() and strMinute.isdigit():
                nbrHeure = int(strHeure)
                nbrMinute = int(strMinute)

                time = (nbrHeure, nbrMinute)

                if date is not None:
                    timeStatus = airport.timeOK(time, date)

                    if timeStatus == -1:
                        text = "L'heure est inférieure ou égale à la date courante!\
                                \nVeuillez vérifier."
                        messagebox.showerror('Error', text)

                    elif timeStatus == 0:
                        text = "L'heure entrée n'est pas valable!\
                                \nVeuillez vérifier."
                        messagebox.showerror('Error', text)

                    elif timeStatus == 1:
                        #time = timeTMP
                        timeOK = True

                    else:
                        time = None

            else:
                text = "L'heure et les minutes entrées ne sont pas des nombres!\
                        \nVeuillez les vérifier."
                messagebox.showerror('Error', text)
        else:
            time = None
            statut = None
            date = None
            dateTuple = None
            timeOK = True  # pour les avions à l'attérissage

        if airlineOK and modelOK and IDok and passengerOK and timeOK:

            plane = airport.createPlane(
                ID,
                airlineName,
                nbrPassengers,
                fuel,
                consumption,
                modelName,
                time,
                dateTuple,
                statut)

            airport.addPlane(plane)
            text = "-L'avion {} a été ajouté.".format(plane.getID())
            self.addNotif(text)
            listBox.insert(END, plane.getID())
            self.addPlaneWindow.destroy()

    def addRandomPlane(self, planeList):
        '''
        Ajoute un avion aléatoire au départ
        '''
        IDletter = False
        model = False

        # Vérification de la présence de modelèle et de compagnie
        if len(airport.airlinesDico) == 0 and len(airport.modelList) == 0:
            text = "Il n'y a ni compangie, ni modèle enregistrés.\
                    \nVeuillez en ajouter via la fenêtre principale"
            messagebox.showwarning('No airline, no model', text)
        else:
            if len(airport.airlinesDico) == 0:
                text = "Il n'y a aucune compangie enregistrée.\
                        \nVeuillez en ajouter via la fenêtre principale"
                messagebox.showwarning('No airline', text)
            else:
                listKeyAirlines = airport.airlinesDico.keys()
                IDletter = random.choice(list(listKeyAirlines))

            if len(airport.modelList) == 0:
                text = "Il n'y a aucun modèle enregistré.\
                        \nVeuillez en ajouter via la fenêtre principale"
                messagebox.showwarning('No model', text)
            else:
                indice = random.randint(0, len(airport.modelList) - 1)
                model = airport.modelList[indice]

        if IDletter and model:
            if planeList == "departure":
                plane = airport.randomPlane(
                    IDletter,
                    model,
                    airport.departureList)
                self.listBoxDepartures.insert(END, plane.getID())

            elif planeList == "arrival":
                plane = airport.randomPlane(
                    IDletter,
                    model,
                    airport.arrivalList)
                self.listBoxArrivals.insert(END, plane.getID())

            text = "-L'avion {} a été ajouté.".format(plane.getID())
            self.addNotif(text)

    def deletePlaneButton(self):
        '''
        Supprime l'avion choisi par un simple clic dans la liste des avions
        au départ
        '''
        item = self.listBoxDepartures.curselection()
        if item:
            self.listBoxDepartures.delete(item)
            numPlane = int(item[0])
            plane = airport.departureList[numPlane]
            airport.delPlane(plane)
            text = "-L'avion {} a été supprimé.".format(plane.getID())
            self.addNotif(text)

    def checkPlaneDelete(self, event=None):
        '''
        Vérifie si un avion est sélectionné dans la liste des avions
        au départ et rend le boutton 'del' actif si oui
        '''
        if self.listBoxDepartures.curselection():
            self.delPlaneButton.configure(state=NORMAL)
            self.delModelButton.configure(state=DISABLED)
            self.delAirlineButton.configure(state=DISABLED)
        else:
            self.delPlaneButton.configure(state=DISABLED)

    def listBoxSelected(self, envent=None):
        '''
        désactive tous les boutons del lorsqu'un avion de la liste des arrivées
        est sélectionné
        '''
        if self.listBoxArrivals.curselection():
            self.delPlaneButton.configure(state=DISABLED)
            self.delAirlineButton.configure(state=DISABLED)
            self.delModelButton.configure(state=DISABLED)

    # Affichage des informations de avions
    def infoArrivalPlane(self, event=None):
        '''
        Affiche les informations d'un avion se trouvant dans la liste
        "Arrival"
        '''
        item = self.listBoxArrivals.curselection()
        if item:
            num = int(item[0])
            plane = airport.arrivalList[num]
            self.infoPlane(airport.arrivalList, plane)

    def infoDeparturePlane(self, event=None):
        '''
        Affiche les informations d'un avion se trouvant dans la liste
        "Departure"
        '''
        item = self.listBoxDepartures.curselection()
        if item:
            num = int(item[0])
            plane = airport.departureList[num]
            self.infoPlane(airport.departureList, plane)

    def infoHistoryPlane(self, event=None):
        '''
        Affiche les informations d'un avion se trouvant dans la liste
        "History"
        '''
        item = self.listBoxHistory.curselection()
        if item:
            num = int(item[0])
            plane = airport.historyList[num]
            self.infoPlane(airport.historyList, plane)

    def infoAirlinePlane(self, event=None):
        '''
        Affiche les informations d'un avion se trouvant dans la liste
        des avions d'une compagnie
        '''
        item = self.listBoxAirlinePlane.curselection()
        if item:
            num = int(item[0])
            plane = self.listAirlinePlane[num]
            self.infoPlane(self.listAirlinePlane, plane)

    def infoModelPlane(self, event=None):
        '''
        Affiche les informations d'un avion se trouvant dans la liste
        des avions d'un modèle
        '''
        item = self.listBoxModelPlane.curselection()
        if item:
            num = int(item[0])
            plane = self.listModelPlane[num]
            self.infoPlane(self.listModelPlane, plane)

    def infoPlane(self, planeList, plane):
        '''
        fenêtre d'affichage des informations d'un avion
        '''
        self.infoPlaneWindow = Toplevel(bg=mainColor)
        self.infoPlaneWindow.resizable(width=FALSE, height=FALSE)
        self.infoPlaneWindow.title("Plane Info")

        principal = Frame(
            self.infoPlaneWindow,
            bd=3,
            bg=mainColor)  # création de la frame principale
        principal.grid(row=0, column=0)

        IDframe = Frame(principal,
                        bd=5,
                        bg=mainColor)  # frame secondaire, contient l'id
        IDframe.grid(row=0, column=0)
        Label(IDframe,
              bd=3,
              bg=mainColor,
              text='ID\n',
              font=tkFont.Font(
                  size=11)).grid(
            row=0,
            column=0)
        Label(IDframe,
              bd=3,
              bg=mainColor,
              text=plane.getID()).grid(
            row=1,
            column=0)

        airlineFrame = Frame(
            principal,
            bd=5,
            bg=mainColor)  # frame secondaire, contient la compagnie
        airlineFrame.grid(row=0, column=1)
        Label(airlineFrame,
              bd=3,
              bg=mainColor,
              text='Company\n',
              font=tkFont.Font(
                  size=11)).grid(
            row=0,
            column=0)
        Label(airlineFrame,
              bd=3,
              bg=mainColor,
              text=plane.getCompany()).grid(
            row=1,
            column=0)

        passengerFrame = Frame(
            principal,
            bd=5,
            bg=mainColor)  # frame secondaire, contient le nombre de passagers
        passengerFrame.grid(row=0, column=2)
        Label(passengerFrame,
              bd=3,
              bg=mainColor,
              text='Passengers\n',
              font=tkFont.Font(
                  size=11)).grid(
            row=0,
            column=0)
        Label(passengerFrame,
              bd=3,
              bg=mainColor,
              text=plane.getPassengers()).grid(
            row=1,
            column=0)

        fuelFrame = Frame(
            principal,
            bd=5,
            bg=mainColor)  # frame secondaire, contient le fuel
        fuelFrame.grid(row=0, column=3)
        Label(fuelFrame,
              bd=3,
              bg=mainColor,
              text='Fuel\n',
              font=tkFont.Font(
                  size=11)).grid(
            row=0,
            column=0)
        Label(fuelFrame,
              bd=3,
              bg=mainColor,
              text=plane.getFuel()).grid(
            row=1,
            column=0)

        consumptionFrame = Frame(
            principal,
            bd=5,
            bg=mainColor)  # frame secondaire, contient la consommation
        consumptionFrame.grid(row=0, column=4)
        Label(consumptionFrame,
              bd=3,
              bg=mainColor,
              text='Consumption\n',
              font=tkFont.Font(
                  size=11)).grid(
            row=0,
            column=0)
        Label(consumptionFrame,
              bd=3,
              bg=mainColor,
              text=plane.getConsumption()).grid(
            row=1,
            column=0)

        modelFrame = Frame(
            principal,
            bd=5,
            bg=mainColor)  # frame secondaire, contient la consommation
        modelFrame.grid(row=0, column=6)
        Label(modelFrame,
              bd=3,
              bg=mainColor,
              text='Model\n',
              font=tkFont.Font(
                  size=11)).grid(
            row=0,
            column=0)
        Label(modelFrame,
              bd=3,
              bg=mainColor,
              text=plane.getModel()).grid(
            row=1,
            column=0)

        if plane.getTime():
            timeFrame = Frame(
                principal,
                bd=5,
                bg=mainColor)  # frame secondaire, contient l'heure
            timeFrame.grid(row=0, column=7)
            Label(timeFrame,
                  bd=3,
                  bg=mainColor,
                  text='Time',
                  font=tkFont.Font(
                      size=11)).grid(
                row=0,
                column=0)

            time = plane.getTime()
            tmp = airport.affTime(airport.convTupleToTick(time))
            date = plane.getDay()
            tmp2 = airport.affDay(date)
            text = (str(tmp2) + "\n" + str(tmp))
            Label(timeFrame,
                  bd=3,
                  bg=mainColor,
                  text=text).grid(
                row=1,
                column=0)

        if plane.getStatut():
            statusFrame = Frame(
                principal,
                bd=5,
                bg=mainColor)  # frame secondaire, contient le statut
            statusFrame.grid(row=0, column=8)
            Label(statusFrame,
                  bd=3,
                  bg=mainColor,
                  text='Statut\n',
                  font=tkFont.Font(
                      size=11)).grid(
                row=0,
                column=0)
            Label(statusFrame,
                  bd=3,
                  bg=mainColor,
                  text=plane.getStatut()).grid(
                row=1,
                column=0)

        if not plane.getStatut():
            ratioFrame = Frame(
                principal,
                bd=5,
                bg=mainColor)  # frame secondaire, contient le ration (nbr de tour)
            ratioFrame.grid(row=0, column=5)
            Label(ratioFrame,
                  bd=3,
                  bg=mainColor,
                  text='Ratio\n',
                  font=tkFont.Font(
                      size=11)).grid(
                row=0,
                column=0)
            Label(ratioFrame,
                  bd=3,
                  bg=mainColor,
                  text=plane.ratio()).grid(
                row=1,
                column=0)

        buttonFrame = Frame(principal, bd=5, bg=mainColor)
        buttonFrame.grid(row=1, column=3)
        Button(
            buttonFrame,
            text='OK',
            relief=GROOVE,
            width=6,
            bg=buttonColor,
            command=self.planeButtonOK).grid(
            row=0,
            column=0)

    def planeButtonOK(self):
        '''
        Ferme la fenêtre d'affichage des informations de l'avion
        '''
        self.infoPlaneWindow.destroy()

    # Airlines
    def addAirline(self):
        '''
        Permet d'ajouter une compagnie. Ouvre une nouvelle fenêtre demandant
        le nom et l'id de la nouvelle compagnie
        '''
        self.addAirlineWindow = Toplevel(bg=mainColor)
        self.addAirlineWindow.resizable(width=FALSE, height=FALSE)
        self.addAirlineWindow.title("Add Airlines")

        labelFrame = Frame(
            self.addAirlineWindow,
            bd=3,
            bg=mainColor)  # frame des label
        labelFrame.grid(row=0, column=1)

        Label(
            labelFrame,
            bd=6,
            bg=mainColor,
            text='Add Airlines',
            font=tkFont.Font(
                size=10)).grid(
            row=0,
            column=1)

        entryFrame = Frame(
            self.addAirlineWindow,
            bd=5,
            bg=mainColor)  # frame des entry
        entryFrame.grid(row=1, column=1)

        Label(
            entryFrame,
            bd=4,
            bg=mainColor,
            text='Full Name').grid(
            row=0,
            column=0)
        airline = Entry(
            entryFrame,
            bd=2,
            bg=mainColor,
            textvariable=str,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        airline.delete(0, 100)
        airline.grid(row=0, column=1)

        Label(entryFrame, bd=4, bg=mainColor, text='ID').grid(row=1, column=0)
        airlineID = Entry(
            entryFrame,
            bd=2,
            bg=mainColor,
            textvariable=str,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        airlineID.delete(0, 100)
        airlineID.grid(row=1, column=1)

        Button(
            self.addAirlineWindow,
            text='Add',
            relief=GROOVE,
            width=10,
            bg=buttonColor,
            command=lambda: self.addAirlinesButton(
                (airline.get()).lower(),
                (airlineID.get()).upper())).grid(
            row=3,
            column=1)

    def addAirlinesButton(self, airline, airlineID):
        '''
        Ajoute la compagnie au dictionnaire des compagnies
        '''
        if len(airlineID) == 2 or len(airlineID) == 3:
            if airlineID not in airport.airlinesDico:
                objAirline = airport.addAirlines(airlineID, airline)
                self.airlinesList.append(airlineID)

                text = "-La compagnie {} a été ajoutée.".format(airline)
                self.addNotif(text)

                self.addAirlineWindow.destroy()

                self.listBoxAirlines.insert(END, airline)

            else:
                text = "La compagnie {} existe déjà.".format(company)
                messagebox.showwarning('Company already exist', text)
        else:
            text = "La taille de l'ID doit être de 2 ou 3 caractères."
            messagebox.showwarning('ID length', text)

    def delAirline(self):
        '''
        Permet de supprimer une compagnie
        '''
        item = self.listBoxAirlines.curselection()
        if item:
            self.listBoxAirlines.delete(item)

            numAirline = int(item[0])
            airlineID = self.airlinesList[numAirline]
            airline = airport.airlinesDico[airlineID]

            text = "-La compagnie {} a été supprimée.".format(
                airline.getName())
            self.addNotif(text)
            airport.delAirlines(airlineID)

    def checkAirlineDelete(self, event=None):
        '''
        Vérifie si un avion est sélectionné dans la liste des avions
        au départ et rend le boutton 'del' actif si oui
        '''
        if self.listBoxAirlines.curselection():
            self.delAirlineButton.configure(state=NORMAL)
            self.delPlaneButton.configure(state=DISABLED)
            self.delModelButton.configure(state=DISABLED)
        else:
            self.delAirlineButton.configure(state=DISABLED)

    def showInfoAirline(self, event=None):
        '''
        Appelle la fonction d'affichage des informations et avions de la
        compangie sélectionnée dans la liste de la fenêtre principale
        '''
        item = self.listBoxAirlines.curselection()
        if item:
            numAirline = int(item[0])
            airlineID = self.airlinesList[numAirline]

            self.infoAirline(airlineID)

    def infoAirline(self, airlineID):
        '''
        Affiche les avions et informations d'une compagnie
        '''
        self.infoAirlineWindow = Toplevel(bg=mainColor)
        self.infoAirlineWindow.resizable(width=FALSE, height=FALSE)
        self.infoAirlineWindow.title("Company Info")

        airline = airport.airlinesDico[airlineID]
        nameAirline = airline.getName()
        textName = "Name: {}".format(nameAirline)
        textID = "ID: {}".format(airlineID)

        principalFrame = Frame(self.infoAirlineWindow,
                               bd=5,
                               bg=mainColor)
        principalFrame.pack()

        infoFrame = Frame(principalFrame,
                          bd=5,
                          bg=mainColor)
        infoFrame.pack()

        Label(infoFrame,
              bd=3,
              bg=mainColor,
              text=textName).pack()
        Label(infoFrame,
              bd=3,
              bg=mainColor,
              text=textID).pack()

        textLabel = "Planes of {} :".format(nameAirline)
        planeFrame = LabelFrame(
            principalFrame,
            bd=5,
            bg=mainColor,
            relief=RIDGE,
            text=textLabel,
            font=tkFont.Font(
                size=10))
        planeFrame.pack()

        listBoxArea = Frame(
            planeFrame,
            bd=8,
            bg=mainColor)  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.listBoxAirlinePlane = Listbox(
            listBoxArea,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)

        # active le double-clic pour obtenir les infos d'un avion
        self.listBoxAirlinePlane.bind(
            "<Double-Button-1>",
            self.infoAirlinePlane)

        planeLists = [
            airport.departureList,
            airport.arrivalList,
            airport.historyList]

        # Liste des avions de la compangnies, simplifie la sélection dans la
        # listbox
        self.listAirlinePlane = []
        for lists in planeLists:
            for plane in lists:
                if plane.getCompany() == nameAirline:
                    self.listBoxAirlinePlane.insert(END, plane.getID())
                    self.listAirlinePlane.append(plane)

        scrollbar.config(command=self.listBoxAirlinePlane.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        listBoxArea.pack()
        self.listBoxAirlinePlane.pack()

        Button(principalFrame,
               text='OK',
               relief=GROOVE,
               width=6,
               bg=buttonColor,
               command=self.airlineButtonOK).pack(
            side=BOTTOM)

    def airlineButtonOK(self):
        '''
        Détruit la fenêtre d'informations de la compagnie
        '''
        self.infoAirlineWindow.destroy()

    # Model
    def addModel(self):
        '''
        Ouvre une fenêtre permetant à l'utilisateur d'entrer les informations
        du modèle qu'il veut ajouter
        '''
        self.addModelWindow = Toplevel(bg=mainColor)
        self.addModelWindow.resizable(width=FALSE, height=FALSE)
        self.addModelWindow.title("Add Model")

        principalFrame = Frame(
            self.addModelWindow,
            bd=3,
            bg=mainColor)  # frame du label
        principalFrame.grid(row=0, column=1)

        entryFrame = Frame(
            self.addModelWindow,
            bd=5,
            bg=mainColor)  # frame des entry
        entryFrame.grid(row=1, column=1)

        labelPrincipal = Label(
            principalFrame,
            bd=6,
            bg=mainColor,
            text='Add Model',
            font=tkFont.Font(
                size=10))
        labelPrincipal.grid(row=0, column=1)

        labelModel = Label(
            entryFrame,
            bd=4,
            bg=mainColor,
            text='Name')
        labelModel.grid(row=0, column=0)
        model = Entry(
            entryFrame,
            bd=2,
            bg=mainColor,
            textvariable=str,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        model.delete(0, 100)
        model.grid(row=0, column=1)

        labelFuel = Label(
            entryFrame,
            bd=4,
            bg=mainColor,
            text='Fuel')
        labelFuel.grid(row=1, column=0)
        fuel = Entry(
            entryFrame,
            bd=2,
            bg=mainColor,
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        fuel.delete(0, 100)
        fuel.grid(row=1, column=1)

        labelCons = Label(
            entryFrame,
            bd=4,
            bg=mainColor,
            text='Consumption')
        labelCons.grid(row=2, column=0)
        consumption = Entry(
            entryFrame,
            bd=2,
            bg=mainColor,
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        consumption.delete(0, 100)
        consumption.grid(row=2, column=1)

        labelPassengers = Label(
            entryFrame,
            bd=4,
            bg=mainColor,
            text='Passengers')
        labelPassengers.grid(row=3, column=0)
        passengers = Entry(
            entryFrame,
            bd=2,
            bg=mainColor,
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        passengers.delete(0, 100)
        passengers.grid(row=3, column=1)

        buttonFrame = Frame(self.addModelWindow, bd=5, bg=mainColor)
        buttonFrame.grid(row=2, column=1)
        buttonOK = Button(
            buttonFrame,
            text='OK',
            relief=GROOVE,
            width=6,
            bg=buttonColor,
            command=lambda: self.addModelButton(
                model,
                fuel,
                consumption,
                passengers)).grid(
            row=0,
            column=0)

    def addModelButton(self, newModel, newFuel, newConsumption, newPassengers):
        '''
        Vérifie les données entrées par l'utilisateur et ajoute le modèle si
        elles sont correctes
        '''
        model = str(newModel.get()).upper()
        fuel = newFuel.get()
        consumption = newConsumption.get()
        passengers = newPassengers.get()

        if fuel.isdigit() and consumption.isdigit() and passengers.isdigit():
            modFuel = int(fuel)
            modConso = int(consumption)
            modPass = int(passengers)
            airport.addModel(model, modFuel, modConso, modPass)

            self.addModelWindow.destroy()

            self.listBoxModel.insert(END, model)
            self.listNameModel.append(model)

            text = "-Le modèle {} a été ajouté.".format(model)
            self.addNotif(text)

        else:
            text = "Les données entrées ne sont pas correctes!\
                    \nVeuillez les vérifier."
            messagebox.showerror('Error', text)

    def delModel(self):
        '''
        Supprime le modèle sélectionné
        '''
        item = self.listBoxModel.curselection()
        if item:
            self.listBoxModel.delete(item)

            numModel = int(item[0])
            model = airport.modelList[numModel]
            airport.delModel(model)

            name = model.getName()
            text = "-Le modèle '{}' a été supprimé.".format(name)
            self.addNotif(text)

    def checkModelDelete(self, event=None):
        '''
        Active le bouton "Delete" lorsqu'un modèle est selectionné
        '''
        if self.listBoxModel.curselection():
            self.delModelButton.configure(state=NORMAL)
            self.delPlaneButton.configure(state=DISABLED)
            self.delAirlineButton.configure(state=DISABLED)
        else:
            self.delModelButton.configure(state=DISABLED)

    def showInfoModel(self, event=None):
        '''
        Appelle la fonction d'affichage du modèle sélectionné
        '''
        item = self.listBoxModel.curselection()
        if item:
            numModel = int(item[0])
            model = airport.modelList[numModel]

            self.infoModel(model)

    def infoModel(self, model):
        '''
        Affiche les informations du modèle
        '''
        self.infoModelWindow = Toplevel(bg=mainColor)
        self.infoModelWindow.resizable(width=FALSE, height=FALSE)
        self.infoModelWindow.title("Model Info")

        name = model.getName()
        fuel = model.getFuel()
        consumption = model.getConso()
        passengers = model.getPassenger()

        planeFrame = Frame(
            self.infoModelWindow,
            bd=3,
            bg=mainColor)  # création de la frame principale
        planeFrame.grid(row=0, column=0)

        nameFrame = Frame(
            planeFrame,
            bd=5,
            bg=mainColor)
        nameFrame.grid(row=0, column=0)
        Label(
            nameFrame,
            bd=3,
            bg=mainColor,
            text='Model',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        Label(
            nameFrame,
            bd=3,
            bg=mainColor,
            text=name).grid(
            row=1,
            column=0)

        fuelFrame = Frame(
            planeFrame,
            bd=5,
            bg=mainColor)
        fuelFrame.grid(row=0, column=1)
        Label(
            fuelFrame,
            bd=3,
            bg=mainColor,
            text='Fuel',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        Label(
            fuelFrame,
            bd=3,
            bg=mainColor,
            text=fuel).grid(
            row=1,
            column=0)

        consFrame = Frame(
            planeFrame,
            bd=5,
            bg=mainColor)
        consFrame.grid(row=0, column=2)
        labelCons = Label(
            consFrame,
            bd=3,
            bg=mainColor,
            text='Consumption',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        Label(
            consFrame,
            bd=3,
            bg=mainColor,
            text=consumption).grid(
            row=1,
            column=0)

        passengerFrame = Frame(
            planeFrame,
            bd=5,
            bg=mainColor)
        passengerFrame.grid(row=0, column=3)
        Label(
            passengerFrame,
            bd=3,
            bg=mainColor,
            text='Passengers',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        Label(
            passengerFrame,
            bd=3,
            bg=mainColor,
            text=passengers).grid(
            row=1,
            column=0)

        text = "{} planes".format(name)
        planeFrame = LabelFrame(
            self.infoModelWindow,
            bd=5,
            relief=RIDGE,
            bg=mainColor,
            text=text,
            font=tkFont.Font(
                size=10))  # création de list_box et de la scrollbar associée
        planeFrame.grid(row=1, column=0)
        listBoxArea = Frame(
            planeFrame,
            bd=8,
            bg=mainColor)
        listBoxArea.pack()

        scrollbar = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.listBoxModelPlane = Listbox(
            listBoxArea,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)

        self.listBoxModelPlane.bind(
            "<Double-Button-1>",
            self.infoModelPlane)
        # active le double-clic pour obtenir les infos d'un avion

        planeLists = [
            airport.departureList,
            airport.arrivalList,
            airport.historyList]

        # Liste des avions du modèle, simplifie la sélection dans la listbox
        self.listModelPlane = []
        for lists in planeLists:
            for plane in lists:
                if plane.getModel() == name:
                    self.listBoxModelPlane.insert(END, plane.getID())
                    self.listModelPlane.append(plane)

        scrollbar.config(command=self.listBoxModelPlane.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listBoxModelPlane.pack()

        buttonFrame = Frame(self.infoModelWindow, bd=5, bg=mainColor)
        buttonFrame.grid(row=2, column=0)
        Button(
            buttonFrame,
            text='OK',
            relief=GROOVE,
            width=6,
            bg=buttonColor,
            command=self.modelButtonOK).grid(
            row=0,
            column=0)

    def modelButtonOK(self):
        '''
        Detruit la fenêtre (Toplevel) contenant les informations du model
        '''
        self.infoModelWindow.destroy()

    # Fonctions d'avancement dans le temps/la simulation
    def checkRunways(self):
        '''
        Vérifie le nombre de pistes et affiche un message dans les
        notifications
        '''
        if airport.departureRunway == 0 and airport.arrivalRunway == 0 \
                and airport.mixteRunway == 0:
            text = "-Votre aéroport n'a aucune piste pour faire décoller ou \
                    atterrir des avions."
            self.addNotif(text)

        elif airport.departureRunway == 0 and airport.mixteRunway == 0:
            text = "-Votre aéroport n'a aucune piste pour faire décoller des \
                    avions."
            self.addNotif(text)

        elif airport.arrivalRunway == 0 and airport.mixteRunway == 0:
            text = "-Votre aéroport n'a aucune piste pour faire atterrir des \
                    avions."
            self.addNotif(text)

    def step(self):
        '''
        Permet d'avancer d'une minute le temps
        Si l'aéroport n'a pas de pistes, un message est affiché
        Effectue les évenement suivants en fonction du nombres
        de pistes présentes dans l'aéroport
        Affiche un message si un avion est en retard
        Mets à jour les informations des avions
        '''
        self.checkRunways()

        if airport.weatherClear:
            for j in range(airport.departureRunway):
                plane = airport.nextEvent("departure")
                if plane:
                    self.executePlane(plane)
                    text = "-L'avion {} a décollé.".format(plane.getID())
                    self.addNotif(text)

            for k in range(airport.arrivalRunway):
                plane = airport.nextEvent("arrival")
                if plane:
                    self.executePlane(plane)
                    text = "-L'avion {} a atterri.".format(plane.getID())
                    self.addNotif(text)

            for l in range(airport.mixteRunway):
                plane = airport.nextEvent("mixte")
                if plane:
                    self.executePlane(plane)
                    if plane.getStatut() == "Landed":
                        text = "-L'avion {} a atterri.".format(
                            plane.getID())
                        self.addNotif(text)
                    else:
                        text = "-L'avion {} a décollé.".format(
                            plane.getID())
                        self.addNotif(text)

        self.eventRandom()
        crashedPlane, delayedPlane = airport.updateStatus()

        for event in crashedPlane:
            plane = event[0]
            death = event[1]
            self.executePlane(plane)

            if airport.weatherClear:
                text = "-L'avion {} s'est crashé.   {} personnes sont \
                        mortes dans l'accident.".format(plane.getID(),
                                                        death)
            else:
                text = "-L'avion {} s'est crashé à cause du mauvais temps.\
                        {} personnes sont mortes dans l'accident.".format(plane.getID(), death)
            self.addNotif(text)

        for plane in delayedPlane:
            if airport.weatherClear:
                text = "-L'avion {} a du retard.".format(plane.getID())
            else:
                text = "-L'avion {} a du retard à cause du mauvais temps".format(
                    plane.getID())
            self.addNotif(text)

        if airport.tick == 1440:
            self.newDay()
            text = 'New Day!'
            self.addNotif(text)

        generalTime = airport.affTime(airport.tick)
        self.clock.configure(text=generalTime)

    def executePlane(self, plane):
        '''
        Éfface l'avion de l'évenement de sa listeBox
        '''
        if plane is not None:
            listPlane = self.listBoxDepartures.get(0, END)
            if plane.getID() in listPlane:
                item = listPlane.index(plane.getID())
                self.listBoxDepartures.delete(item)
            else:
                listPlane = self.listBoxArrivals.get(0, END)
                item = listPlane.index(plane.getID())
                self.listBoxArrivals.delete(item)

    def eventRandom(self):
        '''
        Permet de créer un avion de manière aléatoire
        (évenement aléatoire)
        '''
        nbr = int(random.randint(0, 40))

        if len(airport.modelList) > 0 and len(airport.airlinesDico) > 0:
            if nbr == 8:
                self.addRandomPlane("departure")
            if nbr == 3:
                self.addRandomPlane("arrival")

    def newDay(self):
        '''
        Appelle la fonction newDay qui permet de "nettoyer" l'aéroport
        pour le nouveau jour
        Vide les listBox contenant les avions au départ et à l'arrivée
        '''
        airport.newDay()

        if airport.weatherClear:
            color = "green"
        else:
            color = "red"
        self.affichageMeteo.configure(
            fg=color,
            text=airport.affMeteo(
                airport.weatherClear))

        generalDay = airport.affDay(airport.currentDay)
        self.affichageDay.configure(text=generalDay)

        self.listBoxArrivals.delete(0, END)
        self.listBoxDepartures.delete(0, END)

        for plane in airport.departureList:
            self.listBoxDepartures.insert(END, plane.getID())


    def waitStep(self, window):
        '''
        fonction permetant d'avancer automatiquement le temps à la
        minute suivante réelle
        60000 = 1 minute
        si le temps est d'une minute, vérifier le nombre de secondes déjà
        écoulées dans la minute en cours afin de correspondre aux minutes
        réelles
        '''
        if not self.debugMode:
            self.wait = 60000
            second = datetime.now().second

            if second != 0:
                self.wait = (60 - second) * 1000

        self.step()
        self.thread = self.root.after(self.wait, lambda: self.waitStep(window))

    # Fonctions de modifications des pistes (runways)
    def plusRunway(self, runway):
        '''
        Incrémente d'un la valeur de la piste passée en paramètre
        '''
        if runway == 'departure':
            airport.departureRunway += 1
            text = "Departure: {}".format(airport.departureRunway)
            self.departureLabel.configure(text=text)

        elif runway == 'arrival':
            airport.arrivalRunway += 1
            text = "Arrival:      {}".format(airport.arrivalRunway)
            self.arrivalLabel.configure(text=text)

        elif runway == 'mixte':
            airport.mixteRunway += 1
            text = "Mixte:       {}".format(airport.mixteRunway)
            self.mixteLabel.configure(text=text)

    def minusRunway(self, runway):
        '''
        Décrémente d'un la valeur de la piste pasée en paramètre
        '''
        if runway == 'departure':
            airport.departureRunway -= 1
            if airport.departureRunway < 0:
                airport.departureRunway = 0
            text = "Departure: {}".format(airport.departureRunway)
            self.departureLabel.configure(text=text)

        elif runway == 'arrival':
            airport.arrivalRunway -= 1
            if airport.arrivalRunway < 0:
                airport.arrivalRunway = 0
            text = "Arrival:      {}".format(airport.arrivalRunway)
            self.arrivalLabel.configure(text=text)

        elif runway == 'mixte':
            airport.mixteRunway -= 1
            if airport.mixteRunway < 0:
                airport.mixteRunway = 0
            text = "Mixte:       {}".format(airport.mixteRunway)
            self.mixteLabel.configure(text=text)

    # Statistiques
    def showStat(self):
        '''
        Affiche les statistiques de l'aéroport
        '''
        statWindow = Toplevel(bg=mainColor)
        statWindow.resizable(width=FALSE, height=FALSE)
        statWindow.title("Statistics")

        planeFrame = LabelFrame(
            statWindow,
            bd=4,
            relief=RIDGE,
            bg=mainColor,
            text='Statistics',
            font=tkFont.Font(
                size=11))
        planeFrame.pack()

        text = "\n- Nombre total d'avions: {}"\
            "\n\n- Nombre d'avions au décollage\nou ayant décollés: {}"\
            "\n\n- Nombre d'avions à l'atterrissage\nou ayant atterri: {}"\
            "\n\n- Nombre total de passagers: {}"\
            "\n\n- Nombre de crashs: {}"\
            "\n\n- Nombre de morts lors des crashs: {}"\
            "\n\n- Nombre de compagnies: {}"\
            "\n\n- Nombre de modèles d'avions: {}".format(
                airport.statPlaneGlobal,
                airport.statPlaneDep,
                airport.statPlaneArr,
                airport.statPassengers,
                airport.statCrash,
                airport.statDeath,
                airport.statAirlines,
                airport.statModel)
        message = Message(
            planeFrame,
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
        historyWindow.resizable(width=FALSE, height=FALSE)
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
            text = (str(plane.getID()).ljust(13, ' ') + str(plane.getStatut()))
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
        help = Toplevel(bg=mainColor)
        help.resizable(width=FALSE, height=FALSE)
        help.title("Help")
        Label(
            help,
            bd=6,
            bg=mainColor,
            text="Bienvenue dans le simulateur de gestion d'aéroport.",
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
            filetypes=[
                ("Fichier txt",
                 "*.txt"),
                ("Tous",
                 "*")],
            initialfile="save.txt",
            parent=self.root)
        if fileName:
            if airport.saveSystem(fileName):
                text = "-Sauvegarde réussie."
                self.addNotif(text)
            else:
                messagebox.showwarning(
                    "Sauvegarde",
                    "Problème pendant la sauvegarde.")

    def loadSystem(self, event=None):
        '''
        Permet de charger une sauvegarde
        '''
        fileName = filedialog.askopenfilename(
            filetypes=[
                ("Fichier txt",
                 "*.txt"),
                ("Tous",
                 "*")],
            initialfile="save.txt",
            parent=self.root)
        if fileName:
            if airport.loadSystem(fileName):
                self.root.after_cancel(
                    self.thread)  # arrête le thread en cours
                self.root.destroy()
                root = Tk()
                root.title("Airport Simulator")
                root.configure(background=mainColor)
                root.resizable(width=FALSE, height=FALSE)
                self.__init__(root)
                text = "-Chargement de la sauvegarde réussi."
                self.addNotif(text)
            else:
                messagebox.showwarning(
                    "Chargement",
                    "Problème pendant la chargement.")

    def clearSystem(self, event=None):
        text = "Clear the airport?"
        result = messagebox.askyesno('Clear', text)

        if result:
            airport.clearSystem()
            self.root.after_cancel(self.thread)  # arrête le thread en cours
            self.root.destroy()
            root = Tk()
            root.title("Airport Simulator")
            root.configure(background=mainColor)
            root.resizable(width=FALSE, height=FALSE)
            self.__init__(root)
            text = "-Rénitialisation de l'aéroport."
            self.addNotif(text)

    # Affichage des notifications
    def addNotif(self, text):
        '''
        Ajoute la nouvelle notification à la liste des notifications
        Appelle la fonction d'affichage des notifications
        '''
        self.notifList.insert(
            0,
            text)  # La dernière notif est en position 0 dans la liste
        self.notifDisplayList.pop(0)
        self.notifDisplayList.append(text)
        self.displayNotif()

    def displayNotif(self):
        '''
        Détruit l'ancienne frame de notifications pour la
        remplacer par la nouvelle
        '''
        self.notifFrame.destroy()

        self.notifFrame = LabelFrame(
            self.column4bottom,
            bd=4,
            width=40,
            relief=RIDGE,
            bg=mainColor,
            text='Notifications',
            font=tkFont.Font(size=10))
        self.notifFrame.pack()

        index = 1
        for notif in self.notifDisplayList:
            color = self.textColor
            if index == self.listSize:
                color = self.textColorFirst

            self.notifText = StringVar()
            notification = Message(self.notifFrame,
                                   bd=4,
                                   bg=mainColor,
                                   fg=color,
                                   anchor=W,
                                   width=200,
                                   textvariable=self.notifText,
                                   justify=LEFT)
            self.notifText.set(notif)
            notification.pack(side=BOTTOM)
            index += 1

    def showLog(self):
        '''
        Affiche toutes les notifications depuis le début du programme
        '''
        log = Toplevel(bg=mainColor)
        log.resizable(width=FALSE, height=FALSE)
        log.title("Log")

        notifFrame = LabelFrame(
            log,
            bd=4,
            bg=mainColor,
            height=150,
            text="Log des notifications du programme:",
            font=tkFont.Font(
                size=10))
        notifFrame.pack(
            side=TOP)

        text = "Les notifications les plus récentes sont en tête de liste."
        Label(
            notifFrame,
            bd=7,
            bg=mainColor,
            text=text,
            font=tkFont.Font(
                size=8)).pack()

        listBoxArea = Frame(
            notifFrame,
            bd=8,
            bg=mainColor)  # création de listBox et de la scrollbar associée
        scrollbarVER = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor=mainColor,
            orient=VERTICAL)
        scrollbarHOR = Scrollbar(
            listBoxArea,
            bg=buttonColor,
            activebackground='grey',
            troughcolor=mainColor,
            orient=HORIZONTAL)
        listBoxNotif = Listbox(
            listBoxArea,
            height=25,
            width=40,
            bd=2,
            yscrollcommand=scrollbarVER.set,
            xscrollcommand=scrollbarHOR.set)

        for notif in self.notifList:
            textNotif = notif.join('\n')
            listBoxNotif.insert(END, notif)

        scrollbarVER.config(command=listBoxNotif.yview)
        scrollbarHOR.config(command=listBoxNotif.xview)
        scrollbarVER.pack(side=RIGHT, fill=Y)
        scrollbarHOR.pack(side=BOTTOM, fill=BOTH)
        listBoxArea.pack()
        listBoxNotif.pack()


if __name__ == "__main__":
    root = Tk()
    PrincipalWindow(root)
    root.title("Airport Simulator")
    root.configure(background=mainColor)
    root.resizable(width=FALSE, height=FALSE)
    root.mainloop()
