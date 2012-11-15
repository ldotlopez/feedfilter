import domutils

class MeneameRewriteLink():
    def is_valid_item(self, node):
        return node.getElementsByTagName('meneame:url') and node.getElementsByTagName('description')

    def process_item(self, node):
        if not self.is_valid_item(node):
            return

        dom = domutils.getDomFromNode(node)

        # Swap destination link and meneame link in the 'link' tag
        orig_link = node.getElementsByTagName('meneame:url')[0].childNodes[0]
        link_node = node.getElementsByTagName('link')[0]
        
        new_link = dom.createTextNode(orig_link.data)
        domutils.replaceChildren(link_node, domutils.getDomFromNode(node).createTextNode(orig_link.data))

        # Swap destination link and meneame link in the 'description' tag
        new_descrition_s = node.getElementsByTagName('description')[0].childNodes[0].data
        new_descrition_s = new_descrition_s.replace('noticia original', 'enlace meneame')
        new_descrition_s = new_descrition_s.replace(orig_link.data, link_node.childNodes[0].data)

        new_descrition   = dom.createCDATASection(new_descrition_s)
        domutils.replaceChildren(node.getElementsByTagName('description')[0], new_descrition)

    def process(self, dom):
        for item in dom.getElementsByTagName('item'):
            self.process_item(item)

