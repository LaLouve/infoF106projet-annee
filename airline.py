'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: airlines.py
'''

class Airline:

    def __init__(self, ID, name):
        self.ID = str(ID).upper()
        self.name = str(name).lower()

    def getID(self):
        return self.ID

    def getName(self):
        return self.name

    def __str__(self):
        res = ((str(self.ID).ljust(4, ' ')) + '| ' +
               (str(self.name).ljust(20, ' '))
               )
        return res

    @staticmethod
    def fromjson(json):
        ID = json['ID']
        name = json['name']

        return Airline(ID, name)
