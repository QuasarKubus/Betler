import WebScraping
import Downloading
import PdfsToImage

statisticURLs = WebScraping.getLastNSeasonBundesLigaFileUrls(delay = 0.2, numberOfSeasons = 2)

notSaved = Downloading.getNotSavedPDFs(statisticURLs)

Downloading.saveToFile(notSaved, delay = 0.2)

PdfsToImage.convertAndSave()