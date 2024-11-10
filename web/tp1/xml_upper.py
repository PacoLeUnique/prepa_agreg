from xml.dom import minidom, getDOMImplementation
from dump_xml import load_xml, Document

import sys


def xml_upper(doc : Document) -> Document:
    impl = getDOMImplementation("test")

    impl.createDocument()




if __name__ == '__main__':

    # On recup le fichier 
    if len(sys.argv) < 2:
        print("Faut un argument stp")
        exit()

    path = 'xml/' + sys.argv[1]
    doc = load_xml(path)

