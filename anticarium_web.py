# To run in console: python -m flask run
# To run in console, local network: python -m flask run --host=0.0.0.0

import json
from flask import Flask, jsonify, json, request
from random import uniform, randint
app = Flask(__name__)

def readJson(filePath):
    jsonFile = open(filePath, "r")
    jsonData = json.load(jsonFile)
    jsonFile.close()
    return jsonData

regimesJson = readJson("/home/pi/Desktop/Anticarium_Web/Anticarium_Web/json_files/Regimes.json")
regimeIdJson = readJson("/home/pi/Desktop/Anticarium_Web/Anticarium_Web/json_files/RegimeId.json")
controlJson = readJson("/home/pi/Desktop/Anticarium_Web/Anticarium_Web/json_files/Control.json")
savedRegimesJson = readJson("/home/pi/Desktop/Anticarium_Web/Anticarium_Web/json_files/SavedRegimes.json")
sensorDataJson = readJson("/home/pi/Desktop/Anticarium_Web/Anticarium_Web/json_files/SensorData.json")

@app.route("/")
def home():
    return "Hello, Flask!"


iterator = 0
@app.route("/test")
def testOutput():
    global iterator
    iterator += 1
    return str(iterator)

@app.route("/send/regime", methods=["POST"])
def saveRegime():
    requestJson = request.get_json()
    index = requestJson["regime_id"]["id"]

    global regimesJson
    global savedRegimesJson   
    global regimeIdJson
    global controlJson

    if index == -1: # New regime
        regimesJson["regimes"].append(requestJson["name"])
        savedRegimesJson["saved_regimes"].append(requestJson)
        regimeIdJson["id"] = len(savedRegimesJson["saved_regimes"]) - 1
        savedRegimesJson["saved_regimes"][regimeIdJson["id"]]["regime_id"] = regimeIdJson
        controlJson["regime_value"] = requestJson["regime_value"]
    else: # Edit regime
        regimesJson["regimes"][index] = requestJson["name"]
        savedRegimesJson["saved_regimes"][index] = requestJson
    
    return ('', 204) 

@app.route("/send/regime_id", methods=["POST"])
def saveRegimeId():
    regimeId = request.get_json()["id"]

    global regimeIdJson
    if regimeId >= 100: # If deletion was requested
        regimeId = regimeId - 100
        global savedRegimesJson
        savedRegimesJson["saved_regimes"].pop(regimeId)
        global regimesJson
        regimesJson["regimes"].pop(regimeId)
        if regimeIdJson["id"] == regimeId: # If deleted current regime, set current id to Custom regime
            regimeIdJson["id"] = -1
        
        # Update saved regimes indexes
        savedRegimesLength = len(savedRegimesJson["saved_regimes"])
        for i in range(regimeId, savedRegimesLength, 1):
            savedRegimesJson["saved_regimes"][i]["regime_id"]["id"] = i

    else:
        regimeIdJson["id"] = request.get_json()["id"]

    return ('', 204)

@app.route("/send/control", methods=["POST"])
def saveControlData():
    global controlJson
    controlJson = request.get_json()

    global regimeIdJson
    currentId = regimeIdJson["id"]

    # Set current id to -1 to indicate that there is no regime for now
    if currentId != -1:
        currentRegimeValue = savedRegimesJson["saved_regimes"][currentId]["regime_value"]        
        # Check if temperature or moisture changed
        isSameTemperature = currentRegimeValue["temperature"] == controlJson["regime_value"]["temperature"] 
        isSameMoisture = currentRegimeValue["moisture"] == controlJson["regime_value"]["moisture"]
        if not (isSameTemperature and isSameMoisture):
            # Yes: Custom regime
            regimeIdJson["id"] = -1

    return ('', 204)

@app.route("/send/sensor_data", methods=["POST"])
def saveSensorData():
    global sensorDataJson
    sensorDataJson = request.get_json()
    return ('', 204)    

@app.route("/request/sensor_data")
def returnSensorData():
    # Return real sensor data
    data = jsonify(sensorDataJson)

    # Emulate random sensor data
    # data = jsonify(
    #     temperature=uniform(15.0, 40.0),
    #     humidity=randint(0, 100),
    #     moisture=randint(0, 100),
    # )

    data.headers['Anticarium_content_description'] = "Sensor data" 
    return data

    
@app.route("/request/regime_id")
def returnRegimeId():    
    returnValue = jsonify(regimeIdJson)
    returnValue.headers['Anticarium content description'] = "Regime id"     
    return returnValue

@app.route("/request/control")
def returnControl():
    returnValue = jsonify(controlJson)
    returnValue.headers['Anticarium content description'] = "Control" 
    return returnValue

@app.route("/request/regimes")
def returnRegimes():
    returnValue = jsonify(regimesJson)    
    returnValue.headers['Anticarium content description'] = "Regimes" 
    return returnValue

@app.route("/request/regime")
def returnRegime():
    index = regimeIdJson["id"]
    global controlJson

    # Is custom regime active?
    data = None
    if index == -1:
        # Yes: Create fake regime with current control value
        customRegime = {
            'name': '',
            'regime_id':{
                'id': -1
            },
            'regime_value':{
                'temperature': controlJson["regime_value"]["temperature"],
                'moisture': controlJson["regime_value"]["moisture"],
            }
        }
        data = jsonify(customRegime)
    else:
        # No: Send current regime
        data = jsonify(savedRegimesJson["saved_regimes"][index])
        controlJson["regime_value"] = savedRegimesJson["saved_regimes"][index]["regime_value"]

    data.headers['Anticarium content description'] = "Regime"
    
    return data        

@app.route("/request/saved_regimes")
def returnSavedRegimes():    
    returnValue = jsonify(savedRegimesJson)    
    returnValue.headers['Anticarium content description'] = "Saved regimes" 
    return returnValue

if __name__ == "__main__":
	app.run()
