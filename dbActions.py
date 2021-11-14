import sqlite3, models

class DbActions():
    def __init__(self, dbFile):
        self.connection = None
        self.dbFile = dbFile

    # Connects to database
    def connectToDatabase(self):
        self.connection = sqlite3.connect(self.dbFile, check_same_thread=False)

    # Returns SavedRegimes object, with values queried from database
    def getSavedRegimes(self):
        data = self.connection.execute("SELECT * from REGIMES")

        savedRegimes = models.SavedRegimes([])

        for i in data:
            regimeId = models.RegimeId(i[0])
            name = i[1]
            regimeValue = models.RegimeValue(i[3], i[2])
            regime = models.Regime(name, regimeId, regimeValue)
            savedRegimes.savedRegimes.append(regime)

        return savedRegimes
    
    def saveRegime(self, regime):
        query = f"INSERT INTO REGIMES (ID, NAME, TEMPERATURE, MOISTURE) \
            VALUES ({regime.regimeId.id},'{regime.name}',{regime.regimeValue.temperature},{regime.regimeValue.moisture})"
        self.connection.execute(query)

    
    def editRegimeAt(self, regime, id):
        query = f"UPDATE REGIMES set  \
            NAME = '{regime.name}'\
            TEMPERATURE = {regime.regimeValue.temperature}    \
            MOISTURE = {regime.regimeValue.moisture} \
            where ID = {id} \
            );"
        self.connection.execute(query)

    def deleteRegimeAt(self, id):
        query = f"DELETE from REGIMES where ID = {id}"
        self.connection.execute(query)
        
        # Get amount of database rows
        query = f"COUNT(*)"
        rowCount = self.connection.execute(query)

        # Update row IDs
        for i in range(id, rowCount - 1):
            query = f"UPDATE REGIMES set \
                ID = {i} \
                where ID = {i + 1}"
            self.connection.execute(query)
