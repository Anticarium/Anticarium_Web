class RegimeId():
    def __init__(self, id):
        self.id = id

def toRegimeId(dct):
    return RegimeId(dct['id'])

def fromRegimeId(regimeId):
    dct = {
        'id': regimeId.id
    }
    return dct

class SensorData():
    def __init__(self, temperature, humidity, moisture):
        self.temperature = temperature
        self.humidity = humidity
        self.moisture = moisture

def toSensorData(dct):
    return SensorData(dct['temperature'], dct['humidity'], dct['moisture'])

def fromSensorData(sensorData):
    dct = {
        'temperature': sensorData.temperature,
        'humidity': sensorData.humidity,
        'moisture': sensorData.moisture
    }
    return dct

class Regimes():
    def __init__(self, regimes):
        self.regimes = regimes

def toRegimes(dct):
    return Regimes(dct['regimes'])

def fromRegimes(regimes):
    dct = {'regimes':[]}
    for i in regimes.regimes:
        dct['regimes'].append(i)
    return dct

class RegimeValue():
    def __init__(self, moisture, temperature):
        self.moisture = moisture
        self.temperature = temperature

def toRegimeValue(dct):
    return RegimeValue(dct['moisture'], dct['temperature'])

def fromRegimeValue(regimeValue):
    dct = {
        'temperature': regimeValue.temperature,
        'moisture': regimeValue.moisture
    }
    return dct

class Control():
    def __init__(self, lightPercentage, windPercentage, regimeValue):
        self.lightPercentage = lightPercentage
        self.windPercentage = windPercentage
        self.regimeValue = regimeValue

def toControl(dct):
    return Control(dct['light_percentage'], dct['wind_percentage'], toRegimeValue(dct['regime_value']))

def fromControl(control):
    dct = {
        'light_percentage': control.lightPercentage,
        'wind_percentage': control.windPercentage,
        'regime_value': fromRegimeValue(control.regimeValue)
    }
    return dct

class SavedRegimes():
    def __init__(self, savedRegimes):
        self.savedRegimes = savedRegimes

def toSavedRegimes(dct):
    savedRegimes = []
    for i in dct['saved_regimes']:
        savedRegimes.append(toRegime(i))

    return SavedRegimes(savedRegimes)

def fromSavedRegimes(savedRegimes):
    dct = {
        'saved_regimes':[]
        }
    
    for i in savedRegimes.savedRegimes:
        dct['saved_regimes'].append(fromRegime(i))
    
    return dct


class Regime():
    def __init__(self, name, regimeId, regimeValue):
        self.name = name
        self.regimeId = regimeId
        self.regimeValue = regimeValue

def toRegime(dct):
    return Regime(dct['name'], toRegimeId(dct['regime_id']), toRegimeValue(dct['regime_value']))

def fromRegime(regime):
    dct = {
        'name': regime.name,
        'regime_id': fromRegimeId(regime.regimeId),
        'regime_value': fromRegimeValue(regime.regimeValue)
    }
    return dct