'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: airport.py
'''

import airportFunctions
import airportTerminal


def mainLoop():
    '''
    Boucle principale pour le fonctionnement du programme en terminal

    Vérifie si une sauvegarde est présente
    Appelle le menu des actions 
    Vérifie si l'aéroport posséde des pistes
    Effectue l'évenement suivant (attérissage/décollage) en fonction 
    du nombre de pistes présentes
    Met à jour les informations des avions
    '''
    airport = airportTerminal.airport
    terminal = airportTerminal.Terminal()
    terminal.askNewGame("save.txt")

    while True:
        nbrTick = terminal.userMenu()
        if airport.departureRunway == 0 and\
           airport.arrivalRunway == 0 and\
           airport.mixteRunway == 0:
            print(
                "\nVotre aéroport n'a aucune piste,"
                " vous ne pouvez faire décoller ou atterrir des avions."
                "\nVeuillez en ajouter.")
        elif airport.departureRunway == 0 and\
                airport.mixteRunway == 0:
            print(
                "\nVotre aéroport n'a aucune piste"
                " pour faire décoller des avions."
                "\nVeuillez en ajouter.")
        elif airport.arrivalRunway == 0 and\
                airport.mixteRunway == 0:
            print(
                "\nVotre aéroport n'a aucune piste"
                " pour faire atterrir des avions."
                "\nVeuillez en ajouter.")
        else:
            for i in range(nbrTick):
                airport.eventRandom()
                for j in range(airport.departureRunway):
                    airport.nextDeparture()
                for k in range(airport.arrivalRunway):
                    airport.nextArrival()
                for l in range(airport.mixteRunway):
                    airport.nextEvent()
                airport.updateStatus()
                if airport.tick == 1440:
                    airport.newDay()


if __name__ == "__main__":
    mainLoop()
