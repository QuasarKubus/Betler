import WebScraping
import Downloading
import PdfsToImage
import ImageScraping

#statisticURLs = WebScraping.getLastNSeasonBundesLigaFileUrls(delay = 0.2, numberOfSeasons = 2)

#notSaved = Downloading.getNotSavedPDFs(statisticURLs)

#Downloading.saveToFile(notSaved, delay = 0.2)

#PdfsToImage.convertAndSave()

#ImageScraping.scrapeImages()

print(WebScraping.getPlayerNames()[0])