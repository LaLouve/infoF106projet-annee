'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 4

fichier: airport.py

FONCTIONNEMENT EN TERMINAL PLUS SUPPORTÉ
'''

import airportFunctions
import airportTerminal
import signal


def sigint_handler(signal, frame):
    '''
    Coupe le programme lors d'un ^C
    '''
    print('\nFin de la simulation.')
    exit(0)


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
    signal.signal(signal.SIGINT, sigint_handler)
    terminal = airportTerminal.Terminal()
    airport = airportFunctions.Airport()
    
    terminal.askNewGame("save.txt")

    nbrTick = 1

    while nbrTick > 0:
        nbrTick = terminal.userMenu()
        print("tick", nbrTick)
        ok = terminal.checkRunways()
        print(ok)

        if nbrTick is not None:
            for i in range(nbrTick):
                print("\nn", i)
                plane = airport.eventRandom()
                print('random', plane)
                terminal.showEvent(plane)
                print("piste", airport.departureRunway, airport.arrivalRunway, airport.mixteRunway)

                for j in range(airport.departureRunway):
                    plane = airport.nextDeparture()
                    print("departure", plane)
                    terminal.showEvent(plane)

                for k in range(airport.arrivalRunway):
                    plane = airport.nextArrival()
                    print("arrival", plane)
                    terminal.showEvent(plane)

                for l in range(airport.mixteRunway):
                    plane = airport.nextEvent()
                    print("mixte", plane)
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
                    terminal.newDay()


if __name__ == "__main__":
    mainLoop()
