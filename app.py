# To run in console: python -m flask run
# To run in console, local network: python -m flask run --host=0.0.0.0

import json, models, os
from flask import Flask, jsonify, json, request
app = Flask(__name__)

# Reads json from passed path to file
def readJson(filePath):
    jsonFile = open(filePath, "r")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    return jsonData

# Get path to json_files folder
jsonFilesPath = os.path.realpath(__file__) + "/json_files"

# Read json files
regimesJson = models.toRegimes(readJson(jsonFilesPath + "/Regimes.json"))
regimeIdJson = models.toRegimeId(readJson(jsonFilesPath + "/RegimeId.json"))
controlJson = models.toControl(readJson(jsonFilesPath + "/Control.json"))
savedRegimesJson = models.toSavedRegimes(readJson(jsonFilesPath + "/SavedRegimes.json"))
sensorDataJson = models.toSensorData(readJson(jsonFilesPath + "/SensorData.json"))

# Header which contents describes what data does request contain
ANTICARIUM_HEADER = 'Anticarium content description'

@app.route("/")
def home():
    return "Anticarium"

@app.route("/send/regime", methods=["POST"])
def saveRegime():
    requestJson = models.toRegime(request.get_json())
    index = requestJson.regimeId.id

    global regimesJson
    global savedRegimesJson   
    global regimeIdJson
    global controlJson

    if index == -1: # New regime
        regimesJson.regimes.append(requestJson.name)
        savedRegimesJson.savedRegimes.append(requestJson)
        regimeIdJson.id = len(savedRegimesJson.savedRegimes) - 1
        savedRegimesJson.savedRegimes[regimeIdJson.id].regimeId = regimeIdJson
        controlJson.regimeValue = requestJson.regimeValue
    else: # Edit regime
        regimesJson.regimes[index] = requestJson.name
        savedRegimesJson.savedRegimes[index] = requestJson

    return ('', 204) 

@app.route("/send/regime_id", methods=["POST"])
def saveRegimeId():
    regimeId = models.toRegimeId(request.get_json()).id

    global regimeIdJson
    if regimeId >= 100: # If deletion was requested
        regimeId = regimeId - 100
        global savedRegimesJson
        savedRegimesJson.savedRegimes.pop(regimeId)
        global regimesJson
        regimesJson.regimes.pop(regimeId)
        if regimeIdJson.id == regimeId: # If deleted current regime, set current id to Custom regime
            regimeIdJson.id = -1
        
        # Update saved regimes indexes
        savedRegimesLength = len(savedRegimesJson.savedRegimes)
        for i in range(regimeId, savedRegimesLength, 1):
            savedRegimesJson.savedRegimes[i].regimeId.id = i

    else:
        regimeIdJson.id = regimeId

    return ('', 204)

@app.route("/send/control", methods=["POST"])
def saveControlData():
    global controlJson
    controlJson = models.toControl(request.get_json())

    global regimeIdJson
    currentId = regimeIdJson.id

    # Set current id to -1 to indicate that there is no regime for now
    if currentId != -1:
        currentRegimeValue = savedRegimesJson.savedRegimes[currentId].regimeValue        
        # Check if temperature or moisture changed
        isSameTemperature = currentRegimeValue.temperature == controlJson.regimeValue.temperature 
        isSameMoisture = currentRegimeValue.moisture == controlJson.regimeValue.moisture
        if not (isSameTemperature and isSameMoisture):
            # Yes: Custom regime
            regimeIdJson.id = -1

    return ('', 204)

@app.route("/send/sensor_data", methods=["POST"])
def saveSensorData():
    global sensorDataJson
    sensorDataJson = models.toSensorData(request.get_json())
    return ('', 204)    

@app.route("/request/sensor_data")
def returnSensorData():
    data = jsonify(models.fromSensorData(sensorDataJson))
    data.headers[ANTICARIUM_HEADER] = "Sensor data" 
    return data

    
@app.route("/request/regime_id")
def returnRegimeId():    
    returnValue = jsonify(models.fromRegimeId(regimeIdJson))
    returnValue.headers[ANTICARIUM_HEADER] = "Regime id"     
    return returnValue

@app.route("/request/control")
def returnControl():
    returnValue = jsonify(models.fromControl(controlJson))
    returnValue.headers[ANTICARIUM_HEADER] = "Control" 
    return returnValue

@app.route("/request/regimes")
def returnRegimes():
    returnValue = jsonify(models.fromRegimes(regimesJson))    
    returnValue.headers[ANTICARIUM_HEADER] = "Regimes" 
    return returnValue

@app.route("/request/regime")
def returnRegime():
    index = regimeIdJson.id
    global controlJson

    # Is custom regime active?
    data = None
    if index == -1:
        # Yes: Create fake regime with current control value
        customRegimeId = models.RegimeId(-1)
        customRegimeValue = models.RegimeValue(controlJson.regimeValue.moisture, controlJson.regimeValue.temperature)
        customRegime = models.Regime('', customRegimeId, customRegimeValue)
        data = jsonify(models.fromRegime(customRegime))
    else:
        # No: Send current regime
        data = jsonify(models.fromRegime(savedRegimesJson.savedRegimes[index]))
        controlJson.regimeValue = savedRegimesJson.savedRegimes[index].regimeValue

    data.headers[ANTICARIUM_HEADER] = "Regime"
    
    return data        

@app.route("/request/saved_regimes")
def returnSavedRegimes():    
    returnValue = jsonify(models.fromSavedRegimes(savedRegimesJson))    
    returnValue.headers[ANTICARIUM_HEADER] = "Saved regimes" 
    return returnValue
