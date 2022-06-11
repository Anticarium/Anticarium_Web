# Anticarium_Web

- MODIFY: Return empty data with `Regime_deleted` in `Anticarium_content_description` header on `/send/regime_id` if deletion was requested
- MODIFY: Return Regime on `/send/regime_id` if deletion was not requested
- MODIFY: Return empty data with `Regime_saved` in `Anticarium_content_description` header on `/send/regime`

# 1.0.1
- MODIFY: Fixed database and various other permission errors in local Anticarium_Web dist using `setup_web.sh`
- REMOVE: Removed VERSION file as it is not used
- MODIFY: Fixed apache2 multiple threads issue with `setup_web.sh`

# 1.0.0
- ADD: First time setup script for Raspberry Pi to automatically configure WEB server
- MODIFY: Python scripts in this repo now use ANTICARIUM_WEB_PATH environment variable to access this repo
- MODIFY: anticarium_web.example now uses ANTICARIUM_WEB_PATH environment variable to access scripts provided by this repo 
- MODIFY: anticarium_web.example now uses ANTICARIUM_SERVER_IP environment variable as server ip
- ADD: Apache2 prefork module configuration, in 'apache2.conf', to process all requests in single thread
- ADD: `apache2.conf.example` apache2 configuration example file
- MODIFY: Flask application now permanently stores data in database file and in json files
- ADD: `.gitignore` `/json_files*` directory
- ADD: `.gitignore` `anticarium.db` database file
- ADD: `anticarium_web.wsgi` to run `mod_wsgi`
- ADD: `__init__.py` to launch `mod_wsgi`
- ADD: Data serializers for each data type in `shared_types`. All serializers and deserializers are located in `models.py`
- MODIFY: Move `saveJson` and `readJson` functions to seperate `helper.py` file 
- ADD: `DBActions` interface class for database manipulations
- ADD: `sqlite.py` script that creates `anticarium.db` SQLite database file
