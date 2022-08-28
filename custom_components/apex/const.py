DOMAIN = "apex"
DEVICEIP = "deviceip"
MANUFACTURER = "Neptune Apex"

ADVANCED = "Advanced"
CTYPE = "ctype"
PROG = "prog"
DID = "did"
CONFIG = "config"
INPUTS = "inputs"
OUTPUTS = "outputs"
TYPE = "type"
VARIABLE = "variable"
VIRTUAL = "virtual"
IOTA_PUMP = "iotaPump|Sicce|Syncra"
EXTRA = "extra"
RANGE = "range"
MEASUREMENT = "measurement"
INPUT_CONFIG = "iconf"
OUTPUT_CONFIG = "oconf"
ICON = "icon"
STATUS = "status"
ON = "ON"
OFF = "OFF"
AUTO_ON = "AON"
AUTO_OFF = "AOF"

SWITCHES = {
    "outlet": {ICON: "mdi:power-socket-au"},
    "alert": {ICON: "mdi:alert"},
    VARIABLE: {ICON: "mdi:cog"},
    "afs": {ICON: "mdi:shaker"},
    "24v": {ICON: "mdi:home-lightning-bolt-outline"},
    "dos": {ICON: "mdi:test-tube"},
    VIRTUAL: {ICON: "mdi:monitor-account"},
    IOTA_PUMP: {ICON: "mdi:pump"}
}

SENSORS = {
    "Temp": {ICON: "mdi:water-thermometer", MEASUREMENT: "°C"},
    "Cond": {ICON: "mdi:shaker-outline"},
    "pH": {ICON: "mdi:test-tube"},
    "ORP": {ICON: "mdi:test-tube"},
    "digital": {ICON: "mdi:digital-ocean"},
    "Amps": {ICON: "mdi:lightning-bolt-circle", MEASUREMENT: "A"},
    "pwr": {ICON: "mdi:power-plug", MEASUREMENT: "W"},
    "volts": {ICON: "mdi:flash-triangle", MEASUREMENT: "V"},
    "alk": {ICON: "mdi:test-tube", MEASUREMENT: "dKh"},
    "ca": {ICON: "mdi:test-tube", MEASUREMENT: "ppm"},
    "mg": {ICON: "mdi:test-tube", MEASUREMENT: "ppm"},
    "dos": {ICON: "mdi:pump", MEASUREMENT: "ml"},
    IOTA_PUMP: {ICON: "mdi:pump", MEASUREMENT: "%"},
    VARIABLE: {ICON: "mdi:cog-outline"},
    VIRTUAL: {ICON: "mdi:cog-outline"},
}

MEASUREMENTS = {
    "Celcius": "°C",
    "Faren": "°F"
}

UPDATE_INTERVAL = "update_interval"
UPDATE_INTERVAL_DEFAULT = 60
