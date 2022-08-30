DOMAIN = "apex"
DEVICEIP = "deviceip"
MANUFACTURER = "Neptune Apex"

NAME = "name"
ADVANCED = "Advanced"
CTYPE = "ctype"
PROG = "prog"
DID = "did"
CONFIG = "config"
INPUTS = "inputs"
OUTPUTS = "outputs"
TYPE = "type"
EXTRA = "extra"
RANGE = "range"
MEASUREMENT = "measurement"
INPUT_CONFIG = "iconf"
OUTPUT_CONFIG = "oconf"
ICON = "icon"
STATUS = "status"

class ApexEntityType:
    OUTLET = "outlet"
    VARIABLE = "variable"
    VIRTUAL = "virtual"
    IOTA_PUMP = "iotaPump|Sicce|Syncra"
    DOS = "dos"

    @staticmethod
    def is_variable_type(type: str) -> bool:
        return (type == ApexEntityType.VARIABLE) or (type == ApexEntityType.VIRTUAL) or (type == ApexEntityType.DOS) or (type == ApexEntityType.IOTA_PUMP)

SWITCHES = {
    ApexEntityType.OUTLET: {ICON: "mdi:power-socket-au"},
    "alert": {ICON: "mdi:alert"},
    ApexEntityType.VARIABLE: {ICON: "mdi:cog"},
    "afs": {ICON: "mdi:shaker"},
    "24v": {ICON: "mdi:home-lightning-bolt-outline"},
    ApexEntityType.DOS: {ICON: "mdi:test-tube"},
    ApexEntityType.VIRTUAL: {ICON: "mdi:monitor-account"},
    ApexEntityType.IOTA_PUMP: {ICON: "mdi:pump"}
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
    ApexEntityType.DOS: {ICON: "mdi:pump", MEASUREMENT: "ml"},
    ApexEntityType.IOTA_PUMP: {ICON: "mdi:pump", MEASUREMENT: "%"},
    ApexEntityType.VARIABLE: {ICON: "mdi:cog-outline"},
    ApexEntityType.VIRTUAL: {ICON: "mdi:cog-outline"},
}

MEASUREMENTS = {
    "Celcius": "°C",
    "Faren": "°F"
}

UPDATE_INTERVAL = "update_interval"
UPDATE_INTERVAL_DEFAULT = 60
