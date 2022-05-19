import models, os
from helper import buildRegimesList, readJson, saveJson
from dbActions import DbActions
from flask import Flask, jsonify, request
app = Flask(__name__)

ANTICARIUM_WEB_PATH = os.environ["ANTICARIUM_WEB_PATH"]

database = DbActions(f"{ANTICARIUM_WEB_PATH}/anticarium.db")
database.connectToDatabase()

# Get path to json_files folder
jsonFilesPath = f"{ANTICARIUM_WEB_PATH}/json_files"

# Set path variables to json files
REGIME_ID_JSON_PATH = jsonFilesPath + "/RegimeId.json"
CONTROL_JSON_PATH = jsonFilesPath + "/Control.json"
SENSOR_DATA_JSON_PATH = jsonFilesPath + "/SensorData.json"

# Read json files
savedRegimesJson = database.getSavedRegimes()
regimesJson = models.Regimes(buildRegimesList(savedRegimesJson))
regimeIdJson = models.toRegimeId(readJson(REGIME_ID_JSON_PATH))
controlJson = models.toControl(readJson(CONTROL_JSON_PATH))
sensorDataJson = models.toSensorData(readJson(SENSOR_DATA_JSON_PATH))

# Header which contents describes what data does request contain
ANTICARIUM_HEADER = 'Anticarium_content_description'

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
        newRegime = requestJson
        newRegime.regimeId.id = len(savedRegimesJson.savedRegimes)

        regimesJson.regimes.append(newRegime.name)
        savedRegimesJson.savedRegimes.append(newRegime)
        regimeIdJson.id = newRegime.regimeId.id
        controlJson.regimeValue = newRegime.regimeValue

        saveJson(REGIME_ID_JSON_PATH, models.fromRegimeId(regimeIdJson))
        database.saveRegime(newRegime)
    else: # Edit regime
        regimesJson.regimes[index] = requestJson.name
        savedRegimesJson.savedRegimes[index] = requestJson
        
        database.editRegimeAt(requestJson, index)

    return ('', 204) 

@app.route("/send/regime_id", methods=["POST"])
def saveRegimeId():
    regimeId = models.toRegimeId(request.get_json()).id

    global regimeIdJson
    if regimeId >= 100: # If deletion was requested
        regimeId = regimeId - 100
        global savedRegimesJson
        savedRegimesJson.savedRegimes.pop(regimeId)
        database.deleteRegimeAt(regimeId)
        global regimesJson
        regimesJson.regimes.pop(regimeId)
        if regimeIdJson.id == regimeId:
            # If deleted current regime, set current id to Custom regime
            regimeIdJson.id = -1
        elif regimeIdJson.id > regimeId:
            # If deleted regime above regime of current regime id, make current regime smaller by one
            regimeIdJson.id -= 1
        
        # Update saved regimes indexes
        savedRegimesLength = len(savedRegimesJson.savedRegimes)
        for i in range(regimeId, savedRegimesLength, 1):
            savedRegimesJson.savedRegimes[i].regimeId.id = i
    else:
        regimeIdJson.id = regimeId
    
    saveJson(REGIME_ID_JSON_PATH, models.fromRegimeId(regimeIdJson))
    return ('', 204)

@app.route("/send/control", methods=["POST"])
def saveControlData():
    global controlJson
    controlJson = models.toControl(request.get_json())
    saveJson(CONTROL_JSON_PATH, models.fromControl(controlJson))

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
            saveJson(REGIME_ID_JSON_PATH, models.fromRegimeId(regimeIdJson))

    return ('', 204)

@app.route("/send/sensor_data", methods=["POST"])
def saveSensorData():
    global sensorDataJson
    sensorDataJson = models.toSensorData(request.get_json())
    return ('', 204)    

@app.route("/request/sensor_data")
def returnSensorData():
    data = jsonify(models.fromSensorData(sensorDataJson))
    data.headers[ANTICARIUM_HEADER] = "Sensor_data" 
    return data

    
@app.route("/request/regime_id")
def returnRegimeId():    
    returnValue = jsonify(models.fromRegimeId(regimeIdJson))
    returnValue.headers[ANTICARIUM_HEADER] = "Regime_id"     
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
        saveJson(CONTROL_JSON_PATH, models.fromControl(controlJson))

    data.headers[ANTICARIUM_HEADER] = "Regime"
    
    return data        

@app.route("/request/saved_regimes")
def returnSavedRegimes():    
    returnValue = jsonify(models.fromSavedRegimes(savedRegimesJson))    
    returnValue.headers[ANTICARIUM_HEADER] = "Saved_regimes" 
    return returnValue

if __name__ == "__main__":
	app.run()
