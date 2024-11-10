from xml.dom.minidom import parse
from xml.dom import getDOMImplementation, Node
from sys import argv

def toUpper(node, doc):
    res = None
    if node.nodeType == Node.DOCUMENT_NODE:
        res = doc
    elif node.nodeType == Node.TEXT_NODE:
        res = doc.createTextNode(node.nodeValue.upper())
    elif node.nodeType == Node.ELEMENT_NODE:
        res = doc.createElement(node.nodeName.upper())

    if res is not None:
        for child in node.childNodes:
            rchild = toUpper(child, doc)
            if rchild is not None:
                res.appendChild(rchild)
    return res




doc = parse(argv[1])
impl = getDOMImplementation()
ndoc = impl.createDocument(None, None, None)
toUpper(doc, ndoc)
print(ndoc.toprettyxml())
