from typing import ClassVar
from xml.dom.minidom import parse
from xml.dom import Node
from sys import argv


#Question 2

def toJSON(node):
    if node.nodeType == Node.DOCUMENT_NODE:
        #Le nœud est le nœud fictif situé au dessus de la balise racine:
        return toJSON(node.documentElement)
    elif node.nodeType == Node.TEXT_NODE:
        return node.nodeValue
    elif node.nodeType == Node.ELEMENT_NODE:
        return { "name" : node.nodeName,
                 "attributes" : {
                     node.attributes.item(i).nodeName:
                     node.attributes.item(i).nodeValue for i in range(len(node.attributes))
                 },
                "children" : [ toJSON(child) for child in node.childNodes ]
        }

def toJSONnrec (node):
    #version non récursive qui utilise une pile :
    #chaque nœud est associé au dictionnaire de son parent sur la pile :
    # - on dépile le prochain nœud et le dico du parent.
    # - on transforme le nœud
    # - on l'ajoute en fin des enfants du dictionnaire du parent
    # - on pousse tous les enfants du nœud avec le nouveau dictionnaire sur la
    #   pile. Attention, les enfants doivent être poussés dans l'ordre inverse
    #   pour que le premier se retrouve au sommet de la pile.
    # on s'arrête lorsque la pile est vide.

    first = (node.documentElement, { "children" : [] })
    stack = [ first ]
    while stack:
        node, parent_dict = stack.pop()
        val = None
        if node.nodeType == Node.TEXT_NODE:
            val = node.nodeValue
        elif node.nodeType == Node.ELEMENT_NODE:
            val = { "name" : node.nodeName,
                    "attributes" : {
                     node.attributes.item(i).nodeName :
                     node.attributes.item(i).nodeValue for i in range(len(node.attributes))
                 },
                "children" : []
            }
        parent_dict["children"].append(val)
        for i in range(len(node.childNodes) -1, -1, -1):
            child = node.childNodes[i]
            stack.append((child, val))

    return first[1]["children"][0]

def dump(json):
    print(json)

if len (argv) != 2:
    print ("usage: %s <file.xml>" % argv[0])
    exit (1)

try:
    #Question 1
    doc = parse(argv[1])
    json = toJSON(doc)
    json2 = toJSONnrec(doc)
    assert(json == toJSONnrec(doc))
    dump(json)
    print("--")
    dump(json2)


except Exception as e:
    print(e)
    print ("Error while opening", argv[1])
    exit (2)

