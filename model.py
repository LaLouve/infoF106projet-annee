'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: model.py
'''

class Model:

    def __init__(self,
                 name,
                 fuel,
                 conso,
                 passenger):

        self.name = name
        self.fuel = int(fuel)
        self.conso = int(conso)
        self.passenger = int(passenger)

    def getName(self):
        return self.name

    def getFuel(self):
        return self.fuel

    def getConso(self):
        return self.conso

    def getPassenger(self):
        return self.passenger

    def __str__(self):
        res = ((str(self.name).ljust(10, ' ')) + '| ' +
               (str(self.fuel).ljust(8, ' ')) + '| ' +
               (str(self.conso).ljust(7, ' ')) + '| ' +
               (str(self.passenger).ljust(10, ' '))
               )
        return res

    @staticmethod
    def fromjson(json):
        name = json['name']
        fuel = json['fuel']
        conso = json['conso']
        passenger = json['passenger']

        return Model(name, fuel, conso, passenger)
