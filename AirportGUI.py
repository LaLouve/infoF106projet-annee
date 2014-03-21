'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 3

fichier: AirportGUI.py
'''

from tkinter import *
# permet la mise en forme des textes des label, boutons, ect. par exemple
# changer la taille et la police d'écriture
import tkinter.font as tkFont
import airportFunctions
from plane import Plane
from tkinter import messagebox as tkm

airport = airportFunctions.Airport()
plane1 = Plane('EX1234', 'Exemple Airline', 100, 2000, 15, None, None)
plane2 = Plane('EX2345', 'Exemple Airline', 150, 1500, 10, (10, 20), 'In Time')
plane3 = Plane('EX3456', 'Exemple Airline', 200, 2500, 20, None, 'Take Off')
airport.arrival_list = [plane1]
airport.departure_list = [plane2]
airport.history_list = [plane3]
airport.airlines = {'EX': 'Exemple Airline'}


class AirportGUI:
    airport = airportFunctions.Airport()

    # Création de la fenêtre principale ###
    def __init__(self, root):
        '''
        Créée l'affichage de la fenêtre principale
        la première ligne permet de désactiver par défaut le bouton "del"
        de la deuxième colonne (c'est à dire le rendre inactif tant que
        l'utilisateur ne selectionne pas un avion dans la liste des avions
        au départ
        '''
        root.bind("<Button-1>", self.checkPlaneDelete)
        self.root = root

        ####### colonne 1 #########
        column1 = Frame(root, bd=3, bg='white')
        column1.pack(side=LEFT)
        Label(
            column1,
            bd=7,
            bg='white',
            text="ARRIVALS",
            font=tkFont.Font(
                size=12)).pack()

        list_box_area = Frame(
            column1,
            bd=8,
            bg='white')  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            list_box_area,
            bg='#C0C0C0',
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.list_box_arrivals = Listbox(
            list_box_area,
            height=25,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.list_box_arrivals.bind("<Double-Button-1>", self.infoArrivalPlane)
        for plane in airport.arrival_list:
            self.list_box_arrivals.insert(END, plane.getID())
        scrollbar.config(command=self.list_box_arrivals.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        list_box_area.pack()
        self.list_box_arrivals.pack()

        Button(
            column1,
            text="Add",
            relief=GROOVE,
            bg='#C0C0C0',
            command=self.addArrivalButton).pack(
            side=LEFT)
        Button(
            column1,
            text="Add Random",
            relief=GROOVE,
            bg='#C0C0C0',
            command=self.addArrivalRandom).pack(
            side=LEFT)

        ####### colonne 2 #########
        column2 = Frame(root, bd=3, bg='white')  # création de la colonne
        column2.pack(side=LEFT)
        Label(
            column2,
            bd=7,
            bg='white',
            text="DEPARTURES",
            font=tkFont.Font(
                size=12)).pack()

        list_box_area = Frame(
            column2,
            bd=8,
            bg='white')  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            list_box_area,
            bg='#C0C0C0',
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.list_box_departures = Listbox(
            list_box_area,
            height=25,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.list_box_departures.bind(
            "<<ListboxSelect>>",
            self.checkPlaneDelete)
        self.list_box_departures.bind(
            "<Double-Button-1>",
            self.infoDeparturePlane)
        for plane in airport.departure_list:
            self.list_box_departures.insert(END, plane.getID())
        scrollbar.config(command=self.list_box_departures.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        list_box_area.pack()
        self.list_box_departures.pack()

        Button(
            column2,
            text="Add",
            relief=GROOVE,
            bg='#C0C0C0',
            command=self.addDepartureButton).pack(
            side=LEFT)
        Button(
            column2,
            text="Add Random",
            relief=GROOVE,
            bg='#C0C0C0',
            command=self.addDepartureRandom).pack(
            side=LEFT)
        self.delPlaneButton = Button(
            column2,
            text="Del",
            relief=GROOVE,
            bg='#C0C0C0',
            state=DISABLED,
            command=self.deletePlaneButton)
        self.delPlaneButton.pack(side=LEFT)

        ####### colonne 3 #########
        column3 = Frame(root, bd=6, bg='white')
        column3.pack()
        self.column_time = column3

        # partie haute de la troisième colonne, contient l'heure et le bouton
        # step
        column3_partTOP = Frame(column3, height=220, bg='white')
        column3_partTOP.pack(side=TOP)
        self.general_time = self.time(airport.tick)
        self.clock = Label(
            column3_partTOP,
            bd=6,
            bg='white',
            text=self.general_time,
            font=tkFont.Font(
                size=16))
        self.clock.pack(side=TOP)

        setTime = Frame(
            column3_partTOP,
            bd=4,
            bg='white')  # entrée du temps et bouton step
        setTime.pack()
        self.nbr_min = Entry(
            setTime,
            bg='white',
            justify=CENTER,
            relief=SUNKEN,
            bd=2,
            width=6)
        self.nbr_min.pack(side=LEFT)
        Label(setTime, bg='white', text='min').pack(side=RIGHT)
        Button(
            column3_partTOP,
            text='Step',
            relief=GROOVE,
            width=6,
            bg='#C0C0C0',
            command=lambda: self.stepButton(
                self.nbr_min.get())).pack(
            side=BOTTOM)

        #partie centrale de la troisième colonne, contient les informations
        #des pistes 
        frame_adjust = Frame(column3, height=50, bg='white').pack()
        column3_partCENTER = Frame(column3, height=220, bg='white')
        column3_partCENTER.pack(side=TOP)

        label_principal = LabelFrame(
            column3_partCENTER,
            bd=4,
            relief=RIDGE,
            bg='white',
            text='Runways',
            font=tkFont.Font(
                size=10))
        label_principal.pack()

        departure_frame = Frame(label_principal, bd=6, bg='white')
        departure_frame.pack(side=TOP)
        text_departure_label = "Departure runways: {}".format(
            airport.departure_runway)
        self.departure_label = Label(
            departure_frame,
            bd=3,
            bg='white',
            text=text_departure_label)
        self.departure_label.pack(side=RIGHT)
        self.departure_label.bind("<Double-Button-1>", self.mod_depRunway_button)

        arrival_frame = Frame(label_principal, bd=6, bg='white')
        arrival_frame.pack(side=TOP)
        text_arrival_label = "Arrival runways: {}".format(
            airport.arrival_runway)
        self.arrival_label = Label(
            arrival_frame,
            bd=3,
            bg='white',
            text=text_arrival_label)
        self.arrival_label.pack(side=RIGHT)
        self.arrival_label.bind("<Double-Button-1>", self.mod_arrRunway_button)

        mixte_frame = Frame(label_principal, bd=6, bg='white')
        mixte_frame.pack(side=TOP)
        text_mixte_label = "Mixte runways: {}".format(airport.mixte_runway)
        self.mixte_label = Label(
            mixte_frame,
            bd=3,
            bg='white',
            text=text_mixte_label)
        self.mixte_label.pack(side=RIGHT)
        self.mixte_label.bind("<Double-Button-1>", self.mod_mixRunway_button)

        frame_adjust2 = Frame(column3, height=50, bg='white').pack()

        # partie basse de la troisième colonne, contient les boutons "history",
        # "companies" et "help"
        column3_partBOTTOM = Frame(column3, height=220, bd=20, bg='white')
        column3_partBOTTOM.pack(side=BOTTOM)
        Button(
            column3_partBOTTOM,
            text='Help',
            relief=GROOVE,
            width=12,
            bg='#C0C0C0',
            command=self.helpButton).pack(
            side=BOTTOM)
        Button(
            column3_partBOTTOM,
            text='History',
            relief=GROOVE,
            width=12,
            bg='#C0C0C0',
            command=self.historyButton).pack(
            side=BOTTOM)
        Button(
            column3_partBOTTOM,
            text='Companies',
            relief=GROOVE,
            width=12,
            bg='#C0C0C0',
            command=self.companiesButton).pack(
            side=BOTTOM)
        #Button(
        #   column3_partBOTTOM,
        #    text='Runway',
        #    relief=GROOVE,
        #    width=12,
        #    bg='#C0C0C0',
        #    command=self.runwayButton).pack(
        #    side=BOTTOM)

    ### Fonctions d'ajout et de suppression d'avions ###
    def addButton(self, title, list_plane, list_box):
        '''
        Ouvre une fenêtre demandant les différentes informations pour
        l'ajout d'un avion
        '''
        self.add_window = Tk()
        self.add_window.title(title)
        self.add_window.configure(background='white')
        self.add_window.resizable(width=FALSE, height=FALSE)

        add_frame = Frame(
            self.add_window,
            bd=15,
            bg='white')  # frame principale
        add_frame.pack()

        Label(add_frame, bd=4, bg='white', text='ID').grid(row=0, column=0)
        Id_frame = Frame(
            add_frame,
            bd=4,
            bg='white')  # frame secondaire, contient l'entrée de l'ID
        Id_frame.grid(row=0, column=1)
        ID_letter = Entry(
            Id_frame,
            bd=2,
            bg='white',
            textvariable=str,
            justify=CENTER,
            relief=SUNKEN,
            width=5)
        ID_letter.grid(row=0, column=0)
        ID_number = Entry(
            Id_frame,
            bd=2,
            bg='white',
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=7)
        ID_number.grid(row=0, column=1)

        Label(
            add_frame,
            bd=4,
            bg='white',
            text='Company').grid(
            row=1,
            column=0)
        company = Entry(
            add_frame,
            bd=2,
            bg='white',
            textvariable=str,
            justify=CENTER,
            relief=SUNKEN,
            width=13)
        company.grid(row=1, column=1)

        Label(
            add_frame,
            bd=4,
            bg='white',
            text='Passengers').grid(
            row=2,
            column=0)
        passengers = Entry(
            add_frame,
            bd=2,
            bg='white',
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=13)
        passengers.grid(row=2, column=1)

        Label(add_frame, bd=4, bg='white', text='Fuel').grid(row=3, column=0)
        fuel = Entry(
            add_frame,
            bd=2,
            bg='white',
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=13)
        fuel.grid(row=3, column=1)

        Label(
            add_frame,
            bd=4,
            bg='white',
            text='Consumption').grid(
            row=4,
            column=0)
        consumption = Entry(
            add_frame,
            bd=2,
            bg='white',
            textvariable=int,
            justify=CENTER,
            relief=SUNKEN,
            width=13)
        consumption.grid(row=4, column=1)

        if list_plane == airport.departure_list:
            Label(
                add_frame,
                bd=4,
                bg='white',
                text='Time').grid(
                row=5,
                column=0)
            time_frame = Frame(
                add_frame,
                bd=4,
                bg='white')  # frame secondaire, contient l'entrée de l'heure
            time_frame.grid(row=5, column=1)
            heure = Entry(
                time_frame,
                bd=2,
                bg='white',
                textvariable=int,
                justify=CENTER,
                relief=SUNKEN,
                width=6)
            heure.grid(row=0, column=0)
            minute = Entry(
                time_frame,
                bd=2,
                bg='white',
                textvariable=int,
                justify=CENTER,
                relief=SUNKEN,
                width=6)
            minute.grid(row=0, column=1)
        else:
            heure = None
            minute = None

        statut = None

        Button(
            add_frame,
            text="Add",
            relief=GROOVE,
            bg='#C0C0C0',
            command=lambda: self.get_plane(
                ID_letter,
                ID_number,
                company,
                passengers,
                fuel,
                consumption,
                heure,
                minute,
                statut,
                list_box)).grid(
            row=7,
            column=1)

    def get_plane(
            self,
            ID_letter,
            ID_number,
            company,
            passengers,
            fuel,
            consumption,
            heure,
            minute,
            statut,
            list_box):
        '''
        Ajoute l'avion créé par l'utilisateur dans sa liste
        (airport.departure_list ou airport.arrival_list), détruit la fenêtre
        des entry et fait apparaitre un message signalant quel avion a
        été ajouté
        '''
        letter_ID = (ID_letter.get()).upper()
        number_ID = ID_number.get()
        name_company = (company.get()).lower()
        nbr_passengers = passengers.get()
        nbr_fuel = fuel.get()
        nbr_consumption = consumption.get()

        if len(letter_ID) >= 2 and len(letter_ID) <= 3 and len(number_ID) == 4:
            if number_ID.isdigit() and nbr_passengers.isdigit() and\
                    nbr_fuel.isdigit() and nbr_consumption.isdigit():
                ID = (str(letter_ID) + str(number_ID))
                if heure is not None and minute is not None:
                    nbr_heure = heure.get()
                    nbr_minute = minute.get()
                    if nbr_heure.isdigit() and nbr_minute.isdigit():
                        if int(nbr_heure) >= 0 and int(nbr_heure) <= 23 and int(nbr_minute) >= 0 and int(nbr_minute) <= 59:
                            time = (
                                str(nbr_heure).rjust(
                                    2, '0'), str(nbr_minute).rjust(
                                    2, '0'))
                            plane = airport.create_plane(
                                ID,
                                name_company,
                                nbr_passengers,
                                nbr_fuel,
                                nbr_consumption,
                                time,
                                statut)
                            airport.add_plane(plane)
                            text = "L'avion {} a été ajouté".format(
                                plane.getID())
                            message = tkm.showinfo('Plane Added', text)
                            list_box.insert(END, plane.getID())
                            self.add_window.destroy()
                        else:
                            text = "Les données entrées ne sont pas correctes!\nVeuillez les vérifier"
                            message = tkm.showerror('Error', text)
                    else:
                        text = "Les données entrées ne sont pas correctes!\nVeuillez les vérifier"
                        message = tkm.showerror('Error', text)
                else:
                    time = None
                    plane = airport.create_plane(
                        ID,
                        name_company,
                        nbr_passengers,
                        nbr_fuel,
                        nbr_consumption,
                        time,
                        statut)
                    airport.add_plane(plane)
                    text = "L'avion {} a été ajouté".format(plane.getID())
                    message = tkm.showinfo('Plane Added', text)
                    list_box.insert(END, plane.getID())
                    self.add_window.destroy()
            else:
                text = "Les données entrées ne sont pas correctes!\nVeuillez les vérifier"
                message = tkm.showerror('Error', text)
        else:
            text = "Les données entrées ne sont pas correctes!\nVeuillez les vérifier"
            message = tkm.showerror('Error', text)

    def addDepartureButton(self):
        '''
        ajoute un avion dans la liste des départs
        '''
        plane = self.addButton(
            "Add Departure Plane",
            airport.departure_list,
            self.list_box_departures)

    def addArrivalButton(self):
        '''
        Ajoute un avion dans la liste des arrivées
        '''
        plane = self.addButton(
            "Add Arrival Plane",
            airport.arrival_list,
            self.list_box_arrivals)

    def addDepartureRandom(self):
        '''
        Ajoute un avion aléatoire au départ
        '''
        if len(airport.airlines) == 0:
            self.addCompany()
        plane = airport.add_random_departure_plane()
        self.list_box_departures.insert(END, plane.getID())
        text = "L'avion {} a été ajouté".format(plane.getID())
        message = tkm.showinfo('Plane Added', text)

    def addArrivalRandom(self):
        '''
        Ajoute un avion aléatoire à l'arrivée
        '''
        if len(airport.airlines) == 0:
            self.addCompany()
        plane = airport.add_random_arrival_plane()
        self.list_box_arrivals.insert(END, plane.getID())
        text = "L'avion {} a été ajouté".format(plane.getID())
        message = tkm.showinfo('Plane Added', text)

    def deletePlaneButton(self):
        '''
        Supprime l'avion choisi par un simple clic dans la liste des avions
        au départ
        '''
        item = self.list_box_departures.curselection()
        self.list_box_departures.delete(item)
        numPlane = item[0]
        plane = airport.departure_list[numPlane]
        airport.del_plane(plane)
        text = "L'avion {} a été supprimé".format(plane.getID())
        message = tkm.showwarning("Plane deleted", text)

    def checkPlaneDelete(self, event=None):
        '''
        Vérifie si un avion est sélectionné dans la liste des avions
        au départ et rend le boutton 'del' actif si oui
        '''
        if self.list_box_departures.curselection():
            self.delPlaneButton.configure(state=NORMAL)
        else:
            self.delPlaneButton.configure(state=DISABLED)

    ### Fonction d'affichage de l'aide ###
    def helpButton(self):
        '''
        Affiche une fenêtre contenant le texte d'aide
        '''
        text_help = Tk()
        text_help.title("Help")
        text_help.config(bg='white')
        Label(
            text_help,
            bd=6,
            bg='white',
            text="Bienvenue dans le simulateur de gestion d'aéroport",
            font=tkFont.Font(
                size=9)).pack(
            side=TOP)

        text = (
            "Fonctionnement du programme:"
            "\n\n\n La fenêtre principale est divisée en trois colonne contenant:"
            "\n*les avions à l'arrivée "
            "\n*les avions au départ "
            "\n*l'heure et différents boutons utiles au fonctionnement du programme."
            "\n\n\nFonctions des différents boutons: "
            "\n\n*'Add': Permet d'ajouter manuellement un avion. Il vous faudra "
            "entrer toutes les informations de cet avion "
            "\n\n*'Add Random': Permet d'ajouter un nouvel avion avec des données aléatoires "
            "\n\n*'Del': Permet de supprimer un avion au décollage uniquement "
            "\n\n*'Step': Permet d'avancer le temps de la simulation et d'exécuter "
            "l'événement suivant. Si vous n'indiquez pas de nombre, le programme "
            "passe 1 minute"
            "\n\n*'History': Affiche la liste de tous les avions passés"
            "\n\n*'Company': Affiche la liste des compagnies aériennes. Cette "
            "fenêtre permet aussi d'ajouter ou de supprimer des compagnies"
            "\n\n\nLorsque vous double-cliquez sur un avion, cela affiche une fenêtre  "
            "contenant toutes les informations de cet avion"
            "\nDe même lorsque vous double-cliquez sur une compagnie, cela  "
            "affiche tous les avions de cette compagnie")

        message = Message(
            text_help,
            text=text,
            bd=5,
            bg='white',
            anchor=CENTER)
        message.pack()

    ### Fonction d'affichage de l'history list ###
    def historyButton(self):
        '''
        Affiche la liste "history" dans une nouvelle fenêtre
        '''
        history_window = Tk()
        history_window.title("History List")
        history_window.config(bg='white')
        history_window.resizable(width=FALSE, height=FALSE)

        column = Frame(
            history_window,
            bd=3,
            bg='white')  # création de la colonne
        column.pack(side=LEFT)
        Label(
            column,
            bd=7,
            bg='white',
            text='History',
            font=tkFont.Font(
                size=12)).pack()

        list_box_area = Frame(
            column,
            bd=8,
            bg='white')  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            list_box_area,
            bg='#C0C0C0',
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.list_box_history = Listbox(
            list_box_area,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.list_box_history.bind("<Double-Button-1>", self.infoHistoryPlane)
        for plane in airport.history_list:
            text = (str(plane.getID()).ljust(12, ' ') + str(plane.getStatut()))
            self.list_box_history.insert(END, text)
        scrollbar.config(command=self.list_box_history.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        list_box_area.pack()
        self.list_box_history.pack()

    ### Fonctions d'affichages et de modifications des compagnies ###
    def companiesButton(self):
        '''
        Affiche la liste des compangines dans une nouvelle fenêtre ainsi
        que les bouttons d'ajout et de suppression
        Un double clic sur une des compagnies fait apparaître une nouvelle
        fenêtre avec la liste des avions de cette compagnie
        '''
        airlines_window = Tk()
        airlines_window.title("Companies")
        airlines_window.config(bg='white')
        airlines_window.bind("<Button-1>", self.checkCompanyDelete)
        airlines_window.resizable(width=FALSE, height=FALSE)

        column = Frame(
            airlines_window,
            bd=3,
            bg='white')  # création de la colonne
        column.pack(side=LEFT)
        self.column_company = column
        Label(
            column,
            bd=7,
            bg='white',
            text='Companies',
            font=tkFont.Font(
                size=12)).pack()

        list_box_area = Frame(
            column,
            bd=8,
            bg='white')  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            list_box_area,
            bg='#C0C0C0',
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.list_box_company = Listbox(
            list_box_area,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.list_box_company.bind("<Double-Button-1>", self.showInfoCompany)
        self.list_box_company.bind(
            "<<ListboxSelect>>",
            self.checkCompanyDelete)
        self.list_airlines = []
        for company in airport.airlines:
            text = (str(company).ljust(10, ' ') +
                    str(airport.airlines[company]))
            self.list_box_company.insert(END, text)
            self.list_airlines.append(company)
        scrollbar.config(command=self.list_box_company.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        list_box_area.pack()
        self.list_box_company.pack()
        self.delCompanyButton = Button(
            column,
            text='Delete',
            relief=GROOVE,
            width=12,
            bg='#C0C0C0',
            state=DISABLED,
            command=self.deleteCompanyButton)
        self.delCompanyButton.pack(side=BOTTOM)
        Button(
            column,
            text='Add',
            relief=GROOVE,
            width=12,
            bg='#C0C0C0',
            command=self.addCompany).pack(
            side=BOTTOM)

    def addCompany(self):
        '''
        Permet d'ajouter une compagnie. Ouvre une nouvelle fenêtre demandant
        le nom et l'id de la nouvelle compagnie
        '''
        self.add_airlines = Tk()
        self.add_airlines.title("Add Airlines")
        self.add_airlines.config(bg='white')
        self.add_airlines.resizable(width=FALSE, height=FALSE)

        label_frame = Frame(
            self.add_airlines,
            bd=3,
            bg='white')  # frame du label
        label_frame.grid(row=0, column=1)
        Label(
            label_frame,
            bd=6,
            bg='white',
            text='Add Airlines',
            font=tkFont.Font(
                size=10)).grid(
            row=0,
            column=1)

        entry_frame = Frame(
            self.add_airlines,
            bd=5,
            bg='white')  # frame des entry
        entry_frame.grid(row=1, column=1)
        Label(
            entry_frame,
            bd=4,
            bg='white',
            text='Full Name').grid(
            row=0,
            column=0)
        company = Entry(
            entry_frame,
            bd=2,
            bg='white',
            textvariable=str,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        company.grid(row=0, column=1)

        Label(entry_frame, bd=4, bg='white', text='ID').grid(row=1, column=0)
        company_ID = Entry(
            entry_frame,
            bd=2,
            bg='white',
            textvariable=str,
            justify=CENTER,
            relief=SUNKEN,
            width=12)
        company_ID.grid(row=1, column=1)

        Button(
            self.add_airlines,
            text='Add',
            relief=GROOVE,
            width=10,
            bg='#C0C0C0',
            command=lambda: self.addInAirlines(
                (company.get()).lower(),
                (company_ID.get()).upper())).grid(
            row=3,
            column=1)

    def addInAirlines(self, company, company_ID):
        '''
        Ajoute la compagnie au dictionnaire des compagnies
        '''
        if company_ID not in airport.airlines:
            airport.airlines[company_ID] = company
            text = "La compagnie {} a été ajoutée".format(company)
            message = tkm.showinfo('Company added', text)
            self.add_airlines.destroy()
            text = (str(company_ID).ljust(10, ' ') + str(company))
            self.list_box_company.insert(END, text)
        else:
            text = "La compagnie {} existe déjà".format(company)
            message = tkm.showwarning('Company already exist', text)

    def deleteCompanyButton(self):
        '''
        Permet de supprimer une compagnie
        '''
        item = self.list_box_company.curselection()
        self.list_box_company.delete(item)
        numCompany = item[0]
        company = self.list_airlines[numCompany]
        nameCompany = airport.airlines[company]
        text = "La compagnie '{}' a été supprimé".format(nameCompany)
        message = tkm.showwarning("Company deleted", text)
        airport.del_company(company)

    def checkCompanyDelete(self, event=None):
        '''
        Vérifie si un avion est sélectionné dans la liste des avions
        au départ et rend le boutton 'del' actif si oui
        '''
        if self.list_box_company.curselection():
            self.delCompanyButton.configure(state=NORMAL)
        else:
            self.delCompanyButton.configure(state=DISABLED)

    ### Fonctions d'affichage des informations d'un avion ###
    def infoArrivalPlane(self, event=None):
        item = self.list_box_arrivals.curselection()
        num = item[0]
        plane = airport.arrival_list[num]
        self.infoPlane(airport.arrival_list, plane)

    def infoDeparturePlane(self, event=None):
        item = self.list_box_departures.curselection()
        num = item[0]
        plane = airport.departure_list[num]
        self.infoPlane(airport.departure_list, plane)

    def infoHistoryPlane(self, event=None):
        item = self.list_box_history.curselection()
        num = item[0]
        plane = airport.history_list[num]
        self.infoPlane(airport.history_list, plane)

    def infoPlaneCompany(self, event=None):
        item = self.list_box_company_plane.curselection()
        num = item[0]
        plane = self.list_of_plane[num]
        self.infoPlane(self.list_of_plane, plane)

    def infoPlane(self, plane_list, plane):

        self.info_plane_window = Tk()
        self.info_plane_window.title("Plane Info")
        self.info_plane_window.configure(background='white')
        self.info_plane_window.resizable(width=FALSE, height=FALSE)

        principal = Frame(
            self.info_plane_window,
            bd=3,
            bg='white')  # création de la frame principale
        principal.grid(row=0, column=0)

        frame_ID = Frame(
            principal,
            bd=5,
            bg='white')  # frame secondaire, contient l'id
        frame_ID.grid(row=0, column=0)
        label_ID = Label(
            frame_ID,
            bd=3,
            bg='white',
            text='ID',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        info_ID = Label(
            frame_ID,
            bd=3,
            bg='white',
            text=plane.getID()).grid(
            row=1,
            column=0)

        frame_company = Frame(
            principal,
            bd=5,
            bg='white')  # frame secondaire, contient la compagnie
        frame_company.grid(row=0, column=1)
        label_company = Label(
            frame_company,
            bd=3,
            bg='white',
            text='Company',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        info_compnay = Label(
            frame_company,
            bd=3,
            bg='white',
            text=plane.getCompany()).grid(
            row=1,
            column=0)

        frame_passengers = Frame(
            principal,
            bd=5,
            bg='white')  # frame secondaire, contient le nombre de passagers
        frame_passengers.grid(row=0, column=2)
        label_passengers = Label(
            frame_passengers,
            bd=3,
            bg='white',
            text='Passengers',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        info_passengers = Label(
            frame_passengers,
            bd=3,
            bg='white',
            text=plane.getPassengers()).grid(
            row=1,
            column=0)

        frame_fuel = Frame(
            principal,
            bd=5,
            bg='white')  # frame secondaire, contient le fuel
        frame_fuel.grid(row=0, column=3)
        label_fuel = Label(
            frame_fuel,
            bd=3,
            bg='white',
            text='Fuel',
            font=tkFont.Font(
                size=9)).grid(
            row=0,
            column=0)
        info_fuel = Label(
            frame_fuel,
            bd=3,
            bg='white',
            text=plane.getFuel()).grid(
            row=1,
            column=0)

        frame_consumption = Frame(
            principal,
            bd=5,
            bg='white')  # frame secondaire, contient la consommation
        frame_consumption.grid(row=0, column=4)
        label_consumption = Label(
            frame_consumption,
            bd=3,
            bg='white',
            text='Consumption',
            font=tkFont.Font(
                size=10)).grid(
            row=0,
            column=0)
        info_consumption = Label(
            frame_consumption,
            bd=3,
            bg='white',
            text=plane.getConsumption()).grid(
            row=1,
            column=0)

        if plane_list == airport.departure_list:
            frame_time = Frame(
                principal,
                bd=5,
                bg='white')  # frame secondaire, contient l'heure
            frame_time.grid(row=0, column=5)
            label_time = Label(
                frame_time,
                bd=3,
                bg='white',
                text='time',
                font=tkFont.Font(
                    size=9)).grid(
                row=0,
                column=0)
            time = plane.getTime()
            text = (str(time[0]) + 'h' + str(time[1]))
            info_time = Label(
                frame_time,
                bd=3,
                bg='white',
                text=text).grid(
                row=1,
                column=0)

        if plane_list == airport.history_list or plane_list == airport.departure_list:
            frame_statut = Frame(
                principal,
                bd=5,
                bg='white')  # frame secondaire, contient le statut
            frame_statut.grid(row=0, column=6)
            label_statut = Label(
                frame_statut,
                bd=3,
                bg='white',
                text='statut',
                font=tkFont.Font(
                    size=9)).grid(
                row=0,
                column=0)
            info_statut = Label(
                frame_statut,
                bd=3,
                bg='white',
                text=plane.getStatut()).grid(
                row=1,
                column=0)

        frame_button = Frame(principal, bd=5, bg='white')
        frame_button.grid(row=1, column=3)
        button_OK = Button(
            frame_button,
            text='OK',
            relief=GROOVE,
            width=6,
            bg='#C0C0C0',
            command=lambda: self.planeButtonOK()).grid(
            row=0,
            column=0)

    def planeButtonOK(self):
        self.info_plane_window.destroy()

    ### Fonctions d'affichage des avions d'une compagnie ###
    def showInfoCompany(self, event=None):
        item = self.list_box_company.curselection()
        numCompany = item[0]
        company_ID = self.list_airlines[numCompany]

        self.infoCompanyPlane(company_ID)

    def infoCompanyPlane(self, company_ID):
        self.info_company_window = Tk()
        self.info_company_window.title("Company Info")
        self.info_company_window.configure(background='white')
        self.info_company_window.resizable(width=FALSE, height=FALSE)

        text_label = "planes of {} :".format(airport.airlines[company_ID])
        principal = LabelFrame(
            self.info_company_window,
            bd=5,
            bg='white',
            relief=RIDGE,
            text=text_label,
            font=tkFont.Font(
                size=10))
        principal.pack()

        list_box_area = Frame(
            principal,
            bd=8,
            bg='white')  # création de list_box et de la scrollbar associée
        scrollbar = Scrollbar(
            list_box_area,
            bg='#C0C0C0',
            activebackground='grey',
            troughcolor='#F5F5F5',
            orient=VERTICAL)
        self.list_box_company_plane = Listbox(
            list_box_area,
            height=10,
            width=25,
            bd=2,
            yscrollcommand=scrollbar.set)
        self.list_box_company_plane.bind(
            "<Double-Button-1>",
            self.infoPlaneCompany)
        plane_lists = [
            airport.departure_list,
            airport.arrival_list,
            airport.history_list]
        self.list_of_plane = []
        for lists in plane_lists:
            for plane in lists:
                if plane.getCompany() == (airport.airlines[company_ID]):
                    self.list_box_company_plane.insert(END, plane.getID())
                    self.list_of_plane.append(plane)

        scrollbar.config(command=self.list_box_departures.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        list_box_area.pack()
        self.list_box_company_plane.pack()
        button_OK = Button(
            principal,
            text='OK',
            relief=GROOVE,
            width=6,
            bg='#C0C0C0',
            command=lambda: self.companyButtonOK()).pack(
            side=BOTTOM)

    def companyButtonOK(self):
        self.info_company_window.destroy()

    ### Fonctions relatives au temps ###
    def time(self, tick):
        return (str(tick //
                    60).rjust(2, '0') +
                "h" +
                str(tick %
                    60).rjust(2, '0'))

    def execute_plane(self, plane):
        if plane is not None:
            list_plane = self.list_box_departures.get(0, END)
            if plane.getID() in list_plane:
                item = list_plane.index(plane.getID())
                self.list_box_departures.delete(item)
            else:
                list_plane = self.list_box_arrivals.get(0, END)
                item = list_plane.index(plane.getID())
                self.list_box_arrivals.delete(item)

            
    def stepButton(self, nbr_min):
        self.nbr_min.delete(0, last=END)

        ok = False
        if len(nbr_min) != 0 and nbr_min.isdigit():
            nbr_min = int(nbr_min)
            ok = True
        elif nbr_min == '':
            nbr_min = 1
            ok = True
       
        if airport.departure_runway == 0 and airport.arrival_runway == 0 and airport.mixte_runway == 0:
            text = "\nVotre aéroport n'a aucune piste pour faire décoller ou atterrire des avions."\
                   "\nVeuillez en ajouter."
            message = tkm.showwarning('No runway', text)
        elif airport.departure_runway == 0 and airport.mixte_runway == 0:
            text = "\nVotre aéroport n'a aucune piste pour faire décoller des avions."\
                   "\nVeuillez en ajouter."
            message = tkm.showwarning('No runway', text)
        elif airport.arrival_runway == 0 and airport.mixte_runway == 0:
            text = "\nVotre aéroport n'a aucune piste pour faire atterrire des avions."\
                   "\nVeuillez en ajouter."
            message = tkm.showwarning('No runway', text)
        
        if ok:
            plane = None
            for i in range(int(nbr_min)):
                for j in range(airport.departure_runway):
                    plane = airport.next_departure()
                    self.execute_plane(plane)
                for k in range(airport.arrival_runway):
                    plane = airport.next_arrival()
                    self.execute_plane(plane)
                for l in range(airport.mixte_runway):
                    plane = airport.next_event()
                    self.execute_plane(plane)
                
                crashedPlane, delayedPlane = airport.update_status()
                for plane in crashedPlane:
                    text = "L'avion {} n'a malheureusement pas pu atterrire à temps."\
                        " \nVous avez tué {} passagers. /o\\".format(
                        plane.getID(),
                        plane.getPassengers())
                    message = tkm.showinfo('Plane Crashed', text)
                    list_plane = self.list_box_arrivals.get(0, END)
                    item = list_plane.index(plane.getID())
                    self.list_box_arrivals.delete(item)

                for plane in delayedPlane:
                    text = "L'avion {} est en retard.".format(plane.getID())
                    message = tkm.showinfo('Plane Delayed', text)
                
                if airport.tick == 1440:
                    airport.new_day()
                    text = '{:^20}'.format('New Day')
                    message = tkm.showinfo('New Day', text)
                self.clock.configure(text=self.time(airport.tick))

        else:
            text = "La valeur entrée n'est pas correcte. Veuillez la vérifier."
            message = tkm.showwarning("Valeur Incorecte", text)

    ### Fonctions relatives aux pistes ###
    def mod_depRunway_button(self, event=None):
        self.modifiy_nbrRunway('departures')
        
    def mod_arrRunway_button(self, event=None):
        self.modifiy_nbrRunway('arrivals')

    def mod_mixRunway_button(self, event=None):
        self.modifiy_nbrRunway('mixtes')

    def modifiy_nbrRunway(self, name_runway):
        self.modify_nbrRunway_window = Tk()
        self.modify_nbrRunway_window.title("Modify runway")
        self.modify_nbrRunway_window.configure(background='white')
        self.modify_nbrRunway_window.resizable(width=FALSE, height=FALSE)

        principal = Frame(
            self.modify_nbrRunway_window,
            bd=4,
            bg='white')
        principal.pack()
        text_label = "Modify {} runways".format(name_runway)
        label_principal = Label(
            principal,
            bd=3,
            bg='white',
            text=text_label,
            font=tkFont.Font(
            size=5))
        label_principal.pack()

        button_frame = Frame(
            principal,
            bd=3,
            bg='white')
        button_frame.pack(side=BOTTOM)

        button_plus = Button(
            button_frame,
            text='+1',
            relief=GROOVE,
            width=2,
            bg='#C0C0C0',
            command=lambda:self.incr_nbr_runway(name_runway))
        button_plus.pack(side=LEFT)

        button_moins = Button(
            button_frame,
            text='-1',
            relief=GROOVE,
            width=2,
            bg='#C0C0C0',
            command=lambda:self.decr_nbr_runway(name_runway))
        button_moins.pack(side=RIGHT)


    def incr_nbr_runway(self, name_runway):
        if name_runway == 'departures':
            airport.departure_runway += 1
            text_departure_label = "Departure runways: {}".format(
                airport.departure_runway)
            self.departure_label.configure(text=text_departure_label)

        elif name_runway == 'arrivals':
            airport.arrival_runway += 1
            text_arrival_label = "Arrival runways: {}".format(
                airport.arrival_runway)
            self.arrival_label.configure(text=text_arrival_label)
        
        elif name_runway == 'mixtes':
            airport.mixte_runway += 1
            text_mixte_label = "Mixte runways: {}".format(
                airport.mixte_runway)
            self.mixte_label.configure(text=text_mixte_label)

        self.modify_nbrRunway_window.destroy()



    def decr_nbr_runway(self, name_runway):
        if name_runway == 'departures':
            airport.departure_runway -= 1
            if airport.departure_runway < 0:
                airport.departure_runway = 0
            text_departure_label = "Departure runways: {}".format(
                airport.departure_runway)
            self.departure_label.configure(text=text_departure_label)

        elif name_runway == 'arrivals':
            airport.arrival_runway -= 1
            if airport.arrival_runway < 0:
                airport.arrival_runway = 0
            text_arrival_label = "Arrival runways: {}".format(
                airport.arrival_runway)
            self.arrival_label.configure(text=text_arrival_label)
        
        elif name_runway == 'mixtes':
            airport.mixte_runway -= 1
            if airport.mixte_runway < 0:
                airport.mixte_runway = 0
            text_mixte_label = "Mixte runways: {}".format(
                airport.mixte_runway)
            self.mixte_label.configure(text=text_mixte_label)

        self.modify_nbrRunway_window.destroy()



if __name__ == "__main__":
    root = Tk()
    AirportGUI(root)
    root.title("Airport Simulator")
    root.configure(background='white')
    root.resizable(width=FALSE, height=FALSE)
    root.mainloop()
