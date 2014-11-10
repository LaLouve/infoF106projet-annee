'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: aiportTerminal.py
'''
import airportFunctions

airport = airportFunctions.Airport()

class Terminal:

    #PLANE
    def askAddPlane(self, planeType):
        '''
        Demande les informations nécéssaires à la création d'un nouvel avion
        '''
        if len(airport.dicoModel) == 0:
            print(
                "\nIl n'y a aucun modèle d'avion enregistré,"
                " veuillez en créer un.")
            model, fuel, consumption, modMaxPass = self.askAddModel()

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
                model = str(
                    input("\nEntrez le nom du modèle souhaité: ")).upper()
                modMaxPass = airport.dicoModel[model][2]
                fuel = airport.dicoModel[model][0]
                consumption = airport.dicoModel[model][1]

            elif answer == 'n':
                model, fuel, consumption, modMaxPass = self.askAddModel()

        ok = False
        print("\nInformations de l'avion:")
        while not ok:
            try:
                letterID = (
                    str(input("\nLes 2 ou 3 premières lettres de l'ID:"))
                ).upper()
                numberID = int(input("les 4 chiffres de l'ID:"))
                ID = (letterID + (str(numberID)))
                company = (str(input('Compagnie:'))).lower()
                passOK = False
                while not passOK:
                    passengers = int(input("Nombre de passagers: "))
                    if passengers > modMaxPass:
                        print(
                            "Le nombre de passagers dépasse"
                            " la capacité de ce modèle d'avion")
                    else:
                        passOK = True
                if planeType == 'departure':
                    heure = int(input('Heure de départ (heure):'))
                    minutes = int(input('minutes:'))
                    time = (heure, minutes)
                    statut = 'In Time'
                else:
                    time = None
                    statut = None
                ok = True
            except:
                print("\nVous avez entré une donnée incorrecte!")
        newplane = airport.create_plane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        airport.add_plane(newplane)
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
                      ': ', str(plane), end=' ')
                self.showTime(plane.getTime())
                if plane.getStatut() is not None:
                    print(plane.getStatut())
                else:
                    print()
                count += 1
                
    def showAllInfo(self):
        '''
        Affiche les ifnormations des avions de toutes les listes
        '''
        print('\n\nDEPARTURE\n')
        self.showPlanesInfo(airport.departureList)

        print('\nARRIVAL\n')
        self.showPlanesInfo(airport.arrival_list)

        print('\nHISTORY\n')
        self.showPlanesInfo(airport.history_list)


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
                str(input("Entrez l'ID de la compagnie (2 ou 3 lettres) :"))
            ).upper()
            if IDletter not in airport.airlines:
                ok = True
            else:
                print('Cet ID est déjà utilisé par une autre compangnie.')

            if (company) not in airport.airlines:
                airport.addAirlines(company, IDletter)
            else:
                print('Cette compangie existe déjà')

    def askDelAirlines(self):
        '''
        suppression d'une compagnie
        '''
        self.showAirlines()
        print(
            "\nEntrez l'ID de la compagnie que vous voulez supprimer:",
            end=' ')
        company_ID = (str(input())).upper()

        if company_ID in airport.airlines:
            airport.delAirlines(company_ID)
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
            company_ID = (
                str(input("\nEntrez l'ID de la compagnie: "))).upper()
            if company_ID in airport.airlines:
                self.showAirlineInfo(company_ID)
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

    def showAirlineInfo(self, company_ID):
        '''
        Afficher les informations d'une compagnie
        '''
        company = airport.airlines[company_ID]
        planeLists = [
            airport.departureList,
            airport.arrival_list,
            airport.history_list]
        count = 1
        for lists in planeLists:
            for plane in lists:
                if plane.getCompany() == company:
                    print('n°' +
                          (str(count)).ljust(2, ' ') +
                          ': ', str(plane), end=' ')
                    self.showTime(plane.getTime())
                    if plane.getStatut() is not None:
                        print(plane.getStatut())
                    else:
                        print()
                    count += 1


    #MODEL
    def showModel(self):
        '''
        Permet d'afficher les différents modèles d'avion enregistrés
        '''
        if len(airport.dicoModel) == 0:
            print("\nIl n'y a aucun modèle enregistré")

        else:
            print('\nListe des modèles enregistrés:')
            count = 1
            print(
                "      {:^10} {:^6} {:^6} {:^10}".format(
                    "Model",
                    "Fuel",
                    "Cons.",
                    "Passengers"))
            listKey = airport.dicoModel.keys()
            for model in listKey:
                fuel = str(airport.dicoModel[model][0])
                consumption = str(airport.dicoModel[model][1])
                passengers = str(airport.dicoModel[model][2])
                print(
                    "n°{:2}: {:^10} {:^6} {:^6} {:^10}".format(
                        count,
                        model,
                        fuel,
                        consumption,
                        passengers))
                count += 1

    def askAddModel(self):
        '''
        Demande d'ajouter un modèle
        '''
        ok = False
        print("\nAjout d'un nouvel d'un nouveau modèle d'avion:")

        while not ok:
            try:
                model = (str(input("Entrez le nom du modèle:"))).upper()
                modFuel = int(input("Fuel:"))
                modConso = int(input("Consommation:"))
                modPass = int(input("Nombre maximum de passagers:"))
                ok = True
            except:
                print(
                    "Vous avez entré une donnée incorrecte,"
                    " veuillez rééssayez.")
        airport.addModel(self, model, modFuel, modConso, modPass)

    def askDelModel(self):
        '''
        Demande de supprimer un modèle
        '''
        self.showModel()
        print(
            "\nEntrez le nom du modèle que vous voulez supprimer:",
            end=' ')
        model = (str(input())).upper()

        if model in self.dicoModel:
            airport.delModel(model)
            print("Le modèle à été supprimé.")
        else:
            print("Vous n'avez pas entré un nom de modèle correct")


    # RANDOM PLANE
    def randomDeparturePlane(self):
        ID, company, passengers, fuel, consumption, model = airport.randomPlane()
        time = (randint(0, 23), randint(0, 59))
        statut = "In Time"
        newPlane = airport.createPlane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        airport.addPlane(newPlane)
        print("\nL'avion",
                newPlane.getID(),
               "a été ajouté à la liste des avions au décollage")

    def randomArrivalPlane(self):
        ID, company, passengers, fuel, consumption, model = airport.randomPlane()
        time = None 
        statut = None
        newPlane = airport.createPlane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        airport.addPlane(newPlane)
        print("\nL'avion",
            newPlane.getID(),
            "a été ajouté à la liste des avions à l'atterissage")


    #RUNWAYS
    def askRunway(self):
        '''
        Demande le nombre de pistes à modifier 
        '''
        ok = False
        while not ok:
            try:
                print("\nEntrez le nombre de pistes souhaitées:")
                nbrDepartureRunway = int(
                    input("Pistes pour le décollage:"))
                nbrArrivalRunway = int(
                    input("Pistes pour l'atterissage:"))
                nbrMixteRunway = int(
                    input("Pistes pour l'atterisssage et le décollage:"))
                ok = True
            except:
                print("\nVous n'avez pas indiqué des valeurs correcte!")

        return (nbrDepartureRunway, nbrArrivalRunway, nbrMixteRunway)

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
            print("Arr. Plane", end='  ')
        else:
            print((str(tick[0])).rjust(2, '0') +
                  'h' +
                  (str(tick[1])).rjust(2, '0'), end='  ')

    def showDay(self):
        '''
        Affiche le numéro du jour
        '''
        print('Jour numéro', airport.day)

    def askTime():
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
                airport.addRunway()
            else:
                airport.loadSystem(filename)
        else:
            airport.addRunway()


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
            "\nNombre de modèles d'avions: {}".format(airport.statAvionGlobal,
                                                      airport.statAvionDep,
                                                      airport.statAvionArr,
                                                      airport.statPassengers,
                                                      airport.statCrash,
                                                      airport.statDeath,
                                                      airport.statCompany,
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
                  "\n\nAjouter un avion au décollage: (A)"
                  "\nAjouter un avion à l'atterrissage: (B)"
                  "\nSupprimer un avion au décollage: (C)"
                  "\nAfficher la liste et les informations des avions en "
                  "attente de décollage ou \nd'atterissage: (D)"
                  "\nGénérer aléatoirement un avion au décollage (E) ou à "
                  "l'atterissage: (F)"
                  "\nAfficher les informations d'une compagnie: (G)"
                  "\nAfficher les compagnies: (H)"
                  "\nAjouter une compagnie: (I)"
                  "\nSupprimer une compagnie: (J)"
                  "\nAfficher les pistes: (K)"
                  "\nAjouter des pistes: (L)"
                  "\nSupprimer des pistes: (M)"
                  "\nAfficher les modèles d'avions: (N)"
                  "\nAjouter un modèle d'avion: (O)"
                  "\nSupprimer un modèle d'avion: (P)"
                  "\nAfficher les statistiques de l'aéroport: (R)"
                  "\nSauvegarde: (S)"
                  "\nRestauration: (T)"
                  "\nQuitter le menu: (Q)"
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
                self.randomDeparturePlane()

            elif answer == 'f':
                self.randomArrivalPlane()
                    
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
                self.addRunway()

            elif answer == 'm':
                self.delRunway()

            elif answer == 'n':
                self.showModel()

            elif answer == 'o':
                self.addModel()

            elif answer == 'p':
                self.delModel()

            elif answer == 'r':
                self.showStatistics()

            elif answer == 's':
                airport.saveSystem("save.txt")

            elif answer == 't':
                airport.loadSystem("save.txt")

            elif answer != 'q':
                print("\nVous n'avez pas entré une lettre correcte, rééssayez")

            else:
                nbrTick = self.askTime()
        return nbrTick
