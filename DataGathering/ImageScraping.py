from PIL import Image
import os
import pytesseract
from pytesseract import Output
import csv
import FileHandling
import math

def loadImgCoordinates(path):
    with open(path,"r") as file:
        fileString = file.read()
        boxes = fileString.split("\n")
        boxes = [box.split(",") for box in boxes]
        boxesReturn = []
        for box in boxes:
            boxTmp = [box[0], int(box[1]), int(box[2]), int(box[3]), int(box[4])]
            boxesReturn.append(boxTmp)
        return boxesReturn


# configuration for tesserect, works better than standard configuration
customConfigTesseract = r'-l deu -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZöüäÖÄÜß1234567890.+-/* " --psm 7'

coordinates_07 = loadImgCoordinates("../Data/ImageCoordinatesDataVolley07.txt")
coordinates_4 = loadImgCoordinates("../Data/ImageCoordinatesDataVolley4.txt")

# bounding boxes of Data Volley signature
# needed to identify which coordinates to use
dV07_check_coord= coordinates_07[0]
dV4_check_coord = coordinates_4[0]


def getVersion(image):
    cropped_part_07 = image.crop((dV07_check_coord[1], dV07_check_coord[2], dV07_check_coord[3], dV07_check_coord[4]))
    cropped_part_4 = image.crop((dV4_check_coord[1], dV4_check_coord[2], dV4_check_coord[3], dV4_check_coord[4]))

    readString_07 = pytesseract.image_to_string(cropped_part_07, config=customConfigTesseract).strip()
    readString_4 = pytesseract.image_to_string(cropped_part_4, config=customConfigTesseract).strip()

    #print(readString_07)
    #print(readString_4)

    if "07" in readString_07:
        return "Data Volley 07"
    elif "4" in readString_4:
        return "Data Volley 4"
    return "not Data Volley"

def getUpdates():
    newFiles = []
    fileNames = FileHandling.getAllFileNamesIn("../Data/Images/")
    savedCSVs = FileHandling.readFileToList("../Data/savedCSVs.txt")
    for fileName in fileNames:
        if not fileName in savedCSVs:
            newFiles.append(fileName)
    return newFiles

def scrapeImages():
    scrapedImages = []
    counter = 0
    outOf = 0
    outOf = len(getUpdates())
    for fileName in getUpdates():
        counter += 1
        percent = "{}%".format(math.ceil(100*counter/outOf))
        print(percent, "Processing: ", fileName)
        image = Image.open(fileName)
        coordinates = []
        dataVolleyVersion = getVersion(image)

        os.remove(fileName)

        # select correct bounding boxes
        if dataVolleyVersion == "Data Volley 4":
            coordinates = coordinates_4
        else:
            print("Skipped because not Data Volley 4")
            continue
        
        # filter wrong size
        if image.size != (1654,2339):
            print("Skipped due to size:", fileName)
            continue

        dataDict = {}
        

        for coordinate in coordinates:

            cropped_part = image.crop((coordinate[1], coordinate[2], coordinate[3], coordinate[4]))
        
            readString = pytesseract.image_to_string(cropped_part, config=customConfigTesseract).strip()
            dataDict[coordinate[0]] = readString

        #print(dataDict)
        league = dataDict["League"].replace(" ","").replace(".","").replace("Bundesliga", "BL")
        if "M" in league:
            league = league[0:3] + "M"
        else:
            league = league[0:3] + "F"
        writer = csv.writer(open("../Data/CSVs/{}-{}-{}-{}.csv".format(league, dataDict["Date"].replace("/","_"), dataDict["NameTeam1"].replace(" ", ""), dataDict["NameTeam2"].replace(" ", "")), "w"))
        for key, val in dataDict.items():
            writer.writerow([key, val])
    FileHandling.appendListToFile(scrapedImages, "../Data/savedCSVs.txt")
