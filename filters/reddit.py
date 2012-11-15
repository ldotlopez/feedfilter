import domutils
import bs4 as BeautifulSoup

class RedditLinkFollow(object):
    def _debug(self, msg):
        pass

    def process(self, dom):
        cache = Cache(debug = False)

        items = dom.getElementsByTagName('item')

        for i in xrange(0, len(items)):
            print "Item %d of %d" % (i+1, len(items))
            item = items[i]

            link_node = item.getElementsByTagName('link')[0]
            link_url = link_node.childNodes[0].data

            # Fetch page
            try:
                (buff, cached) = cache.fetch_url(link_url)
                soup = BeautifulSoup.BeautifulSoup(buff)
            except IOError as e:
                print "Unable to load url %s: %s" % (link_url, e)
                continue

            # Dont do anything
            if soup.title.text == 'Too Many Requests':
                cache.delete(link_url)
                print "Reddit is angry"
                continue

            try:
                real_link_url = soup.find('p', 'title').find('a', 'title').get('href')
            except AttributeError:
                cache.delete(link_url)
                print "Unable to retrieve original link for '%s'" % soup.title
                continue

            self._debug("Got real link on '%s' (%s), replacing" % (soup.title.text, real_link_url))

            domutils.replaceChildren(link_node, dom.createTextNode(real_link_url))
            replaceChildren(item.getElementsByTagName('guid')[0], dom.createTextNode(real_link_url))

            if not cached:
                time.sleep(2)

