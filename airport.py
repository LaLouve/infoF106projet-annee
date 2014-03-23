'''
Dervaux Florence, N° de matricule : 000396246, groupe 1

Projet d'année: Simulation de la gestion du trafic aérien d’un aéroport
Partie 3

fichier: airport.py
'''

import airportFunctions


def main_loop():
    airport = airportFunctions.Airport()

    airport.add_runway()

    while True:
        nbrTick = airport.user_menu()
        if airport.departure_runway == 0 and\
           airport.arrival_runway == 0 and\
           airport.mixte_runway == 0:
            print(
                "\nVotre aéroport n'a aucune piste,"
                " vous ne pouvez faire décoller ou atterrire des avions."
                "\nVeuillez en ajouter.")
        elif airport.departure_runway == 0 and\
                airport.mixte_runway == 0:
            print(
                "\nVotre aéroport n'a aucune piste"
                " pour faire décoller des avions."
                "\nVeuillez en ajouter.")
        elif airport.arrival_runway == 0 and\
                airport.mixte_runway == 0:
            print(
                "\nVotre aéroport n'a aucune piste"
                " pour faire atterrire des avions."
                "\nVeuillez en ajouter.")
        else:
            for i in range(nbrTick):
                for j in range(airport.departure_runway):
                    airport.next_departure()
                for k in range(airport.arrival_runway):
                    airport.next_arrival()
                for l in range(airport.mixte_runway):
                    airport.next_event()
                airport.update_status()
                if airport.tick == 1440:
                    airport.new_day()


if __name__ == "__main__":
    main_loop()
