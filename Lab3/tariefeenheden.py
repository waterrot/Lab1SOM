from typing import List
import csv

class Tariefeenheden:

    @staticmethod
    def get_stations():
        # Open het CSV-bestand en lees de gegevens
        with open('Lab3\Tariefeenheden.csv', newline='') as csvfile:
            csv_data = list(csv.reader(csvfile, delimiter=','))

        # De eerste rij bevat de stationsnamen (behalve het eerste element dat leeg is)
        stations = csv_data[0][1:]
        return stations

    @staticmethod
    def get_tariefeenheden(from_station, to_station):
        # Open het CSV-bestand en lees de gegevens
        with open('Lab3\Tariefeenheden.csv', newline='') as csvfile:
            csv_data = list(csv.reader(csvfile, delimiter=','))

        # Zoek de index van de stations in de eerste rij van het CSV-bestand
        stations = csv_data[0][1:]
        from_index = stations.index(from_station)
        to_index = stations.index(to_station)

        # Hier kun je je logica toevoegen om tariefeenheden te berekenen op basis van de afstand tussen stations
        # In dit voorbeeld gebruik ik de gegeven tariefeenheden uit het CSV-bestand
        tariefeenheden = int(csv_data[from_index + 1][to_index + 1])
        return tariefeenheden