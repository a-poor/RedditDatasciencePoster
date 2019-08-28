import re
import time
import sqlite3
import logging

import requests
from bs4 import BeautifulSoup
import praw
import feedparser

from credentials import *

##### Setup Logging #####
logging.basicConfig(
        filename="datasciencereddit.log", 
        filemode="a", 
        format="%(asctime)s – %(levelname)s – %(message)s",  
        level=logging.INFO
        )
logging.info("Starting program")


##### Store the Total Links Added #####
LINKS_ADDED = 0

##### Connect to the Database #####
logging.info("Connecting to the database...")
DB = sqlite3.connect("ds_links.db")
c = DB.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS "DsLinks"(
    "source" TEXT,
    "title" TEXT,
    "link" TEXT,
    "time" REAL,
    PRIMARY KEY ("title")
);""")

def add_to_db(source, title, link):
    global LINKS_ADDED
    title = title.lower().strip()
    title = re.sub(r"\s+", " ", title)
    c = DB.cursor()
    if not post_in_db(source, title, link):
        c.execute(
            "INSERT INTO DsLinks (source,title,link,time) VALUES (?,?,?,?);",
            (source, title, link, time.time())
            )
        LINKS_ADDED += 1
        return True
    else:
        logging.warning("Can't add to DB. Post already exists: %s: %s" % (source, title))
        return False

def post_in_db(source, title, link):
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM DsLinks WHERE source = ? AND title LIKE ?;", (source, "%"+title+"%"))
    if c.fetchone()[0] > 0:
        return True
    c.execute("SELECT COUNT(*) FROM DsLinks WHERE source = ? AND link LIKE ?;", (source, "%"+link+"%"))
    if c.fetchone()[0] > 0:
        return True
    return False


##### Connect to the Reddit #####
logging.info("Connecting to reddit...")
REDDIT = praw.Reddit(
    client_id=ID,
    client_secret=SECRET,
    user_agent="DsLinkPoster",
    username=U,
    password=P
    )
DS_LINKS = REDDIT.subreddit("ds_links")


def post(title, link):
    time.sleep(0.1)
    return DS_LINKS.submit(title, url=link)

##### Flowing Data #####
logging.info("Checking 'flowing data'...")
response = requests.get("https://flowingdata.com/")
soup = BeautifulSoup(response.content, features='lxml')
n = 0
for e in soup.find_all("div", attrs={"class":"entry"}):
    try:
        title_element = e.find("h1")
        title = title_element.text.strip()
        link = title_element.find("a").attrs["href"]
        if add_to_db("flowingdata", title, link):
            post("Flowingdata: "+title, link)
            n += 1
    except Exception as e:
        logging.error("Error occured", exc_info=True)
        
    else:
        DB.commit()
logging.info("%i links found" % n)
time.sleep(5)

##### datascience.com #####
logging.info("Checking 'datascience.com'...")
response = requests.get("https://www.datascience.com/resources/topic/white-papers")
soup = BeautifulSoup(response.content, features='lxml')
n = 0
for e in soup.find("div", attrs={"id":"container"}).find_all("a"):
    try:
        title = e.find("h6").text.strip()
        link = e.attrs["href"]
        add_to_db("datascience.com", title, link)
        post("datascience.com: "+title, link)
        n += 1
    except Exception as e:
        logging.error("Error occured", exc_info=True)
        
    else:
        DB.commit()
logging.info("%i links found" % n)
time.sleep(5)

##### datasciencefoundation #####
logging.info("Checking 'data science foundation'...")
response = requests.get("https://datascience.foundation/sciencewhitepaper")
soup = BeautifulSoup(response.content, features='lxml')
n = 0
for e in soup.find_all("header", attrs={"class":"post-header"}):
    try:
        title = e.find("h3").find("a").text.strip()
        link = e.find("h3").find("a").attrs["href"]
        add_to_db("datasciencefoundation", title, link)
        post("Datascience Foundation: "+title, link)
        n += 1
    except Exception as e:
        logging.error("Error occured", exc_info=True)
        
    else:
        DB.commit()
logging.info("%i links found from data science foundation" % n)
time.sleep(5)

##### ibm #####
logging.info("Checking 'ibm'...")
feed = feedparser.parse("http://feeds.feedburner.com/ibm-big-data-hub-whitepapers")
n = 0
for e in feed["entries"]:
    try:
        title = e["title"]
        link = e['link']
        add_to_db("ibm", title, link)
        post("IBM: "+title, link)
        n += 1
    except Exception as e:
        logging.error("Error occured", exc_info=True)
        
    else:
        DB.commit()
logging.info("%i links found from ibm" % n)
time.sleep(5)

##### arxiv #####
logging.info("Checking 'arxiv'...")
response = requests.get("https://arxiv.org/search/cs?query=data+science&searchtype=all&abstracts=show&order=-announced_date_first&size=50")
soup = BeautifulSoup(response.content, features='lxml')
n = 0
for e in soup.find("ol").find_all("li", attrs={"class":"arxiv-result"}):
    try:
        title = e.find("p", attrs={"class":"title"}).text.strip()
        link = e.find("p", attrs={"class":"list-title"}).find("a").attrs["href"]
        add_to_db("arxiv", title, link)
        post("arxiv: "+title, link)
        n += 1
    except Exception as e:
        logging.error("Error occured", exc_info=True)
        
    else:
        DB.commit()
logging.info("%i links found from arxiv" % n)
time.sleep(5)


logging.info("Search complete.")
logging.info("Total of %i links added.\n\n\n" % LINKS_ADDED)
