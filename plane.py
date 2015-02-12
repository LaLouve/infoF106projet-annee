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
        # modèle de l'avion, définit le fuel, la consommation et le nbr max de
        # passagers
        self.model = model
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
        if (int((self.time[0] * 60) + (self.time[1]))) <= tick:
            return True
        else:
            return False

    def __str__(self):

        # Vérifie la longeur de self.company et self.model
        if len(self.company) > 20:
            self.company = str(self.company[:19]) + '.'
        if len(self.model) > 5:
            self.model = str(self.model[:4] + '.')

        res = ((str(self.ID).ljust(8, ' ')) + '| ' +
               (str(self.company).ljust(20, ' ')) + '| ' +
               (str(self.passengers).ljust(5, ' ')) + '| ' +
               (str(self.fuel).ljust(5, ' ')) + '| ' +
               (str(self.consumption).ljust(4, ' ')) + '| ' +
               (str(self.model).ljust(5, ' '))
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

        return Plane(
            ID,
            company,
            passengers,
            fuel,
            consumption,
            model,
            time,
            statut)
