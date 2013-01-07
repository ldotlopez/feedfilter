import domutils
import sys

class MeneameRewriteLink():
    def is_valid_item(self, node):
        return node.getElementsByTagName('meneame:url') and node.getElementsByTagName('description')

    def process_item(self, node):
        if not self.is_valid_item(node):
            return

        dom = domutils.getDomFromNode(node)

        # Get nodes for the 'meneame' link and 'dest' link.
        # Note than tag names and variable names are swapped, this is correct.
        # They aren't textNodes yet
        dest_link_node    = node.getElementsByTagName('link')[0]
        meneame_link_node = node.getElementsByTagName('meneame:url')[0]
        guid_node         = node.getElementsByTagName('guid')[0]

        # Get URLs as text. Contrary to their names and variables this code is correct, I'm storing them
        # swapped.
        meneame_url = dest_link_node.childNodes[0].data
        dest_url = meneame_link_node.childNodes[0].data

        # Now, we have to swap them on the dom
        domutils.replaceChildren(dest_link_node, dom.createTextNode(dest_url))
        domutils.replaceChildren(guid_node, dom.createTextNode(dest_url))

        # Rewrite description
        description = node.getElementsByTagName('description')[0].childNodes[0].data
        description = description.replace('noticia original', 'enlace meneame')
        description = description.replace(dest_url, meneame_url)
        domutils.replaceChildren(node.getElementsByTagName('description')[0],
                                 dom.createCDATASection(description))

    def process(self, dom):
        for child in domutils.getUniqueChildbyTagName(dom, 'rss', 'channel').childNodes:
            if not child.nodeType == child.ELEMENT_NODE:
                continue

            if child.nodeName == 'title':
                domutils.replaceChildren(child, dom.createTextNode('Meneame (Directo)'))

            if child.nodeName == 'link':
                domutils.replaceChildren(child, dom.createTextNode('https://github.com/ldotlopez/feedfilter'))

            if child.nodeName == 'atom:link' and child.hasAttribute('rel') and child.getAttribute('rel') in ('self','hub'):
                child.parentNode.removeChild(child)

        for item in dom.getElementsByTagName('item'):
            self.process_item(item)

