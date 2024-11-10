from xml.dom import minidom
import sys

Document = minidom.Document

# ================= EXERCICE 2 =====================

# 1.
def load_xml(path : str) -> Document:
    doc : Document = minidom.parse(path)
    return doc


# 2.
def toJSON(doc : Document) -> dict:
    """Transforme l'arbre DOM en dictionnaire Python, au format JSON."""

    # 0. Les Cas de base 
    if doc.nodeName == "#text":
        return doc.nodeValue
    if doc.nodeName == "#document":
        return toJSON(doc.childNodes[0])

    json = {}

    #1 - le nom
    json["name"] = doc.nodeName

    # 2 - les attributs
    if (doc.hasAttributes()):
        json["atrributes"] = {}
        attributs = doc.attributes

        for i in range(attributs.length):
            attr = attributs.item(i)
            json["atrributes"][attr.name] = attr.value

    # 3 - les enfants (récursif)
    if doc.hasChildNodes:
        json["children"] = []

        for child in doc.childNodes:
            json["children"].append(toJSON(child))

    return json

if __name__ == '__main__':

    # On recup le fichier 
    if len(sys.argv) < 2:
        print("Faut un argument stp")
        exit()

    # On charge le DOM
    file = "xmls/" + sys.argv[1]
    doc : Document = load_xml(file)

    # youhou on a un document
    # print(doc.nodeName)
    # for child in doc.childNodes:
    #     print(child.nodeName)

    json = toJSON(doc)
    print(json)