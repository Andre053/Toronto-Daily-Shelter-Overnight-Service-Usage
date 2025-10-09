'''
GLOBALS DEFINED
- GEOJSON_BASE
- FSV_CODES
- GLOBALS_PATH
- DATA_FOLDER
- GEOJSON_FSA_PATH
- GEOJSON_NB_PATH
- MONTHS
- GROUP_BY_AGGREGATE

'''
GEOJSON_BASE = {
    "type": "FeatureCollection",
    "name": "toronto_fsa_codes_generated",
    "crs": { 
        "type": "name", 
        "properties": { 
                "name": "urn:ogc:def:crs:EPSG::3347" 
            } 
        },
    "features": []
}

FSV_CODES = "'M4V' 'M4S' 'M4C' 'M8Y' 'M8W' 'M1H' 'M6S' 'M6E' 'M2M' 'M3C' 'M4T' 'M1L' 'M6G' 'M6H' 'M6A' 'M6B' 'M5R' 'M4K' 'M5T' 'M4G' 'M1S' 'M3A' 'M1N' 'M9C' 'M6J' 'M6K' 'M4L' 'M5S' 'M6M' 'M4E' 'M8V' 'M5A' 'M6N' 'M5N' 'M9A' 'M6R' 'M4B' 'M4J' 'M3H' 'M9M' 'M9R' 'M4N' 'M2K' 'M9N' 'M3L' 'M4A' 'M1B' 'M9W' 'M6C' 'M8Z' 'M5P' 'M5M' 'M4R' 'M2J' 'M2N' 'M4W' 'M1C' 'M4M' 'M6P' 'M1M' 'M1K' 'M3B' 'M9L' 'M1E' 'M2R' 'M1R' 'M2H' 'M4X' 'M9B' 'M1X' 'M5V' 'M4P' 'M6L' 'M2P' 'M2L' 'M8X' 'M5H' 'M1P' 'M9V' 'M5B' 'M1J' 'M9P' 'M3M' 'M3K' 'M1T' 'M1V' 'M3N' 'M3J' 'M1G' 'M1W' 'M4H' 'M4Y' 'M5C' 'M5J' 'M5E' 'M5G' 'M7A' 'M5X'".replace("'", "").split(" ")

GLOBALS_PATH = "./globals.json"

DATA_FOLDER = "../data"

GEOJSON_FSA_PATH = "../data/GeoJson/tor_fsa_cbf.geojson"

GEOJSON_NB_PATH = "../data/GeoJson/tor_neighbourhoods.geojson"

MONTHS = {
    1: 'JAN',
    2: 'FEB',
    3: 'MAR',
    4: 'APR',
    5: 'MAY',
    6: 'JUN',
    7: 'JUL',
    8: 'AUG',
    9: 'SEP',
    10: 'OCT',
    11: 'NOV',
    12: 'DEC',
}

GROUP_BY_AGGREGATE = {
    'SERVICE_USER_COUNT': ['mean', 'max', 'min'],
    'OCCUPIED_BEDS': ['mean', 'max', 'min'],
    'UNOCCUPIED_BEDS': ['mean', 'max', 'min'],
    'OCCUPIED_ROOMS': ['mean', 'max', 'min'],
    'UNOCCUPIED_ROOMS': ['mean', 'max', 'min'],
    'CAPACITY_ACTUAL_BED': ['mean', 'max', 'min'],
    'CAPACITY_FUNDING_BED': ['mean', 'max', 'min'],
    'PROGRAM_ID': 'nunique',
    'SHELTER_ID': 'nunique',
    'LOCATION_ID': 'nunique',
    'ORGANIZATION_ID': 'nunique',
}

