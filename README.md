# Anticarium_Web

This file describes `Anticarium_Web` data requests, response and processing.

# General

- All data gets transfered using json format
- Every json request and response is model that is serialized using `Shared_Types` in C++ programs
- When receiving or reading data, it gets serialized into object
- Data gets stored in two places. In SQLite database and in local variables, depending on situation

# Data storing requests

- All data storing requests happen using POST method
- Data requests have parameter `/send`, following by descriptor. For example: `/send/regime` requests to save passed regime
- Must respond with code `204`

## `/send/regime`

Creates and saves new regime or edits existing in database

### Regime id is `-1`

1. Create new regime and store it in database
2. Set this regime as current regime by assigning its values to according local variables

### Regime id is not `-1`

1. Edit regime in database using regime id

## `/send/regime_id`

Saves current Regime id in local variable or deletes saved Regime in database

### Regime id is bigger or equal than 100

1. Delete regime by subtracting 100 from regime id

### Regime id is smaller than 100

1. Store Regime id in local variable and in `./json_files/RegimeId.json`

## `/send/control`

Manages custom regime status

1. Store passed Control json in `./json_files/Control.json` and in local Control variable
2. If current Regime id is not `-1` (indicating, that some Regime was working previously), and temperature or moisture values have changed, set current Regime id value to `-1` to indicate, that custom Regime is working now, and store new Regime id value in `./json_files/RegimeId.json`.

## `/send/sensor_data`

Stores sensor data

1. Store sensor data in local variable

# Data requests

- All data requests happen using GET method
- Data requests have parameter `/request`, following by descriptor. For example: `/request/sensor_data` requests sensor data.
- All responses must have `Anticarium_content_description` header with appropriate value. 
 
## `/request/sensor_data`

1. Return Sensor data value, that was stored in local variable

## `/request/regime_id`

1. Return Regime id value, that was stored in local variable

## `/request/control`

1. Return Control value, that was stored in local variable

## `/request/regimes`

1. Return Regimes value, that was stored in local variable

## `/request/regime`

Returns current Regime value, or "fake" Regime value

### Current Regime id value is `-1`

1. Return Regime with:
    - Empty `name`
    - `-1` Regime id
    - `regime_value` with current Control value

### Current Regime id value is not `-1`

1. Return current Regime

## `/request/saved_regimes`

1. Return SavedRegimes, read form database 