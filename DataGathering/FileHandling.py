import os

def readFileToList(path: str) -> [str]:
    with open(path, "r") as f:
        lineList = f.read().split("\n")
        f.close()
        return lineList

def writeListToFile(listToWrite: [str], path: str):
    content = "\n".join(listToWrite)
    with open(path, "w") as f:
        if f.writable:
            f.write(content)
        else:
            print("Couldn't Write File", path)
            raise Exception()
        f.close()

def getAllFileNamesIn(path: str) -> [str]:
    fileNames = []
    for root, dirs, files in os.walk(path):
        for file in files:
            fileNames.append(os.path.join(root, file))
    return fileNames
