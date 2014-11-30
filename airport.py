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
        terminal.checkRunways()

        for i in range(nbrTick):
            plane = airport.eventRandom()
            terminal.showEvent(plane)

            for j in range(airport.departureRunway):
                plane = airport.nextDeparture()
                terminal.showEvent(plane)

            for k in range(airport.arrivalRunway):
                plane = airport.nextArrival()
                terminal.showEvent(plane)

            for l in range(airport.mixteRunway):
                plane = airport.nextEvent()
                terminal.showEvent(plane)

            crashedPlane, delayedPlane = airport.updateStatus()
            for info in crashedPlane:
                plane = info[0]
                death = info[1]
                terminal.showEvent(plane)
                terminal.showEvent(death)

            for plane in delayedPlane:
                terminal.showEvent(plane)

            if airport.tick == 1440:
                airport.newDay()


if __name__ == "__main__":
    mainLoop()
