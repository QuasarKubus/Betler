from pdf2image import convert_from_path
from PIL import Image
import os
import FileHandling

def checkUpdates():
    newFiles = []
    alreadyImageNames = FileHandling.readFileToList("../Data/savedImages.txt")
    pdfNames = FileHandling.getAllFileNamesIn("../Data/Pdfs")
    for pdfName in pdfNames:
        if not (pdfName in alreadyImageNames):
            newFiles.append(pdfName)
    return newFiles

def convertAndSave():
    savedImages = []
    for fileName in checkUpdates():
        savedImages.append(savedImages)
        print("Converting:", fileName)
        images = convert_from_path(fileName)
        for image in images:
            fileName = fileName.replace("../Data/Pdfs", "../Data/Images")
            fileName = fileName.replace(".pdf", ".png")
            image.save(fileName)