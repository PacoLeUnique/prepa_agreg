from xml.dom.minidom import parse
from sys import argv


if len (argv) != 2:
    print ("usage: %s <file.xml>" % argv[0])
    exit (1)

try:
    print("Before loading", argv[1])
    doc = parse(argv[1])
    print("After loading")
    input("Press any key to continue...")
except:
    print ("Error while opening", argv[1])
    exit (2)

