import json

# Saves json to passed path of file
def saveJson(filePath, dct):
    jsonFile = open(filePath, "w")
    jsonFile.write(json.dumps(dct))

# Reads json from passed path to file
def readJson(filePath):
    jsonFile = open(filePath, "r")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    return jsonData

def buildRegimesList(savedRegimes):    
    regimes = []
    for i in savedRegimes.savedRegimes:
        regimes.append(i.name)
    return regimes        