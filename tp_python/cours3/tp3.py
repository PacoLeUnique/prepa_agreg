import csv
from collections import namedtuple
from datetime import datetime


# ================== NETTOYAGE DES DONNEES ==================

Record = namedtuple("Record", ["uid", "vitesse_vent", "temperature", "humidite", "precipitations", "date"])

# 1+2 : fetch la data
records : list[Record] = []

with open("synop.201902.csv", "r") as f:
    dr : csv.DictReader = csv.DictReader(f, delimiter=";") 
    for line in dr:
        records.append(Record(line["numer_sta"], line["ff"], line["t"], line["u"], line["rr1"], line["date"]))

print("records au début :", len(records))

# 3. On vire les champs incomplets (ceux ou il y a des mq)
records = [r for r in records if all([v != 'mq' for v in r])]

print("Après avoir enlevé les champs avec des trous :", len(records))

print("avant :")
for i in range(10):
    print(records[i])

# 4. On convertit les champs dans le bon type
for i in range(len(records)):
    r = records[i]

    #str -> degré Kelvin -> degré Celcius
    temperature = float(r.temperature) - 273

    #str -> m/s -> km/h
    vitesse_vent = float(r.vitesse_vent) * 3.6

    #str -> pourcentage
    humidite = float(r.humidite) / 100

    #str -> float
    precipitations = float(r.precipitations)

    #str -> date
    date = datetime.strptime(r.date, "%Y%m%d%H%M%S")

    records[i] = Record(r.uid, vitesse_vent, temperature, humidite, precipitations, date)


# Affichage des 10 premières lignes
print("après :")
for i in range(10):
    print(records[i])



# ================= STATISTIQUES ================= 

#6.
def temperature_min(records : list[Record]) -> float:
    """Renvoie la température la plus basse relevée."""    
    return min(r.temperature for r in records)

#7.
def id_station_max_vent(records : list[Record]) -> str:
    """Renvoie l'id de la station météo ayant relevé la vitesse maximale de vent."""
    r : Record = max((r for r in records), key= lambda r:r.vitesse_vent)
    return r.uid

#8. Fetch infos sur les stations
Station = namedtuple("Station", ["nom", "latitude", "longitude", "altitude"])

stations : dict[str, Station] = {}
with open("postesSynop.csv", "r") as f:
    dr = csv.DictReader(f, delimiter=";")
    for line in dr:
        stations[line["ID"]] = Station(line["Nom"], line["Latitude"], line["Longitude"], line["Altitude"])

print("stations :")
print(stations)


def test():
    print("")
    print(f"Temp min relevée : {temperature_min(records)}°C")
    print(f"uid de la station du vent max : {id_station_max_vent(records)}")

test()