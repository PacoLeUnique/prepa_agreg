import csv
from collections import namedtuple
from datetime import datetime
from datetime import *
import matplotlib.pyplot as plt


# ================== NETTOYAGE DES DONNEES ==================

Record = namedtuple("Record", ["uid", "vitesse_vent", "temperature", "humidite", "precipitations", "date"])

# 1+2 : fetch la data
def extract_table(file : str) -> list[Record]:
    """Extrait les donnes du csv, et renvoie la liste de tous ses records."""
    
    records : list[Record] = []
    with open(file, "r") as f:
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

    return records


records : list[Record] = extract_table("synop.201902.csv")
records2009 : list[Record] = extract_table("synop.200902.csv")

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
        
        # 1. On cherche par dichotomie une station avec le bon uid
        g = 0
        d = len(records)-1
        m = 0

        while (int(records[m].uid) != int(uid)) and (g != d):
            print(f"passe à [{g}:{d}]")

            m = (g+d)//2
            if int(uid) < int(records[m].uid):
                d = m-1
            else:
                g = m
        
        if (g == d) and int(records[m].uid) != int(uid):
            raise ValueError(f"y'a pas de station d'id {int(uid)}")

        # 2. à partir de m, on s'étend à droite et a gauche
        records_station.append(records[m])
        
        # eeeeet a droite
        i = 1
        while int(records[m+i].uid) == int(uid):
            records_station.append(records[m+i])
            i += 1

        # eeeeeeeeet a gauche
        i = 1
        while int(records[m-i].uid) == int(uid):
            records_station.append(records[m-i])
            i += 1

    return records_station

#12.
def sort_records(records : list[Record]):
    """Trie les records, par ordre d'uid croissant."""
    records.sort(key= lambda r:int(r.uid))


# ===================== FUSION DE TABLES =====================

def meme_date(d1 : datetime, d2 : datetime):
    """Renvoie True si d1 et d2 sont les mêmes, à l'année près."""
    return (    d1.month == d2.month
            and d1.day == d2.day
            and d1.hour == d2.hour)


#14.
Temperature = namedtuple("Temperature", ["uid", "date", "tmp_2009", "tmp_2019"])
def merge_temperatures_de_fevrier(records2019 : list[Record], records2009 : list[Record]) -> list[Temperature]:
    """Fusionne 2 tables ayant les memes record, à des années différentes.
       Ne garde que la température du mois de février.
    """

    fev09 : list[Record] = [r for r in records2009 if r.date.month == 2]
    fev19 : list[Record] = [r for r in records2019 if r.date.month == 2]

    temperatures : list[Temperature] = []
    for r09 in fev09:
        for r19 in fev19:
            if meme_date(r19.date, r09.date):
                temperatures.append(Temperature(r09.uid, r09.date, r09.temperature, r19.temperature))
                break

    return temperatures

#15.
def qui_est_le_plus_chaud(temperatures : list[Temperature]) -> str:
    """Renvoie l'année ou il a fait le plus chaud.
    Donc soit 2009, soit 2019.
    """

    chaud2009 = 0
    chaud2019 = 0
    for t in temperatures:
        if t.tmp_2009 > t.tmp_2019 : chaud2009 += 1
        else:  chaud2019 += 1
    
    return "2009" if chaud2009>chaud2019 else "2019"



# ===================== GRAPHIQUES =====================

#16.
def show_temperatures(temperatures : list[Temperature]):
    """crée un graphique qui montre les différences de températures entre février 2009 et février 2019.
    """

    #On vérifie juste qu'on a bien seulement les températures de février
    assert all(t.date.month == 2 for t in temperatures)
    

    # On regroupe les températures par jour
    # --> tmp_jour[20] = tous les records du 19 février 
    tmp_jours : list[list[dict]] = [[{"2009" : t.tmp_2009, "2019" : t.tmp_2019, "date" : t.date} for t in temperatures if t.date.day == i] for i in range(1,29)]

    # On fait la moyenne de tout
    # --> moy_temp_2009[20] = la température moyenne du 19 février 2009
    moy_tmp_2009 = [ (  sum( r["2009"] for r in day_records)/len(day_records)  ) for day_records in tmp_jours]
    moy_tmp_2019 = [ (  sum( r["2019"] for r in day_records)/len(day_records)  ) for day_records in tmp_jours]
    days = list(range(1,29))

    print(moy_tmp_2009)
    print(moy_tmp_2019)

    plt.title("Evolution de la température entre 2009 et 2019")
    plt.xlabel("Jour")
    plt.ylabel("Température (en °C)")

    plt.plot(days, moy_tmp_2009, "x-", label="février 2009")
    plt.plot(days, moy_tmp_2019, "o-", label="février 2019")
    plt.legend()

    plt.show()
    




# ==============================================================
# ========================= LE TESTING =========================
# ==============================================================

def test():
    print("")
    print(f"Temp min relevée : {temperature_min(records)}°C")

    uid : str = id_station_max_vent(records)
    print(f"uid de la station du vent max : {uid}")
    print(f"Le nom de cette station : {stations[uid].nom}")

    print(f"Humidité moyenne : {round(humidite_moyenne(records), 2)}%")
    print(f"précipitations moyennes des stations entre 60000 et 69999 : {precipitation_moyenne_mais_seulement_venant_des_stations_dont_luid_est_compris_entre_60000_et_69999(records)}")

    print("\n=============================\n")

    id = "07005"
    recs = get_records(records, id)
    print(f"Il y a {len(recs)} records enregistrés par la station {id}. Pas mal !")
    print(f"les 10 1ers relevés de la station 07005 : ")
    for i in range(10):
        print(recs[i])

    print("allez hop on sort les records")
    sort_records(records)
    
    id2 = "07072"
    recs = get_records(records, id2, is_records_sorted=True)

    print(f"les record de la station {id} :")
    for i in range(10):
        print(recs[i])

    print("\n================FUSION DE TABLE================\n")

    temperatures = merge_temperatures_de_fevrier(records, records2009)
    print("quelques températures de février :")
    for i in range(5):
        print(temperatures[i])

    plus_chaud : str = qui_est_le_plus_chaud(temperatures)
    print(f"et le plus chaud c'est {plus_chaud}")


    print("\n===========================================\n")

    show_temperatures(temperatures)





test()