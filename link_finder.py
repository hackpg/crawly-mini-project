from html.parser import HTMLParser
from urllib import parse
from bs4 import BeautifulSoup


class LinkFinder(HTMLParser):

    new=list()
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    url = url.replace(" ","")
                    if url.find('iot') != -1 and len(url)>10:
                        self.links.add(url)



    def page_links(self):
        return self.links

    def error(self, message):
        pass
