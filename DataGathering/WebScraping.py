import os
import time
import requests
from bs4 import BeautifulSoup
import FileHandling

# Make a request to [url] and then wait for [delay] seconds return response
def myRequest(url: str, delay: float = 1) -> requests.Response:
    print("Requesting:", url)
    session = requests.Session()
    cookies = {"JSESSIONID":"199Optg7fnXWyVx1uqnFGaXoDgNxCcrAQvBSBCjA.sas02"}
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
    response = session.get(url, headers = headers, cookies = cookies)
    time.sleep(delay)
    return response

# Wrapper to make a beautifulsoup object from response
def toSoup(response: requests.Response):
    return BeautifulSoup(response.text, "html.parser")

# Helper function
def addProtocolAndServerToAll(URLPaths: [str], protocolAndServer: str) -> [str]:
    return [protocolAndServer + URLPath for URLPath in URLPaths]

# Helper function
def findNthOccurence(strToSearch: str, subString: str, nOccurence: int) -> int:
    index = -1
    for i in range(0, nOccurence): 
        index = strToSearch.find(subString, index + 1)
    return index

def findLinks(soup: BeautifulSoup, name: str) -> [str]:
    tags = soup.find_all("a", string=name)
    URLs = [tag.get("href") for tag in tags]
    return URLs

# e.g find all links that lead to the "Spiele" - page 
def findURLsWithKeyIn(url: str, key: str, delay: float = 1) -> [str]:
    soup = toSoup(myRequest(url, delay))
    URLPaths = findLinks(soup, key) # only backpart of urls (-> without server and protocol)
    protocolAndServer = url[0:findNthOccurence(url, "/", 3)]
    fullURLs = addProtocolAndServerToAll(URLPaths, protocolAndServer)
    return fullURLs

# seperate function since the site is built differently and normal method wont work
def findAlleSpieleURLs(soup: BeautifulSoup) -> [str]:
    everyTagWithLink = soup.find_all("a")
    urls = []
    for tag in everyTagWithLink:
        if not tag.string is None:
            if "alle Spiele" in tag.string:
                urls.append(tag.get("href"))
    return addProtocolAndServerToAll(urls, "https://www.volleyball-bundesliga.de/")

# seperate function since the site is built differently and normal method wont work
def findStatisticURLs(soup: BeautifulSoup) -> [str]:
    urls = []
    allTagsWithStats = soup.find_all(class_="glyphicons glyphicons-stats")
    for tag in allTagsWithStats:
        tag_with_link = tag.parent.parent.parent.parent
        urls.append(tag_with_link.get("href"))
    return urls

def getLastNSeasonBundesLigaFileUrls(delay: float = 1, numberOfSeasons: int = 1) -> [str]:
    urls = []
    startingURLs = FileHandling.readFileToList("../Data/startingURLs.txt")
    for startingURL in startingURLs:
        spieleURLs = findURLsWithKeyIn(startingURL, "Spiele", delay)
        spieleSoups = [toSoup(myRequest(url, delay)) for url in spieleURLs][0:numberOfSeasons] #select only first few depending on number of seasons
        for spieleSoup in spieleSoups:
            alleSpieleURLs = findAlleSpieleURLs(spieleSoup)
            for alleSpieleURL in alleSpieleURLs:
                soup = toSoup(myRequest(alleSpieleURL, delay))
                statisticULRs = findStatisticURLs(soup)
                for statisticULR in statisticULRs:
                    urls.append(statisticULR)
    return urls