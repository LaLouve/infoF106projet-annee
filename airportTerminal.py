'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: aiportTerminal.py
'''
import airportFunctions
import random
import os

airport = airportFunctions.Airport()


class Terminal:

    #PLANE
    def askAddPlane(self, planeType):
        '''
        Demande les informations nécéssaires à la création d'un nouvel avion
        '''
        # modèle
        if len(airport.modelList) == 0:
            print(
                "\nIl n'y a aucun modèle d'avion enregistré,"
                " veuillez en créer un.")
            model = self.askAddModel()
            modelName = model.getName()
            modMaxPass = model.getPassenger()
            fuel = model.getFuel()
            consumption = model.getConso()

        else:
            answerOK = False
            while not answerOK:
                answer = str(
                    input("\n"
                          "Voulez-vous utiliser un modèle d'avion enregistré?"
                          " (O)ui/(N)on ")).lower()
                if answer == 'o' or answer == 'n':
                    answerOK = True

            if answer == 'o':
                self.showModel()
                ok = False
                while not ok:
                    try:
                        indice = int(input('Entrez sa position dans'
                                      ' la liste des modèles: ')) - 1
                        if indice < len(airport.modelList) and\
                            indice >= 0:
                            ok = True
                        else:
                            ok = False
                            print("\nVous n'avez pas entré"
                                  " le numéro d'un modèle.")
                    except:
                        ok = False
                        print("\nVous n'avez pas entré un nombre.")

                model = airport.modelList[indice]
                modelName = model.getName()
                modMaxPass = model.getPassenger()
                fuel = model.getFuel()
                consumption = model.getConso()


            elif answer == 'n':
                model = self.askAddModel()
                modelName = model.getName()
                modMaxPass = model.getPassenger()
                fuel = model.getFuel()
                consumption = model.getConso()

        #Informations de l'avion
        ok = False
        print("\nInformations de l'avion:")
        while not ok:
            try:
                letterID = (
                    str(input("\nLes 2 ou 3 premières lettres de l'ID: "))
                ).upper()
                numberID = int(input("les 4 chiffres de l'ID: "))
                ID = (letterID + (str(numberID)))
                company = (str(input('Compagnie: '))).lower()
                passOK = False
                while not passOK:
                    passengers = int(input("Nombre de passagers: "))
                    if passengers > int(modMaxPass):
                        print(
                            "Le nombre de passagers dépasse"
                            " la capacité de ce modèle d'avion.")
                    else:
                        passOK = True
                ok = True

            except:
                print("\nVous avez entré une donnée incorrecte!")

        if planeType == 'departure':
            timeOK = False
            while not timeOK:
                heure = int(input('Heure de départ (heure): '))
                minutes = int(input('minutes: '))
                if 0 <= heure <= 23  and 0 <= minutes <= 59: 
                    time = (heure, minutes)
                    timeOK = True
                else:
                    print("Vous avez entré une heure incorrecte!")
            statut = 'In Time'
        else:
            time = None
            statut = None

        newplane = airport.createPlane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            modelName,
            time,
            statut)
        airport.addPlane(newplane)
        if planeType == 'departure':
            typeText = "au décollage"
        else:
            typeText = "à l'atterrissage"

        print("L'avion {} a été ajouté à la liste des avions {}.".format(
            newplane.getID(),
            typeText))

    def askDelPlane(self):
        if len(airport.departureList) == 0:
            print ("\nIl n'y a pas d'avion à supprimer.")
        else:
            print('\nListe des avions au départ:\n')
            self.showPlanesInfo(airport.departureList)
            print('\nQuel avion voulez-vous supprimer?')

            ok = False
            while not ok:
                try:
                    indice = int(input('Entrez sa position dans'
                                  ' la liste des avions au départ: ')) - 1
                    if indice < len(airport.departureList) and\
                        indice >= 0:
                        ok = True
                    else:
                        ok = False
                        print("\nVous n'avez pas entré"
                              " le numéro d'un avion.")
                except:
                    ok = False
                    print("\nVous n'avez pas entré un nombre.")

            plane = airport.departureList[indice]
            airport.delPlane(plane)
            print("\nL'avion", plane.getID(), "a été supprimé")
 
    def showPlanesInfo(self, planeList):
        '''
        afficher les informations sur les avions
        '''
        if len(planeList) == 0:
            print("la liste est vide")
        else:
            count = 1
            for plane in planeList:
                print('n°' +
                      (str(count)).ljust(2, ' ') +
                      ':', str(plane), end='|')
                self.showTime(plane.getTime())
                if plane.getStatut() is not None:
                    print('|'+ str(plane.getStatut()))
                else:
                    print()
                count += 1
                
    def showAllInfo(self):
        '''
        Affiche les ifnormations des avions de toutes les listes
        '''
        text = "-----{:^9} {:^20} {:^5} {:^7} {:^5} {:^7} {:^5} ".format(
                                                                "ID",
                                                                "Compagnie",
                                                                "Pass.",
                                                                "Fuel",
                                                                "Cons.",
                                                                "Modèle",
                                                                "Time")
        print('\n\nDEPARTURE')
        print(text, " Statut")
        self.showPlanesInfo(airport.departureList)

        print('\nARRIVAL')
        print(text)
        self.showPlanesInfo(airport.arrivalList)

        print('\nHISTORY')
        print(text, " Statut")
        self.showPlanesInfo(airport.historyList)


    #AIRLINES
    def askAddAirlines(self):
        '''
        ajout d'une compangnie au dictionnaire des compagnies
        '''
        ok = False

        while not ok:
            company = (
                str(input("\nEntrez le nom complet de la compagnie"
                          " que vous voulez ajouter: "))).lower()
            IDletter = (
                str(input("Entrez l'ID de la compagnie (2 ou 3 lettres): "))
            ).upper()
            if IDletter not in airport.airlines:
                ok = True
            else:
                print('Cet ID est déjà utilisé par une autre compangnie.')

            if (company) not in airport.airlines:
                airport.addAirlines(company, IDletter)
            else:
                print('Cette compangie existe déjà')
        return IDletter

    def askDelAirlines(self):
        '''
        suppression d'une compagnie
        '''
        self.showAirlines()
        print(
            "\nEntrez l'ID de la compagnie que vous voulez supprimer: ",
            end=' ')
        companyID = (str(input())).upper()

        if companyID in airport.airlines:
            airport.delAirlines(companyID)
        else:
            print("Vous n'avez pas entré un ID correct")
   
    def askAirlinesInfo(self):
        '''
        Demande d'afficher les informations d'une compagnie
        '''
        if len(airport.airlines) == 0:
            print("\nIl n'y a aucune compagnie enregistrée")
        else:
            self.showAirlines()
            companyID = (
                str(input("\nEntrez l'ID de la compagnie: "))).upper()
            if companyID in airport.airlines:
                self.showAirlinesInfo(companyID)
            else:
                print("\nLa compagnie demandée n'est pas enregistrée")
   
    def showAirlines(self):
        '''
        afficher les différentes compagnies existantes avec leur ID
        '''
        if len(airport.airlines) == 0:
            print("\nIl n'y a aucune compagnie enregistrée")
        else:
            print('\nListe des compagnies enregistrées:')
            count = 1
            listKey = airport.airlines.keys()
            for key in listKey:
                print('n°' + (str(count)).ljust(2, ' ') + ': ', end=' ')
                print(str(airport.airlines[key]).center(20, ' '), key)
                count += 1

    def showAirlinesInfo(self, companyID):
        '''
        Afficher les informations d'une compagnie
        '''
        company = airport.airlines[companyID]
        planeLists = [
            airport.departureList,
            airport.arrivalList,
            airport.historyList]
        text = "-----{:^9} {:^20} {:^5} {:^7} {:^7} {:^6} {:^5} ".format(
                                                        "ID",
                                                        "Compagnie",
                                                        "Pass.",
                                                        "Fuel",
                                                        "Cons.",
                                                        "Modèle",
                                                        "Time")
        if len(airport.departureList) > 0 or len(airport.arrivalList) > 0\
            or len(airport.historyList) > 0:
            count = 1
            print('\nListe des avions de la compagnie', company,':')
            print(text, " Statut")
            for lists in planeLists:
                for plane in lists:
                    if plane.getCompany() == company:
                        print('n°' +
                              (str(count)).ljust(2, ' ') +
                              ':', str(plane), end='|')
                        self.showTime(plane.getTime())
                        if plane.getStatut() is not None:
                            print('|' + str(plane.getStatut()))
                        else:
                            print()
                        count += 1
        else:
            print('Cette compagnie n\'a aucun avion.')


    #MODEL
    def showModel(self):
        '''
        Permet d'afficher les différents modèles d'avion enregistrés
        '''
        print("Liste des modèles:")
        text = "----{:^9} {:^9} {:^10} {:^10}".format("Name",
                                              "Fuel",
                                              "Cons.",
                                              "Passagers")
        print(text)

        if len(airport.modelList) == 0:
            print("la liste est vide")
        else:
            count = 1
            for model in airport.modelList:
                print('n°' +
                      (str(count)).ljust(2, ' ') +
                      ':', str(model))
                count += 1

    def askAddModel(self):
        '''
        Demande d'ajouter un modèle
        '''
        ok = False
        print("\nAjout d'un nouvel d'un nouveau modèle d'avion:")

        while not ok:
            try:
                model = (str(input("Entrez le nom du modèle: "))).upper()
                modFuel = int(input("Fuel: "))
                modConso = int(input("Consommation: "))
                modPass = int(input("Nombre maximum de passagers: "))
                ok = True
            except:
                print(
                    "Vous avez entré une donnée incorrecte,"
                    " veuillez rééssayez.")
        newModel = airport.addModel(model, modFuel, modConso, modPass)
        return newModel

    def askDelModel(self):
        '''
        Demande de supprimer un modèle
        '''
        if len(airport.modelList) == 0:
            print ("\nIl n'y a pas de modèle à supprimer.")
        else:
            self.showModel()
            print('\nQuel avion voulez-vous supprimer?')

            ok = False
            while not ok:
                try:
                    indice = int(input('Entrez sa position dans'
                                  ' la liste des modèles: ')) - 1
                    if indice < len(airport.modelList) and\
                        indice >= 0:
                        ok = True
                    else:
                        ok = False
                        print("\nVous n'avez pas entré"
                              " le numéro d'un modèle.")
                except:
                    ok = False
                    print("\nVous n'avez pas entré un nombre.")

            model = airport.modelList[indice]
            airport.delModel(model)
            print("\nLe modèle", model.getName(), "a été supprimé")


    # RANDOM PLANE
    def askRandomPlane(self, planeList):
        '''
        Vérifie si il existe au moins un compagnie et un modèle
        si oui, fait un choix parmis ceux-ci 
        appelle la fonction airport.randomPlane() afin de créer l'avion 
        '''
        if len(airport.modelList) == 0:
            print("\nIl n'y a aucun modèle d'avion enregistré.")
            model = self.askAddModel()

        else:
            indice = random.randint(0, len(airport.modelList))
            model = airport.modelList[indice-1]

        if len(airport.airlines) == 0:
            print("\nIl n'y a aucune compagnie enregistrée.")
            IDletter = self.askAddAirlines()
        else:
            listKeyAirlines = airport.airlines.keys()
            IDletter = random.choice(list(listKeyAirlines))

        newPlane = airport.randomPlane(IDletter, model, planeList)
        
        if planeList == airport.departureList:
            print("\nL'avion",
                    newPlane.getID(),
                    "a été ajouté à la liste des avions au décollage")
        else:
            print("\nL'avion",
                    newPlane.getID(),
                    "a été ajouté à la liste des avions à l'attérissage")


    #RUNWAYS
    def askRunway(self):
        '''
        Demande le nombre de pistes à modifier 
        '''
        ok = False
        while not ok:
            try:
                print("\nEntrez le nombre de pistes souhaitées:")
                nbrDepRunway = int(
                    input("Pistes pour le décollage:"))
                nbrArrRunway = int(
                    input("Pistes pour l'atterissage:"))
                nbrMixteRunway = int(
                    input("Pistes pour l'atterisssage et le décollage:"))
                ok = True
            except:
                print("\nVous n'avez pas indiqué des valeurs correcte!")
        airport.modifRunways(nbrDepRunway, nbrArrRunway, nbrMixteRunway)

    def showRunway(self):
        '''
        Affiche le nombre de pistes de l'aéroport
        '''
        print("\nListe des pistes:")
        print("Pistes pour le décollage:", airport.departureRunway)
        print("Pistes pour l'atterissage:", airport.arrivalRunway)
        print("Pistes mixtes:", airport.mixteRunway)


    # TIME
    def showTime(self, tick):
        '''
        Affiche l'heure au format '00h00'
        '''
        if type(tick) is int:
            print(str(airport.convTickToTuple(tick)[0]) +
                  "h" +
                  str(airport.convTickToTuple(tick)[1]) +
                  ".")
        elif tick is None:
            print("Arri.", end='  ')
        else:
            print((str(tick[0])).rjust(2, '0') +
                  'h' +
                  (str(tick[1])).rjust(2, '0'), end='  ')

    def showDay(self):
        '''
        Affiche le numéro du jour
        '''
        print('Jour numéro', airport.day)

    def askTime(self):
        correct = False
        while not correct:
            try:
                heure = int(
                    input('\nCombien de temps voules-vous passer? (heure):'))
                minutes = int(input('minutes:'))
                correct = True
            except:
                print("\nVous n'avez pas entré un nombre correct!\n")
        return (heure * 60 + minutes)

    
    # SAVE 
    def askNewGame(self, filename):
        '''
        Vérifie si une sauvegarde existe et propose de l'utiliser.
        Si il n'y a pas de sauvegarde, lance le simulateur.
        '''
        saveFile = None
        try:
            saveFile = open(filename, "r")

        except:
            print("\nIl n'y a pas de sauvegarde enregistrée.")

        if saveFile is not None:
            answerOK = False
            while not answerOK:
                answer = str(
                    input("\n"
                          "Voulez-vous utiliser la sauvegarde? (Si non, une nouvelle simulation commencera)"
                          "(O)ui/(N)on\n ")).lower()
                if answer == 'o' or answer == 'n':
                    answerOK = True
            if answer == 'n':
                os.remove(filename)
                self.askRunway()
            else:
                airport.loadSystem(filename)
        else:
            self.askRunway()


    # STATISTICS
    def showStatistics(self):
        '''
        Affiche les différentes statistiques
        '''
        text = "\nNombre total d'avions: {}"\
            "\nNombre d'avions au décollage ou ayant décollés: {}"\
            "\nNombre d'avions à l'atterrissage ou ayant atterri : {}"\
            "\nNombre total de passagers: {}"\
            "\nNombre de crashs: {}"\
            "\nNombre de morts lors des crashs: {}"\
            "\nNombre de compangies: {}"\
            "\nNombre de modèles d'avions: {}".format(airport.statPlaneGlobal,
                                                      airport.statPlaneDep,
                                                      airport.statPlaneArr,
                                                      airport.statPassengers,
                                                      airport.statCrash,
                                                      airport.statDeath,
                                                      airport.statAirlines,
                                                      airport.statModel)
        print(text)

    
    # USER MENU
    def userMenu(self):
        '''
        Menu principal de l'utilisateur.
        Permet le choix des actions à effectuer
        '''
        answer = 0
        while answer != 'q':
            print("\nMenu des actions, que voulez-vous faire?")
            self.showDay()
            print("Il est", end=' ')
            self.showTime(airport.tick)
            print("---------------------------------------------------------"
                  "\n\n-Ajouter un avion au décollage: (A)"
                  "\n-Ajouter un avion à l'atterrissage: (B)"
                  "\n-Supprimer un avion au décollage: (C)"
                  "\n-Afficher la liste et les informations des avions: (D)"
                  "\n-Générer aléatoirement un avion au décollage (E) ou à "
                  "l'atterissage: (F)"
                  "\n\n-Afficher les informations d'une compagnie: (G)"
                  "\n-Afficher les compagnies: (H)"
                  "\n-Ajouter une compagnie: (I)"
                  "\n-Supprimer une compagnie: (J)"
                  "\n\n-Afficher les pistes: (K)"
                  "\n-Modifier le nombre de pistes: (L)"
                  "\n\n-Afficher les modèles d'avions: (M)"
                  "\n-Ajouter un modèle d'avion: (N)"
                  "\n-Supprimer un modèle d'avion: (O)"
                  "\n\n-Afficher les statistiques de l'aéroport: (P)"
                  "\n-Sauvegarde: (S)"
                  "\n-Restauration: (R)"
                  "\n-Quitter le menu: (Q)"
                  "\n---------------------------------------------------------"
                  "\n(Entrez la lettre correpsondant à l'action)")

            answer = (str(input("\nAction choisie: "))).lower()

            if answer == 'a':
                self.askAddPlane("departure")

            elif answer == 'b':
                self.askAddPlane("arrival")

            elif answer == 'c':
                self.askDelPlane()

            elif answer == 'd':
                self.showAllInfo()

            elif answer == 'e':
                self.askRandomPlane(airport.departureList)

            elif answer == 'f':
                self.askRandomPlane(airport.arrivalList)                    
            
            elif answer == 'g':
                self.askAirlinesInfo()
           
            elif answer == 'h':
                self.showAirlines()

            elif answer == 'i':
                self.askAddAirlines()

            elif answer == 'j':
                self.askDelAirlines()

            elif answer == 'k':
                self.showRunway()

            elif answer == 'l':
                self.askRunway()

            elif answer == 'm':
                self.showModel()

            elif answer == 'n':
                self.askAddModel()

            elif answer == 'o':
                self.askDelModel()

            elif answer == 'p':
                self.showStatistics()

            elif answer == 's':
                airport.saveSystem("save.txt")

            elif answer == 'r':
                airport.loadSystem("save.txt")

            elif answer != 'q':
                print("\nVous n'avez pas entré une lettre correcte, rééssayez")

            else:
                nbrTick = self.askTime()
        return nbrTick
