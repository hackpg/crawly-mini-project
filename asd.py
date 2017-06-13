import webbrowser
import os.path
from urllib.request import urlopen
from link_finder import LinkFinder
from domain import *
from general import *
import threading
import shutil
from pymongo import Connection
from newspaper import Article

class Spider:

    project_name = ''
    base_url = ''

    domain_name = ''

    queue_file = ''
    crawled_file = ''
    apli_file = ''
    queue = set()
    crawled = set()
    apli = set()
    count=1;

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url

        Spider.domain_name = domain_name

        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'
        Spider.apli_file = Spider.project_name + '/apli.html'
        self.boot()
        self.crawl_page('First spider', Spider.base_url)


    # Creates directory and files for project on first run and starts the spider
    @staticmethod
    def boot():
        if os.path.exists(Spider.project_name):
            shutil.rmtree(Spider.project_name)
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    # Updates user display, fills queue and updates files
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled  ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)
            if Spider.count <= 20:
                Spider.apli.add(page_url)
                con = Connection()
                db = con.CRAWLY
                testieee = db.testieee
                art = Article(page_url)
                art.download()
                art.parse()
                with open(Spider.apli_file, "a+") as f:
                    m = page_url.split('/')
                    msg = "" + m[-4] + "  " + m[-3] + "  " + m[-2]
                    msg = msg.replace('/', '  ')
                    msg = msg.replace('.', '  ')
                    msg = msg.replace('-', '  ')
                    #f.write("<p><a href=" + page_url + ">" + msg + "</a></p>")
                    testieee.insert({'set': {'heading': art.title, 'url': page_url,'image':art.top_image,'text':art.text}})
                Spider.count=Spider.count+1

            else:
                #threading._shutdown()
                webbrowser.open("file:///" + os.path.abspath(Spider.apli_file))
                os._exit(1)


            Spider.update_files()

    # Converts raw response data into readable information and checks for proper html formatting
    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    # Saves queue data to project files
    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url) :
                continue
            Spider.queue.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)
        #set_to_file_HTML(Spider.apli, Spider.apli_file)

