class InvalidResult(Exception): pass

def getDomFromNode(node):
    while True:
        parent = node.parentNode
        if parent == None:
           return node
        node = parent

def replaceChildren(node, children):
    if not isinstance(children, list):
        children = (children,)

    for child in node.childNodes:
        node.removeChild(child)

    for child in children:
        node.appendChild(child)

def getChildrenByTagName(node, tag_name):
    return [x for x in node.childNodes if (x.nodeType == x.ELEMENT_NODE) and
            (x.nodeName == tag_name)]

def getUniqueChildbyTagName(node, *args):
    r = None
    for tag in args:
        r = getChildrenByTagName(node, tag)
        if len(r) > 1:
            raise InvalidResult("More than one child found with tag '%s'" % tag)
        node = r[0]
    if not r:
        raise InvalidResult("No matching tag '%s'" % tag)
    return r[0]
