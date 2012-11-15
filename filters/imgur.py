import bs4 as BeautifulSoup

class ImgURFilter(object):
    def _deimgur(self, url):
        comp = os.path.basename(url)
        (id_, ext) = os.path.splitext(comp)
        if ext:
            return (url, 'image')

        (html, cached) = Cache().fetch_url(url)
        soup = BeautifulSoup.BeautifulSoup(html)

	if soup.title.text == 'Too Many Requests':
            Cache().delete(url)
            return (url, 'rollback')

        ret = None
        src_type = None

        try:
            if url.find('/a/') >= 0:
                (ret, src_type) = (
                soup.find_all('div', id='image-container')[0].find_all('div','image')[0].find_all('img')[0].get('data-src'),
                'album')
            else:
                (ret, src_type) = (
                soup.find_all('div','panel')[0].find_all('div','image')[0].find_all('img')[0].get('src'),
                'image')
        except:
            pdb.set_trace()

        if not ret:
            raise Exception("Unable to find image in '%s'" % url)

        return (ret, src_type)

    def process(self, dom):
        items = dom.getElementsByTagName('item')
        for item in items:
            linkNode = item.getElementsByTagName('link')[0]
            link_url = linkNode.childNodes[0].data
            (hotlink, src_type) = self._deimgur(link_url)
            if src_type == 'rollback':
                print "Reddit rollback"
                continue

            descriptionNode = item.getElementsByTagName('description')[0]
            descriptionNode.parentNode.removeChild(descriptionNode)

            more = ''
            if src_type == 'album':
                more = '<p><a href="%s">This image belongs to an album</a></p>' % (link_url)

            description = dom.createElement('description')
            description.appendChild(dom.createTextNode('<p><img src="%s"></p>%s' % (hotlink, more)))

            item.appendChild(description)

            #replaceChildren(linkNode, dom.createTextNode(hotlink))
            #replaceChildren(item.getElementsByTagName('guid')[0], dom.createTextNode(hotlink))

            mc = dom.createElement('media:content')
            mc.setAttribute('url', hotlink)
            mc.setAttribute('medium', 'image')
            item.appendChild(mc)


