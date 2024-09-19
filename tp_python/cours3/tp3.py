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
    humidite = int(r.humidite)

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

#8.
#  Fetch infos sur les stations
Station = namedtuple("Station", ["nom", "latitude", "longitude", "altitude"])

stations : dict[str, Station] = {}
with open("postesSynop.csv", "r") as f:
    dr = csv.DictReader(f, delimiter=";")
    for line in dr:
        stations[line["ID"]] = Station(line["Nom"], line["Latitude"], line["Longitude"], line["Altitude"])


for s in stations:  print(stations[s])


#9.
def humidite_moyenne(records : list[Record]) -> float:
    """Renvoie le taux d'humidité moyenne sur l'ensemble des relevés."""
    
    humi : int = 0
    for r in records:
        humi += r.humidite
    return humi / len(records)

#10.
def precipitation_moyenne_mais_seulement_venant_des_stations_dont_luid_est_compris_entre_60000_et_69999(records : list[Record]) -> float:
    """Franchement, lis juste le nom de la fonction."""

    precipit : float = 0.
    nb_stations : int = 0
    for r in records:
        if int(r.uid) >= 60000 and int(r.uid) < 70000:
            nb_stations += 1
            precipit += r.precipitations
    return precipit / nb_stations


#11. (+13.)
def get_records(records: list[Record], uid : str, is_records_sorted=False) -> Record:
    """Renvoie tous les records d'une station donnée."""

    records_station : list[Record] = []

    #Les records sont pas triés (complexité : O(n))
    if not is_records_sorted:
        for r in records:
            if r.uid == uid:
                records_station.append(r)

    #Les records sont triés (complexité : O(log(n) + |records d'id uid|))
    else:
        pass #TODO

    return records_station

#12.
def sort_records(records : list[Record]):
    """Trie les records, par ordre d'uid croissant."""
    records.sort(key= lambda r:int(r.uid))


# ===================== FUSION DE TABLES =====================





def test():
    print("")
    print(f"Temp min relevée : {temperature_min(records)}°C")

    uid : str = id_station_max_vent(records)
    print(f"uid de la station du vent max : {uid}")
    print(f"Le nom de cette station : {stations[uid].nom}")

    print(f"Humidité moyenne : {round(humidite_moyenne(records), 2)}%")
    print(f"précipitations moyennes des stations entre 60000 et 69999 : {precipitation_moyenne_mais_seulement_venant_des_stations_dont_luid_est_compris_entre_60000_et_69999(records)}")

    print("\n=============================")

    id = "07005"
    recs = get_records(records, id)
    print(f"Il y a {len(recs)} records enregistrés par la station {id}. Pas mal !")
    print(f"les 10 1ers relevés de la station 07005 : ")
    for i in range(10):
        print(recs[i])

    print("\n allez hop on sort les records")
    sort_records(records)
    print("flemme de l'afficher pck c'est trop de lignes, mais t'as l'idée")
    #print("les voicis triés :")
    #for i in range(1000):
    #    print(records[-i])






test()