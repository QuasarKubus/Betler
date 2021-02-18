import os

def readFileToList(path: str) -> [str]:
    with open(path, "r") as f:
        lineList = f.read().split("\n")
        f.close()
        return lineList

def writeListToFile(listToWrite: [str], path: str):
    if len(listToWrite) == 0:
        return
    content = "\n".join(listToWrite)
    with open(path, "w") as f:
        if f.writable:
            f.write(content)
        else:
            print("Couldn't Write File", path)
            raise Exception()
        f.close()

def appendListToFile(listToWrite: [str], path: str):
    if len(listToWrite) == 0:
        return
    content = "\n".join(listToWrite)
    with open(path, "a") as f:
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

def readGameCSV(path: str):
    d = {}
    with open(path, "r") as file:
        content = file.read().strip()
        items = content.split("\n")
        for item in items:
            item = item.split(",")
            if len(item) == 2:
                tmp = item[1]
                try:
                    tmp = float(item[1])
                except:
                    if len(item[1]) <= 3:
                        tmp = ""
            d[item[0]] = tmp
    return d
