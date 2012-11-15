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

