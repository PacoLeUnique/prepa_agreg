from xml.sax.handler import ContentHandler
from xml.sax import parse
from sys import argv

class ToUpperHandler(ContentHandler):

    def __init__(self, *args, **kwargs):
        super(ToUpperHandler, self).__init__(*args, **kwargs)

    def startElement(self, name, attrs):
        #appelé sur une balise ouvrante:
        print("<", end="")
        print(name.upper(), end="")
        if attrs.getLength():
            print(" ", end="")
        print (" ".join([ n + "='" + attrs.getValue(n) + "'" for n in attrs.getNames()]),
               end="")
        print(">", end="")

    def endElement(self, name):
        #appelé sur une balise fermante
        print("</", end="")
        print(name.upper(), end="")
        print(">", end="")

    def ignorableWhitespace(self, whitespace):
        #appelé sur des suites de ' ', '\t', '\n'
        print(whitespace)

    def characters(self, content):
        #appelé sur du texte
        print(content.upper(), end="")

if len (argv) != 2:
    print ("usage: %s <file.xml>" % argv[0])
    exit (1)

try:
    doc = parse(argv[1], ToUpperHandler())
except Exception as e:
    print(e)
    exit(2)