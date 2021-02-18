import requests
import time
import FileHandling
from bs4 import BeautifulSoup
import os

def removeProtocolAndServer(url: str) -> str:
    url = url.replace(":443","")
    url = url.replace("http://live.volleyball-bundesliga.de/", "")
    url = url.replace("https://www.volleyball-bundesliga.de/", "")
    url = url.replace("http://www.volleyball-bundesliga.de/", "")
    url = url.replace("https://www.volleyball-bundesliga.de:443/", "")
    return url

def getNotSavedPDFs(newlyScrapedPDFURLs: [str]) -> [str]:
    notSavedPDFURLs = []
    savedPDFURLs = FileHandling.readFileToList("../Data/savedURLs.txt")

    for URL in newlyScrapedPDFURLs:
        if not URL in savedPDFURLs:
            notSavedPDFURLs.append(URL)
    return notSavedPDFURLs

def saveToFile(URLs: [str], delay: float = 1):
    savedURLs = []
    for URL in URLs:
        print("Saving: " + URL)
        savedURLs.append(URL)
        session = requests.Session()
        cookies = {"JSESSIONID":"pest8CiVvKIcEytxWo1u1dDHEq-1T57F7HP_OVAF.sas02"}
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0"}
        response = session.get(URL, headers = headers, cookies = cookies)
        URL = removeProtocolAndServer(URL)
        URL = URL.replace("/", "_")
        if not ".pdf" in URL:
            URL += ".pdf"
        with open("../Data/Pdfs/"+URL, "wb") as file:
            file.write(response.content)
        time.sleep(delay)
    FileHandling.appendListToFile(savedURLs, "../Data/savedURLs.txt")