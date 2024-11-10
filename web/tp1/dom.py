# ================== EXERCICE 1 ===================

import xml.dom.minidom as md
import sys

Document = md.Document

# On recup le fichier 
if len(sys.argv) < 2:
    print("Faut un argument stp")
    exit()
file = "xmls/xml" + sys.argv[1]

# Puis on charge le fichier
print("chargement.......")
doc : Document = md.parse(file)
print("fichier chargé :D")

print("écris un truc pour quitter")
input()


