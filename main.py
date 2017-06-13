import webbrowser,os.path
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
import sys

PROJECT_NAME = 'resonance'#http://timesofindia.indiatimes.com/
#print(str(sys.argv))
#fin = str(sys.argv[1])http://edition.cnn.com/entertainment
#print(fin)http://www.news18.com/
#if fin == 'TOI':http://timesofindia.indiatimes.com/ http://a4academics .com/final-year-be-project/12-be-ece-electronics-and-communication-project
HOMEPAGE = 'http://iot-journal.weebly.com/call-for-papers.html'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
#string = 'http://www.hindustantimes.com/'
queue = Queue()
#queue.put(string)
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)





# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    count = 1;
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()

