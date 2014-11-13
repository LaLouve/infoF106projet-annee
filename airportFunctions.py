'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: airportFunctions.py


contient toutes les fonctions de bases du programme
permet fonctionnement en terminal et en GUI 
'''

import random
from plane import Plane
import json  # pour le système de sauvegarde

IDmax = 9999  # valeur maximun de l'ID


class Airport:

    def __init__(self):
        '''
        initialisation des données
        '''
        self.departureList = []  # avions en attente de décollage
        self.arrivalList = []  # avions en attente de d'atterissage
        # autres avions (déjà atterri, décollé ou crashé)
        self.historyList = []
       
        # dictionnaire de toutes les compagnies, avec leur ID
        self.airlines = {}
        
        # entier représentant les minutes écoulées (min: 0, max: 1439)
        self.tick = 0
        self.day = 1 
        
        self.departureRunway = 0  # nbr de pistes de décollage
        self.arrivalRunway = 0  # nbr de pistes d'atterrissage
        self.mixteRunway = 0  # nbr de piste d'atterrissage et de décollage
        
        self.dicoModel = {}  # dico des différents modèles d'avions

        self.statPlaneGlobal = 0  # nbr total d'avions
        self.statPlaneDep = 0  # nbr d'avions au décollage
        self.statPlaneArr = 0  # nbr d'avions à l'arrivé
        self.statPassengers = 0  # nbr de passagers
        self.statCrash = 0  # nbr de crash
        self.statDeath = 0  # nbr de passagers morts dans des crashs
        self.statAirlines = 0  # nbr de compagnies
        self.statModel = 0  # nbr de modèles

    # PLANE
    def createPlane(self, ID, company, passengers, fuel, consumption, model, time, statut):
        '''
        creation d'un avion
        '''
        newPlane = Plane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        IDletter = ID[:-4]
        # ajouter la compagnie au dictionnaire si elle n'y est pas déjà
        if (company) not in self.airlines:
            self.addAirlines(company, IDletter)
        self.statPlaneGlobal += 1 #statistiques
        self.statPassengers += int(passengers) #statistiques
        return newPlane

    def addPlane(self, plane):
        '''
        ajout d'un avion à departureList, arrivalList
        '''
        if plane.getTime() is None:
            self.arrivalList.append(plane)
            self.statPlaneArr += 1
        else:
            self.departureList.append(plane)
            self.statPlaneDep += 1

    def delPlane(self, plane):
        '''
        supression d'un avion de departureList
        '''
        self.departureList.remove(plane)
        plane.setStatut("Deleted")
        self.historyList.append(plane)


    # AIRLINES
    def addAirlines(self, company, IDletter):
        '''
        ajout d'une compangnie au dictionnaire des compagnies
        '''
        self.airlines[IDletter] = company
        self.statAirlines += 1

    def delAirlines(self, companyID):
        '''
        Supprime la compangnie demandée
        '''
        self.airlines.pop(companyID)
        self.statAirlines -= 1


    # MODEL
    def addModel(self, model, modFuel, modConso, modPass):
        '''
        permet d'ajouter un nouveau modèle d'avion
        '''
        modCar = [
            modFuel,
            modConso,
            modPass]  # liste des caractéristique du modèle
        self.dicoModel[model] = modCar
        self.statModel += 1
        
    def delModel(self, model):
        '''
        Permet de supprimer un modèle d'avion
        '''
        del self.dicoModel[model]
        self.statModel -= 1


    # RANDOM PLANE
    def randomPlane(self, airlines, model, planeList):
        '''
        Permet la création d'un avion au départ avec des données aléatoires.
        utilise l'ID et le modèle passés en paramètres 
        '''
        modMaxPass = self.dicoModel[model][2]
        passengers = random.randint(1, modMaxPass)
        fuel = self.dicoModel[model][0]
        consumption = self.dicoModel[model][1]   


        company = self.airlines[airlines]
        number = str(random.randint(1, IDmax))
        IDnumber = number.rjust(4, '0')
        ID = (airlines + IDnumber)

        if planeList == self.departureList:
            time = (random.randint(0, 23), random.randint(0, 59))
            statut = "In Time"
        else:
            time = None
            statut = None

        newPlane = self.createPlane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        self.addPlane(newPlane)

        return newPlane


    # RUNWAYS
    def modifRunways(self, nbrDepRunway, nbrArrRunway, nbrMixteRunway):
        '''
        Permet de modifier le nombre de pistes
        '''
        self.departureRunway = nbrDepRunway
        self.arrivalRunway = nbrArrRunway
        self.mixteRunway = nbrMixteRunway


    # NEXT EVENT
    def priorityDeparture(self):
        '''
        avion le plus prioritaire pour le depart

        [1:] permet de ne pas verifier l'avion prioritaire
        avec lui même vu qu'il est le premier de la liste
        '''
        if len(self.departureList) == 0:
            mostPrior = None

        else:
            mostPrior = self.departureList[0]
            for plane in self.departureList[1:]:
                if self.convTupleToTick(plane.getTime()) <\
                   self.convTupleToTick(mostPrior.getTime()):
                    mostPrior = plane

                if self.convTupleToTick(plane.getTime()) ==\
                   self.convTupleToTick(mostPrior.getTime()):
                    if int(plane.getPassengers()) >\
                       mostPrior.getPassengers():
                        mostPrior = plane

        return mostPrior

    def priorityArrival(self):
        '''
        avion le plus prioritaire pour l'atterissage

        on divise le niveau de carburant (fuel)par la consommation de carburant
        par tour (consumption), pour obtenir le nombre de tours
        que l'avion peut encore rester en l'air.
        '''
        if len(self.arrivalList) == 0:
            mostPrior = None

        else:
            mostPrior = self.arrivalList[0]
            for plane in self.arrivalList[1:]:
                if plane.ratio() < mostPrior.ratio():
                    mostPrior = plane
                    # si le nombre de tour restant est le même, on regarde le
                    # nombre de passagers
                elif plane.ratio() == mostPrior.ratio():
                    if plane.getPassengers() >\
                       mostPrior.getPassengers():
                        mostPrior = plane
        return mostPrior

    def nextEvent(self):
        '''
        Permet d'effectuer l'action la plus prioritaire. Si il n'y a pas
        d'avion devant décoller, c'est l'avion avec le ratio carburant/
        consomation le plus petit qui atterri.
        Une fois l'action effectuée, l'avion en question est retiré de sa liste
        d'origine et placé dans historyList
        '''
        arrivalPlane = self.priorityArrival()
        departurePlane = self.priorityDeparture()
        mostPrior = None

        if arrivalPlane is not None and arrivalPlane.ratio() == 1:
            mostPrior = arrivalPlane
            mostPrior.setStatut('Landed')
            self.arrivalList.remove(mostPrior)
            
        elif departurePlane is not None and\
                self.convTupleToTick(departurePlane.getTime()) <= self.tick:
            mostPrior = departurePlane
            mostPrior.setStatut('Take Off')
            self.departureList.remove(mostPrior)

        elif arrivalPlane is not None:
            mostPrior = arrivalPlane
            mostPrior.setStatut('Landed')
            self.arrivalList.remove(mostPrior)

        if mostPrior is not None:
            self.historyList.append(mostPrior)

        return (mostPrior)

    def nextDeparture(self):
        '''
        Determine le prochain avion à décoller
        '''
        departurePlane = self.priorityDeparture()
        mostPrior = None

        if departurePlane is not None and\
           self.convTupleToTick(departurePlane.getTime()) <= self.tick:
            mostPrior = departurePlane
            mostPrior.setStatut('Take Off')
            self.departureList.remove(mostPrior)

        if mostPrior is not None:
            self.historyList.append(mostPrior)

        return (mostPrior)

    def nextArrival(self):
        '''
        Determine le prochain avion à atterrir
        '''
        mostPrior = None

        arrivalPlane = self.priorityArrival()

        if arrivalPlane is not None and arrivalPlane.ratio() == 1:
            mostPrior = arrivalPlane
            mostPrior.setStatut('Landed')
            self.arrivalList.remove(mostPrior)

        elif arrivalPlane is not None:
            mostPrior = arrivalPlane
            mostPrior.setStatut('Landed')
            self.arrivalList.remove(mostPrior)

        if mostPrior is not None:
            self.historyList.append(mostPrior)

        return (mostPrior)

    def eventRandom(self):
        '''
        Permet de créer un avion de manière aléatoire
        (évenement aléatoire) 
        '''
        nbr = int(random.randint(0, 40))

        if len(self.dicoModel) > 0 and len(self.airlines) > 0:
            listKeyModel = self.dicoModel.keys()
            model = random.choice(list(listKeyModel))
            
            listKeyAirlines = self.airlines.keys()
            airlines = random.choice(list(listKeyAirlines))
            
            if nbr == 8:
                self.randomPlane(airlines, model, self.departureList)

            if nbr == 3:
                self.randomPlane(airlines, model, self.arrivalList)


    # DAY / UPDATE
    def newDay(self):
        '''
        réinitialise les listes departureList et arrivalList ainsi que la
        variable du temps, tick
        '''
        self.tick = 0
        self.day += 1
        self.departureList = []
        self.arrivalList = []
        return self.tick, self.day, self.departureList, self.arrivalList

    def updateStatus(self):
        '''
        Met à jour les informations des avions lors d'une nouvelle minute.
        Le carburant des avions à l'atterrissage est diminué en fonction de
        la consomation. Les avions au décollage dont l'heure de départ est
        plus petite que le tick actuel sont notés comme en retard.
        '''
        crashedPlane = []
        delayedPlane = []
        for plane in self.arrivalList:
            # diminution du carburant en fonction de la consomation/tour
            plane.update()

            if plane.isCrashed():  # si l'avion n'a plus de fuel, il se crashe
                passengers = plane.getPassengers()
                plane.setStatut('Crashed')
                self.arrivalList.remove(plane)
                self.historyList.append(plane)
                self.statCrash += 1
                self.statDeath += passengers
                crashedPlane.append(plane)

        for plane in self.departureList:
            if plane.isDelayed(self.tick):
                if plane.getStatut() != 'Delayed':
                    plane.setStatut('Delayed')
                    delayedPlane.append(plane)
        self.tick += 1

        return crashedPlane, delayedPlane


    # TIME (conversion)
    def convTupleToTick(self, tupple):
        '''
        converti un tuple en un entier
        '''
        return int(tupple[0] * 60 + tupple[1])

    def convTickToTuple(self, time):
        '''
        converti l'entier "tick" en un tuple
        '''
        return ((str(time // 60)).rjust(2, '0'),
                (str(time % 60)).rjust(2, '0'))


    # SAVE
    def saveSystem(self, filename):
        '''
        Sauvegarde l'état courant du système à l'aide de json.
        Sauve les modèles, les compangies, le nombre de pistes, les avions (dans
        leurs listes respectives), l'heure et les statistiques de l'aéroport. 
        '''
        saveDeparturePlane = []
        saveArrivalPlane = []
        saveHistoryPlane = []

        for plane in self.departureList:
            savePlane = plane.__dict__
            saveDeparturePlane.append(savePlane)

        for plane in self.arrivalList:
            savePlane = plane.__dict__
            saveArrivalPlane.append(savePlane)

        for plane in self.historyList:
            savePlane = plane.__dict__
            saveHistoryPlane.append(savePlane)

        saveRunways = {"departureRunway": self.departureRunway,
                        "arrivalRunway": self.arrivalRunway,
                        "mixteRunway": self.mixteRunway}

        saveTime = {"time": self.tick, "day": self.day}

        saveStat = {"plane global": self.statPlaneGlobal,
                     "plane dep": self.statPlaneDep,
                     "plane arr": self.statPlaneArr,
                     "passengers": self.statPassengers,
                     "death": self.statDeath,
                     "company": self.statAirlines,
                     "model": self.statModel}

        save = json.dumps({"models": self.dicoModel,
                           "airlines": self.airlines,
                           "runways": saveRunways,
                           "departurePlanes": saveDeparturePlane,
                           "arrivalPlanes": saveArrivalPlane,
                           "history_planes": saveHistoryPlane,
                           "time": saveTime,
                           "stat": saveStat})

        saveFile = open(filename, "w")
        saveFile.write(save)

        return True

    def loadSystem(self, filename):
        '''
        Converti le text du fichier de sauvegarde en données utilisables
        par le simulateur.
        '''
        try:
            saveFile = open(filename, "r")
            save = json.load(saveFile)

            self.dicoModel = save["models"]
            self.airlines = save["airlines"]

            loadRunways = save["runways"]
            self.arrivalRunway = loadRunways["arrivalRunway"]
            self.departureRunway = loadRunways["departureRunway"]
            self.mixteRunway = loadRunways["mixteRunway"]

            loadDeparturePlane = save["departurePlanes"]
            for plane in loadDeparturePlane:
                newplane = Plane.fromjson(plane)
                self.departureList.append(newplane)

            loadArrivalPlane = save["arrivalPlanes"]
            for plane in loadArrivalPlane:
                newplane = Plane.fromjson(plane)
                self.arrivalList.append(newplane)

            loadHistoryPlane = save["history_planes"]
            for plane in loadHistoryPlane:
                newplane = Plane.fromjson(plane)
                self.historyList.append(newplane)

            loadTime = save["time"]
            self.tick = loadTime["time"]
            self.day = loadTime["day"]

            loadStat = save["stat"]
            self.statPlaneGlobal = loadStat["plane global"]
            self.statPlaneDep = loadStat["plane dep"]
            self.statPlaneArr = loadStat["plane arr"]
            self.statPassengers = loadStat["passengers"]
            self.statDeath = loadStat["death"]
            self.statAirlines = loadStat["company"]
            self.statModel = loadStat["model"]
        except:
            print ("Le fichier de sauvegarde est corrompu.")

        return True
