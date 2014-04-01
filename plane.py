'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: plane.py
'''


class Plane:

    def __init__(
            self,
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut):
        self.ID = ID
        self.company = company
        self.passengers = int(passengers)
        self.fuel = int(fuel)
        self.model = model
        # modèle de l'avion, définit le fuel, la consommation et le nbr max de
        # passagers
        self.consumption = int(consumption)
        self.time = time
        # statut= Landed, Crashed, Take Off, Delayed, Deleted, In Time or None
        self.statut = statut

    def getID(self):
        return self.ID

    def getCompany(self):
        return self.company

    def getPassengers(self):
        return self.passengers

    def getFuel(self):
        return self.fuel

    def getConsumption(self):
        return self.consumption

    def getModel(self):
        return self.model

    def getTime(self):
        return self.time

    def getStatut(self):
        return self.statut

    def setStatut(self, valStatut):
        self.statut = valStatut

    def companyID(self):
        return self.ID[:-4]

    def ratio(self):
        return int(self.getFuel() // self.getConsumption())

    def update(self):
        self.fuel -= self.consumption

    def isCrashed(self):
        # retourne True si l'avion s'est crashé
        return self.fuel <= 0

    def isDelayed(self, tick):  # L'avion est-il retardé?
        if (int((self.time[0] * 60) + (self.time[1]))) < tick:
            return True
        else:
            return False

    def __str__(self):
        res = ((str(self.ID).ljust(9, ' ')) +
               (str(self.company).ljust(20, ' ')) +
               (str(self.passengers).ljust(5, ' ')) +
               (str(self.fuel).ljust(6, ' ')) +
               (str(self.consumption).ljust(5, ' ')) +
               (str(self.model).ljust(8, ' '))
               )
        return res

    @staticmethod
    def fromjson(json):
        ID = json["ID"]
        company = json["company"]
        passengers = json["passengers"]
        fuel = json["fuel"]
        consumption = json["consumption"]
        model = json["model"]
        time = json["time"]
        statut = json["statut"]

        return Plane(ID, company, passengers, fuel, consumption, model, time, statut)