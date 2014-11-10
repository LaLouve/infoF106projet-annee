'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: aiportTerminal.py
'''

class Terminal:

    def ask_for_add_plane(self, plane_type):
        '''
        Demande les informations nécéssaires à la création d'un nouvel avion
        '''
        if len(Airport.dico_model) == 0:
            print(
                "\nIl n'y a aucun modèle d'avion enregistré,"
                " veuillez en créer un.")
            model, fuel, consumption, modMaxPass = Airport.add_model()

        else:
            ansOK = False
            while not ansOK:
                ans = str(
                    input("\n"
                          "Voulez-vous utiliser un modèle d'avion enregistré?"
                          " (O)ui/(N)on ")).lower()
                if ans == 'o' or ans == 'n':
                    ansOK = True

            if ans == 'o':
                Airport.show_model()
                model = str(
                    input("\nEntrez le nom du modèle souhaité: ")).upper()
                modMaxPass = Airport.dico_model[model][2]
                fuel = Airport.dico_model[model][0]
                consumption = Airport.dico_model[model][1]

            elif ans == 'n':
                model, fuel, consumption, modMaxPass = Airport.add_model()

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
                if plane_type == 'departure':
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
        newplane = Airport.create_plane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
        Airport.add_plane(newplane)
        if plane_type == 'departure':
            type_text = "au décollage"
        else:
            type_text = "à l'atterrissage"

        text = "L'avion {} a été ajouté à la liste des avions {}.".format(
            newplane.getID(),
            type_text)
        print(text)


    def ask_for_del_plane(self):
        if len(Airport.departure_list) == 0:
            print ("\nIl n'y a pas d'avion à supprimer.")
        else:
            print('\nListe des avions au départ:\n')
            Airport.show_list_info(Airport.departure_list)
            print('\nQuel avion voulez-vous supprimer?')

            ok = False
            while not ok:
                try:
                    indice = int(input('Entrez sa position dans'
                                  ' la liste des avions au départ: ')) - 1
                    if indice < len(Airport.departure_list) and\
                        indice >= 0:
                        ok = True
                    else:
                        ok = False
                        print("\nVous n'avez pas entré"
                              " le numéro d'un avion.")
                except:
                    ok = False
                    print("\nVous n'avez pas entré un nombre.")

            plane = Airport.departure_list[indice]
            Airport.del_plane(plane)
            print("\nL'avion", plane.getID(), "a été supprimé")


    def ask_add_company(self):
        '''
        ajout d'une compangnie au dictionnaire des compagnies
        '''
        ok = False

        while not ok:
            company = (
                str(input("\nEntrez le nom complet de la compagnie"
                          " que vous voulez ajouter: "))).lower()
            ID_letter = (
                str(input("Entrez l'ID de la compagnie (2 ou 3 lettres) :"))
            ).upper()
            if ID_letter not in Airport.airlines:
                ok = True
            else:
                print('Cet ID est déjà utilisé par une autre compangnie.')

            if (company) not in Airport.airlines:
                Airport.add_company(company, ID_letter)
            else:
                print('Cette compangie existe déjà')
        
        return company, ID_letter

    def show_airlines(self):
        '''
        afficher les différentes compagnies existantes avec leur ID
        '''
        if len(Airport.airlines) == 0:
            print("\nIl n'y a aucune compagnie enregistrée")
        else:
            print('\nListe des compagnies enregistrées:')
            count = 1
            list_keys = Airport.airlines.keys()
            for key in list_keys:
                print('n°' + (str(count)).ljust(2, ' ') + ': ', end=' ')
                print(str(Airport.airlines[key]).center(20, ' '), key)
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
                Airport.showTime(plane.getTime())
                if plane.getStatut() is not None:
                    print(plane.getStatut())
                else:
                    print()
                count += 1

    def show_all_info(self):
        '''
        Affiche les ifnormations des avions de toutes les listes
        '''
        print('\n\nDEPARTURE\n')
        Airport.show_list_info(Airport.departure_list)

        print('\nARRIVAL\n')
        Airport.show_list_info(Airport.arrival_list)

        print('\nHISTORY\n')
        Airport.show_list_info(Airport.history_list)

    def show_airline_info(self, company_ID):
        '''
        Afficher les informations d'une compagnie
        '''
        company = Airport.airlines[company_ID]
        plane_lists = [
            Airport.departure_list,
            Airport.arrival_list,
            Airport.history_list]
        count = 1
        for lists in plane_lists:
            for plane in lists:
                if plane.getCompany() == company:
                    print('n°' +
                          (str(count)).ljust(2, ' ') +
                          ': ', str(plane), end=' ')
                    Airport.showTime(plane.getTime())
                    if plane.getStatut() is not None:
                        print(plane.getStatut())
                    else:
                        print()
                    count += 1