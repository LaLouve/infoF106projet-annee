'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 3

fichier: airportFunctions.py
'''

from random import randint, choice
from plane import Plane


class Airport:

    def __init__(self):
        '''
        initialisation des données
        '''
        self.departure_list = []  # avions en attente de décollage
        self.arrival_list = []  # avions en attente de d'attérissage
        # autres avions (déjà attéri, décollé ou crashé)
        self.history_list = []
        # dictionnaire de toutes les compagnies, avec leur ID
        self.airlines = {}
        # entier représentant les minutes écoulées (min: 0, max: 1439)
        self.tick = 0
        self.departure_runway = 0  # nbr de pistes de décollage
        self.arrival_runway = 0  # nbr de pistes d'atterissage
        self.mixte_runway = 0  # nbr de piste d'atterissage et de décollage
        self.dico_model = {} #dico des différents modèles d'avions

    def create_plane(
            self,
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut):
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
        ID_letter = ID[:-4]
        # ajouter la compagnie au dictionnaire si elle n'y est pas déjà
        if (company) not in self.airlines:
            self.airlines[ID_letter] = company
            return newPlane

    def add_plane(self, plane):
        '''
        ajout d'un avion à departure_list, arrival_list
        '''
        if plane.getTime() is None:
            self.arrival_list.append(plane)

        else:
            self.departure_list.append(plane)

    def del_plane(self, plane):
        '''
        supression d'un avion de departure_list
        '''
        self.departure_list.remove(plane)
        plane.setStatut("Deleted")
        self.history_list.append(plane)

    def add_company(self):
        '''
        ajout d'une compangnie au dictionnaire des compagnies
        '''
        ok = False

        while not ok:
            company = (
                str(input("\nEntrez le nom complet de la compagnie que vous voulez ajouter: "))).lower()
            ID_letter = (
                str(input("Entrez l'ID de la compagnie (2 ou 3 lettres) :"))).upper()
            if ID_letter not in self. airlines:
                ok = True
            else:
                print('Cet ID est déjà utilisé par une autre compangnie.')

            if (company) not in self.airlines:
                self.airlines[ID_letter] = company
            else:
                print('Cette compangie existe déjà')

        return company, ID_letter

    def del_company(self, company_ID):
        print("\nLa compagnie", self.airlines[company_ID], "a été supprimée.")
        self.airlines.pop(company_ID)

    def departure_priority_plane(self):
        '''
        avion le plus prioritaire pour le depart

        [1:] permet de ne pas verifier l'avion prioritaire avec lui même vu qu'il
        est le premier de la liste
        '''
        if len(self.departure_list) == 0:
            most_prior_plane = None

        else:
            most_prior_plane = self.departure_list[0]
            for plane in self.departure_list[1:]:
                if int(plane.getTime()) < most_prior_plane.getTime():
                    most_prior_plane = plane
                if int(plane.getTime()) == most_prior_plane.getTime():
                    if int(plane.getPassengers()) > most_prior_plane.getPassengers():
                        most_prior_plane = plane
        return most_prior_plane

    def arrival_priority_plane(self):
        '''
        avion le plus prioritaire pour l'atterissage

        on divise le niveau de carburant (fuel)par la consommation de carburant
        par tour (consumption), pour obtenir le nombre de tours que l'avion peut
        encore rester en l'air.
        '''
        if len(self.arrival_list) == 0:
            most_prior_plane = None

        else:
            most_prior_plane = self.arrival_list[0]
            for plane in self.arrival_list[1:]:
                if plane.ratio() < most_prior_plane.ratio():
                    most_prior_plane = plane
                    # si le nombre de tour restant est le même, on regarde le
                    # nombre de passagers
                elif plane.ratio() == most_prior_plane.ratio():
                    if plane.getPassengers() > most_prior_plane.getPassengers():
                        most_prior_plane = plane
        return most_prior_plane

    def show_airlines(self):
        '''
        afficher les différentes compagnies existantes avec leur ID
        '''
        if len(self.airlines) == 0:
            print("\nIl n'y a aucune compagnie enregistrée")
        else:
            print('\nListe des compagnies enregistrées:')
            count = 1
            list_keys = self.airlines.keys()
            for key in list_keys:
                print('n°' + (str(count)).ljust(2, ' ') + ': ', end=' ')
                print(str(self.airlines[key]).center(20, ' '), key)
                count += 1

    def show_list_info(self, plane_list):
        '''
        afficher les informations sur les avions
        '''
        if len(plane_list) == 0:
            print("la liste est vide")
        else:
            count = 1
            for plane in plane_list:
                print('n°' +
                      (str(count)).ljust(2, ' ') +
                      ': ', str(plane), end=' ')
                self.showTime(plane.getTime())
                if plane.getStatut() is not None:
                    print(plane.getStatut())
                print()
                count += 1

    def show_all_info(self):
        '''
        Affiche les ifnormations des avions de toutes les listes
        '''
        print('\n\nDEPARTURE\n')
        self.show_list_info(self.departure_list)

        print('\nARRIVAL\n')
        self.show_list_info(self.arrival_list)

        print('\nHISTORY\n')
        self.show_list_info(self.history_list)

    def show_airline_info(self, company_ID):
        '''
        Afficher les informations d'une compagnie
        '''
        company = self.airlines[company_ID]
        plane_lists = [
            self.departure_list,
            self.arrival_list,
            self.history_list]
        count = 1
        for lists in plane_lists:
            for plane in lists:
                if plane.getCompany() == company:
                    print('n°' +
                          (str(count)).ljust(2, ' ') +
                          ': ', str(plane), end=' ')
                    self.showTime(plane.getTime())
                    if plane.getStatut() is not None:
                        print(plane.getStatut())
                    print()
                    count += 1

    def new_day(self):
        '''
        réinitialise les listes departure_list et arrival_list ainsi que la
        variable du temps, tick
        '''
        print("\nNew Day!")
        self.tick = 0
        self.departure_list = []
        self.arrival_list = []
        return self.tick, self.departure_list, self.arrival_list

    def update_status(self):
        '''
        Met à jour les informations des avions lors d'une nouvelle minute.
        Le carburant des avions à l'atterrissage est diminué en fonction de
        la consomation. Les avions au décollage dont l'heure de départ est
        plus petite que le tick actuel sont notés comme en retard.
        '''
        crashedPlane = []
        delayedPlane = []
        for plane in self.arrival_list:
            # diminution du carburant en fonction de la consomation/tour
            plane.update()

            if plane.isCrashed():  # si l'avion n'a plus de fuel, il se crashe
                print(
                    "\nL'avion",
                    plane.getID(),
                    "n'a malheureusement pas pu atterire à temps. \nVous avez tué",
                    plane.getPassengers(),
                    'passagers./o\\')
                plane.setStatut('Crashed')
                self.arrival_list.remove(plane)
                self.history_list.append(plane)
                crashedPlane.append(plane)

        for plane in self.departure_list:
            if plane.isDelayed(self.tick):
                print("\nL'avion", plane.getID(), "Est en retard.")
                plane.setStatut('Delayed')
                delayedPlane.append(plane)
        self.tick += 1

        return crashedPlane, delayedPlane

    def next_event(self):
        '''
        Permet d'effectuer l'action la plus prioritaire. Si il n'y a pas
        d'avion devant décoller, c'est l'avion avec le ratio carburant/
        consomation le plus petit qui attéri.
        Une fois l'action effectuée, l'avion en question est retiré de sa liste
        d'origine et placé dans history_list
        '''
        arrival_plane = self.arrival_priority_plane()
        departure_plane = self.departure_priority_plane()
        most_prior_plane = None

        if arrival_plane is not None and arrival_plane.ratio() == 1:
            most_prior_plane = arrival_plane
            most_prior_plane.setStatut('Landed')
            self.arrival_list.remove(most_prior_plane)
            print("\nL'avion", most_prior_plane.getID(), "a attéri.")

        elif departure_plane is not None and self.convTupleToTick(departure_plane.getTime()) <= self.tick:
            most_prior_plane = departure_plane
            most_prior_plane.setStatut('Take Off')
            self.departure_list.remove(most_prior_plane)
            print("\nL'avion", most_prior_plane.getID(), "a décollé.")

        elif arrival_plane is not None:
            most_prior_plane = arrival_plane
            most_prior_plane.setStatut('Landed')
            self.arrival_list.remove(most_prior_plane)
            print("\nL'avion", most_prior_plane.getID(), "a attéri.")

        if most_prior_plane is not None:
            self.history_list.append(most_prior_plane)

        return (most_prior_plane)

    def next_departure(self):
        departure_plane = self.departure_priority_plane()
        most_prior_plane = None

        if departure_plane is not None and self.convTupleToTick(departure_plane.getTime()) <= self.tick:
            most_prior_plane = departure_plane
            most_prior_plane.setStatut('Take Off')
            self.departure_list.remove(most_prior_plane)
            print("\nL'avion", most_prior_plane.getID(), "a décollé.")

        if most_prior_plane is not None:
            self.history_list.append(most_prior_plane)

        return (most_prior_plane)

    def next_arrival(self):
        departure_plane = self.departure_priority_plane()
        most_prior_plane = None

        arrival_plane = self.arrival_priority_plane()

        if arrival_plane is not None and arrival_plane.ratio() == 1:
            most_prior_plane = arrival_plane
            most_prior_plane.setStatut('Landed')
            self.arrival_list.remove(most_prior_plane)
            print("\nL'avion", most_prior_plane.getID(), "a attéri.")

        elif arrival_plane is not None:
            most_prior_plane = arrival_plane
            most_prior_plane.setStatut('Landed')
            self.arrival_list.remove(most_prior_plane)
            print("\nL'avion", most_prior_plane.getID(), "a attéri.")

        if most_prior_plane is not None:
            self.history_list.append(most_prior_plane)

        return (most_prior_plane)

    def ask_for_runway(self):
        ok = False
        while not ok:
            try:
                print("\nEntrez le nombre de pistes souhaitées:")
                self.nbr_departure_runway = int(input("Pistes pour le décollage:"))
                self.nbr_arrival_runway = int(input("Pistes pour l'atterissage:"))
                self.nbr_mixte_runway = int(
                    input("Pistes pour l'atterisssage et le décollage:"))
                ok = True
            except:
                print("\nVous n'avez pas indiqué des valeurs correcte!")

        return (self.nbr_departure_runway, self.nbr_arrival_runway, self.nbr_mixte_runway)

    def show_runway(self):
        print("\nListe des pistes:")
        print("Pistes pour le décollage:", self.departure_runway)
        print("Pistes pour l'atterissage:", self.arrival_runway)
        print("Pistes mixtes:", self.mixte_runway)

    def add_runway(self):
        self.ask_for_runway()

        self.departure_runway += self.nbr_departure_runway
        self.arrival_runway += self.nbr_arrival_runway
        self.mixte_runway += self.nbr_mixte_runway

        return (self.departure_runway, self.arrival_runway, self.mixte_runway)

    def del_runway(self):
        self.ask_for_runway()

        self.departure_runway -= self.nbr_departure_runway
        self.arrival_runway -= self.nbr_arrival_runway
        self.mixte_runway -= self.nbr_mixte_runway

        if self.departure_runway < 0:
            self.departure_runway = 0

        if self.arrival_runway < 0:
            self.arrival_runway = 0

        if self.mixte_runway < 0:
            self.mixte_runway = 0

        return (self.departure_runway, self.arrival_runway, self.mixte_runway)

    def add_model(self):
        '''
        permet d'ajouter un nouveau modèle d'avion
        '''
        ok = False
        print ("\nAjout d'un nouvel d'un nouveau modèle d'avion:")

        while not ok:
            try:
                model = (str(input("Entrez le nom du modèle:"))).upper()
                modFuel = int(input("Fuel:"))
                modConso = int(input("Consommation:"))
                modPass = int(input("Nombre maximum de passagers:"))
                ok = True
            except:
                print ("Vous avez entré une donnée incorrecte, veuillez rééssayez.")

        modCar = [modFuel, modConso, modPass] #liste des caractéristique du modèle
        self.dico_model[model] = modCar

        return model, modFuel, modConso, modPass

    def del_model(self):
        self.show_model()
                print(
                    "\nEntrez le nom du modèle que vous voulez supprimer:",
                    end=' ')
                model = (str(input())).upper()

                if model in self.dico_model:
                    del self.dico_model[model]
                    print ("Le modèle à été supprimé.")
                else:
                    print("Vous n'avez pas entré un ID correct")
    
    def show_model(self):
        if len(self.dico_model) == 0:
            print("\nIl n'y a aucun modèle enregistré")
        else:
            print('\nListe des modèles enregistrés:')
            count = 1
            print ("      {:^10} {:^6} {:^6} {:^10}".format("Model", "Fuel", "Cons.", "Passengers"))
            list_keys = self.dico_model.keys()
            for model in list_keys:
                fuel = str(self.dico_model[model][0])
                consumption = str(self.dico_model[model][1])
                passengers = str(self.dico_model[model][2])
                print("n°{:2}: {:^10} {:^6} {:^6} {:^10}".format(count, model, fuel, consumption, passengers))
                count += 1

    def add_random_departure_plane(self):
        '''
        Permet la création d'un avion au départ avec des données aléatoires.
        Si il n'y a aucune compagnie aérienne enregistrée, des informations
        sont demandées à l'utilisateur afin d'en créer une nouvelle.
        '''
        if len(self.dico_model) == 0:
            print("\nIl n'y a aucun modèle d'avion enregistré, veuillez en entrer un manuellement")

            model, fuel, consumption, maxPass = self.add_model()
            passengers = randint(1, maxPass)

        else:
            list_key_model = self.dico_model.keys()
            model = choice(list(list_key_model))

            modMaxPass = self.dico_model[model][2]
            passengers = randint(1, modMaxPass)
            fuel = self.dico_model[model][0]
            consumption = self.dico_model[model][1]

        if len(self.airlines) == 0:
            print(
                "\nIl n'y a aucune compagnie enregistrée, veuillez en entrer une manuellement")

            company, ID_letter = self.add_company()

            number = str(randint(1, 9999))
            ID_number = number.rjust(4, '0')
            ID = (ID_letter + ID_number)

        else:
            list_key_airline = self.airlines.keys()
            airlines_key = choice(list(list_key_airline))
            company = self.airlines[airlines_key]
            number = str(randint(1, 9999))
            ID_number = number.rjust(4, '0')
            ID = (airlines_key + ID_number)

        time = (randint(0, 23), randint(0, 59))
        statut = None
        newPlane = self.create_plane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        self.add_plane(newPlane)
        return newPlane

    def add_random_arrival_plane(self):
        '''
        Permet la création d'un avion à l'arrivée avec des données aléatoires.
        Si il n'y a aucune compagnie aérienne enregistrée, des informations
        sont demandées à l'utilisateur afin d'en créer une nouvelle.
        '''
        if len(self.dico_model) == 0:
            print("\nIl n'y a aucun modèle d'avion enregistré, veuillez en entrer un manuellement")

            model, fuel, consumption, maxPass = self.add_model()
            passengers = randint(1, maxPass)

        else:
            list_key_model = self.dico_model.keys()
            model = choice(list(list_key_model))

            modMaxPass = self.dico_model[model][2]
            passengers = randint(1, modMaxPass)
            fuel = self.dico_model[model][0]
            consumption = self.dico_model[model][1]

        if len(self.airlines) == 0:
            print(
                "\nIl n'y a aucune compagnie enregistrée, veuillez en entrer une manuellement")

            company, ID_letter = self.add_company()

            number = str(randint(1, 9999))
            ID_number = number.rjust(4, '0')
            ID = (ID_letter + ID_number)

        else:
            list_key_airline = self.airlines.keys()
            airlines_key = choice(list(list_key_airline))
            company = self.airlines[airlines_key]
            number = str(randint(1, 9999))
            ID_number = number.rjust(4, '0')
            ID = (airlines_key + ID_number)

        time = None
        statut = None
        newPlane = self.create_plane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        self.add_plane(newPlane)
        return newPlane

    def convTupleToTick(self, tupple):
        return (tupple[0] * 60 + tupple[1])

    def convTickToTuple(self, time):
        return ((str(time // 60)).rjust(2, '0'),
                (str(time % 60)).rjust(2, '0'))

    def showTime(self, tick):
        if type(tick) is int:
            print(str(self.convTickToTuple(tick)[0]) +
                  "h" +
                  str(self.convTickToTuple(tick)[1]) +
                  ".")
        elif tick is None:
            print("Arr. Plane", end='  ')
        else:
            print((str(tick[0])).rjust(2, '0') +
                  'h' +
                  (str(tick[1])).rjust(2, '0'), end='  ')

    def user_menu(self):
        '''
        Menu principal de l'utilisateur. Permet le choix des actions à effectuer
        '''
        answer = 0
        while answer != 'q':
            print("\nMenu des actions, que voulez-vous faire?"
                  "\nIl est", end=' ')
            self.showTime(self.tick)
            print("---------------------------------------------------------"
                  "\n\nAjouter un avion au décollage: (A)"
                  "\nAjouter un avion à l'atterrissage: (B)"
                  "\nSupprimer un avion au décollage: (C)"
                  "\nAfficher la liste et les informations des avions en "
                  "attente de décollage ou \nd'atterissage: (D)"
                  "\nAfficher les informations d'une compagnie: (E)"
                  "\nGénérer aléatoirement un avion au décollage (F) ou à "
                  "l'atterissage: (G)"
                  "\nAfficher les compagnies: (H)"
                  "\nAjouter une compagnie: (I)"
                  "\nSupprimer une compagnie: (J)"
                  "\nAfficher les pistes: (K)"
                  "\nAjouter des pistes: (L)"
                  "\nSupprimer des pistes: (M)"
                  "\nAfficher les modèles d'avions: (N)"
                  "\nAjouter un modèle d'avion: (O)"
                  "\nSupprimer un modèle d'avion: (P)"
                  "\nQuitter le menu: (Q)"
                  "\n---------------------------------------------------------"
                  "\n(Entrez la lettre correpsondant à l'action)")

            answer = (str(input("\nAction choisie: "))).lower()

            if answer == 'a':
                ok = False
                while not ok:
                    try:
                        letterID = (
                            str(input("\nLes 2 ou 3 premières lettres de l'ID:"))).upper()
                        numberID = int(input("les 4 chiffres de l'ID:"))
                        ID = (letterID + (str(numberID)))
                        company = (str(input('Compagnie:'))).lower()
                        passengers = int(input('Nombre de passagers:'))
                        fuel = int(input('Quantité de carburant:'))
                        consumption = int(input('Consommation de carburant:'))
                        heure = int(input('Heure de départ (heure):'))
                        minutes = int(input('minutes:'))
                        time = (heure, minutes)
                        ok = True
                    except:
                        print("\nVous avez entré une donnée incorrecte!")
                statut = None
                newplane = self.create_plane(
                    ID,
                    company,
                    passengers,
                    fuel,
                    consumption,
                    time,
                    statut)
                self.add_plane(newplane)
                print(
                    "\nL'avion",
                    newplane.getID(),
                    "a été ajouté à la liste des avions au décollage")

            elif answer == 'b':
                ok = False
                while not ok:
                    try:
                        letterID = (
                            str(input("\nLes 2 ou 3 premières lettres de l'ID:"))).upper()
                        numberID = int(input("les 4 chiffres de l'ID:"))
                        ID = (letterID + (str(numberID)))
                        company = str(input('Compagnie:'))
                        passengers = int(input('Nombre de passagers:'))
                        fuel = int(input('Quantité de carburant:'))
                        consumption = int(input('Consommation de carburant:'))
                        ok = True
                    except:
                        print('Vous avez entré une donnée incorrecte!')

                time = None
                statut = None
                newplane = self.create_plane(
                    ID,
                    company,
                    passengers,
                    fuel,
                    consumption,
                    time,
                    statut)
                self.add_plane(newplane)
                print(
                    "\nL'avion",
                    newplane.getID(),
                    "a été ajouté à la liste des avions à l'atterissage")

            elif answer == 'c':
                print('\nListe des avions au départ:\n')
                self.show_list_info(self.departure_list)
                print('\nQuel avion voulez-vous supprimer?')

                ok = False
                while not ok:
                    try:
                        indice = (
                            int(input('Entrez sa position dans la liste des avions au départ: ')) - 1)
                        if indice <= (len(self.departure_list)) and indice >= 0:
                            ok = True
                        else:
                            ok = False
                            print(
                                "\nVous n'avez pas entré le numéro d'un avion.")
                    except:
                        print("\nVous n'avez pas entré un nombre.")

                plane = self.departure_list[indice]
                self.del_plane(plane)
                print("\nL'avion", plane.getID(), "a été supprimé")

            elif answer == 'd':
                self.show_all_info()

            elif answer == 'e':
                if len(self.airlines) == 0:
                    print("\nIl n'y a aucune compagnie enregistrée")
                else:
                    company_ID = (
                        str(input("\nEntrez l'ID de la compagnie: "))).upper()
                    if company_ID in self.airlines:
                        self.show_airline_info(company_ID)
                    else:
                        print("\nLa compagnie demandée n'est pas enregistrée")

            elif answer == 'f':
                newPlane = self.add_random_departure_plane()
                print(
                    "\nL'avion",
                    newPlane.getID(),
                    "a été ajouté à la liste des avions au décollage")

            elif answer == 'g':
                newPlane = self.add_random_arrival_plane()
                print(
                    "\nL'avion",
                    newPlane.getID(),
                    "a été ajouté à la liste des avions à l'atterissage")

            elif answer == 'h':
                self.show_airlines()

            elif answer == 'i':
                self.add_company()

            elif answer == 'j':
                self.show_airlines()
                print(
                    "\nEntrez l'ID de la compagnie que vous voulez supprimer:",
                    end=' ')
                company_ID = (str(input())).upper()

                if company_ID in self.airlines:
                    self.del_company(company_ID)
                else:
                    print("Vous n'avez pas entré un ID correct")

            elif answer == 'k':
                self.show_runway()

            elif answer == 'l':
                self.add_runway()

            elif answer == 'm':
                self.del_runway()

            elif answer == 'n':
                self.show_model()

            elif answer == 'o':
                self.add_model()

            elif answer == 'p':
                self.del_model()

            elif answer != 'q':
                print("\nVous n'avez pas entré une lettre correcte, rééssayez")

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
