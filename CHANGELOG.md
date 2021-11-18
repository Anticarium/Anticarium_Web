# Anticarium_Web

- MODIFY: Flask application now permanently stores data in database file and in json files
- ADD: `.gitignore` `/json_files*` directory
- ADD: `.gitignore` `anticarium.db` database file
- ADD: `anticarium_web.wsgi` to run `mod_wsgi`
- ADD: `__init__.py` to launch `mod_wsgi`
- ADD: Data serializers for each data type in `shared_types`. All serializers and deserializers are located in `models.py`
- MODIFY: Move `saveJson` and `readJson` functions to seperate `helper.py` file 
- ADD: `DBActions` interface class for database manipulations
- ADD: `sqlite.py` script that creates `anticarium.db` SQLite database file