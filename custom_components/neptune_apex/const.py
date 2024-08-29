from enum import StrEnum
from homeassistant.const import (ATTR_UNIT_OF_MEASUREMENT, UnitOfTemperature, UnitOfLength,
                                 UnitOfElectricPotential, UnitOfElectricCurrent, UnitOfPower, UnitOfVolume,
                                 CONCENTRATION_PARTS_PER_MILLION, PERCENTAGE, DEVICE_CLASS_UNITS)

from homeassistant.components.sensor import SensorDeviceClass


class SensorDeviceClassExtra(SensorDeviceClass):
    CONCENTRATION = "concentration"
    TOTAL_ALKALINITY = "total_alkalinity"
    SALINITY = "salinity"
    CALCIUM = "calcium"
    MAGNESIUM = "magnesium"


class UnitOfConcentration(StrEnum):
    PARTS_PER_THOUSAND = "ppt"
    PARTS_PER_MILLION = "ppm"
    PARTS_PER_BILLION = "ppb"


# 1 meq/L = 50 mg/L = 2.8 dKH
# 1 dKH = 17.9 mg/L = 17.9 ppm
class UnitOfTotalAlkalinity(StrEnum):
    DEGREES_OF_CARBONATE_HARDNESS = "dKH"
    MILLIGRAMS_PER_LITER = "mg/L"
    MILLIEQUIVALENTS_PER_LITER = "meq/L"
    PARTS_PER_MILLION = "ppm"


DEVICE_CLASS_UNITS_EXTRA: dict[SensorDeviceClass, set[type[StrEnum] | str | None]] = {
    SensorDeviceClassExtra.CONCENTRATION: set(UnitOfConcentration),
    SensorDeviceClassExtra.TOTAL_ALKALINITY: set(UnitOfTotalAlkalinity),
    SensorDeviceClassExtra.SALINITY: set(UnitOfConcentration),
    SensorDeviceClassExtra.CALCIUM: set(UnitOfConcentration),
    SensorDeviceClassExtra.MAGNESIUM: set(UnitOfConcentration)
}
DEVICE_CLASS_UNITS_EXTRA.update(DEVICE_CLASS_UNITS)

DOMAIN = "neptune_apex"
MANUFACTURER = "Neptune Apex"

# common constants
ICON = "icon"
SENSOR_DEVICE_CLASS = "sensor_device_class"
DEVICEIP = "deviceip"
NAME = "name"
STATUS = "status"
DID = "did"
HEATER_DID = "heater_did"
CHILLER_DID = "chiller_did"
TYPE = "type"
CONFIG = "config"
INPUTS = "inputs"
OUTPUTS = "outputs"
PCONF = "pconf"
OCONF = "oconf"
ICONF = "iconf"
MCONF = "mconf"
STATE = "state"
ATTRIBUTES = "attributes"
SYSTEM = "system"
HOSTNAME = "hostname"

# types
DOS = "dos"
DQD = "dqd"
IOTA = "iotaPump|Sicce|Syncra"
VARIABLE = "variable"
VIRTUAL = "virtual"
OUTLET = "outlet"

# trident is a selector in config
SELECTOR = "selector"

# Hardware types, in status, are capitalized - these are types that have values in the "extra"
# field we might want to capture as a sensor
# XXX NOTE - I'm not sure about this, this info came from another person's data in a feature request
# XXX NOTE - and it doesn't seem to match the status from my device
HWTYPE = "hwtype"


class HwTypes(StrEnum):
    HWTYPE_TRI = "TRI"
    HWTYPE_TNP = "TNP"
    HWTYPE_DOS = "DOS"
    HWTYPE_DQD = "DQD"

# other types
# "MXMLight|Ecotech|30G6L"
# "MXMLight|Ecotech|30G5"
# "MXMLight|Ecotech|30G5L"
# "MXMPump|Ecotech|Vortech"
# "MXMPump|Ecotech|Vectra"
# "alert"
# "24v"


# control types
CTYPE = "ctype"
ADVANCED = "Advanced"
HEATER = "Heater"
CHILLER = "Chiller"
PROG = "prog"

SWITCHES = {
    OUTLET: {ICON: "mdi:power-socket-au"},
    "alert": {ICON: "mdi:alert"},
    VARIABLE: {ICON: "mdi:cog"},
    "afs": {ICON: "mdi:shaker"},
    "24v": {ICON: "mdi:home-lightning-bolt-outline"},
    DOS: {ICON: "mdi:test-tube"},
    DQD: {ICON: "mdi:test-tube"},
    VIRTUAL: {ICON: "mdi:monitor-account"},
    IOTA: {ICON: "mdi:pump"}
}

SENSORS = {
    "Temp": {ICON: "mdi:water-thermometer", SENSOR_DEVICE_CLASS: SensorDeviceClass.TEMPERATURE, ATTR_UNIT_OF_MEASUREMENT: UnitOfTemperature.CELSIUS},
    "Cond": {ICON: "mdi:shaker-outline", SENSOR_DEVICE_CLASS: SensorDeviceClassExtra.SALINITY, ATTR_UNIT_OF_MEASUREMENT: UnitOfConcentration.PARTS_PER_THOUSAND},
    "in": {ICON: "mdi:ruler", SENSOR_DEVICE_CLASS: SensorDeviceClass.DISTANCE, ATTR_UNIT_OF_MEASUREMENT: UnitOfLength.INCHES},
    "pH": {ICON: "mdi:test-tube", SENSOR_DEVICE_CLASS: SensorDeviceClass.PH},
    "ORP": {ICON: "mdi:test-tube", SENSOR_DEVICE_CLASS: SensorDeviceClass.VOLTAGE, ATTR_UNIT_OF_MEASUREMENT: UnitOfElectricPotential.MILLIVOLT},
    "digital": {ICON: "mdi:digital-ocean"},
    "Amps": {ICON: "mdi:lightning-bolt-circle", SENSOR_DEVICE_CLASS: SensorDeviceClass.CURRENT, ATTR_UNIT_OF_MEASUREMENT: UnitOfElectricCurrent.AMPERE},
    "pwr": {ICON: "mdi:power-plug", SENSOR_DEVICE_CLASS: SensorDeviceClass.POWER, ATTR_UNIT_OF_MEASUREMENT: UnitOfPower.WATT},
    "volts": {ICON: "mdi:flash-triangle", SENSOR_DEVICE_CLASS: SensorDeviceClass.VOLTAGE, ATTR_UNIT_OF_MEASUREMENT: UnitOfElectricPotential.VOLT},
    # trident
    "alk": {ICON: "mdi:test-tube", SENSOR_DEVICE_CLASS: SensorDeviceClassExtra.TOTAL_ALKALINITY, ATTR_UNIT_OF_MEASUREMENT: UnitOfTotalAlkalinity.DEGREES_OF_CARBONATE_HARDNESS},
    "ca": {ICON: "mdi:test-tube", SENSOR_DEVICE_CLASS: SensorDeviceClassExtra.CALCIUM, ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_PARTS_PER_MILLION},
    "mg": {ICON: "mdi:test-tube", SENSOR_DEVICE_CLASS: SensorDeviceClassExtra.MAGNESIUM, ATTR_UNIT_OF_MEASUREMENT: CONCENTRATION_PARTS_PER_MILLION},
    # DOS and DOS Quiet Drive pumps
    DOS: {ICON: "mdi:pump", SENSOR_DEVICE_CLASS: SensorDeviceClass.VOLUME, ATTR_UNIT_OF_MEASUREMENT: UnitOfVolume.MILLILITERS},
    DQD: {ICON: "mdi:pump", SENSOR_DEVICE_CLASS: SensorDeviceClass.VOLUME, ATTR_UNIT_OF_MEASUREMENT: UnitOfVolume.MILLILITERS},
    # an Iota integration
    IOTA: {ICON: "mdi:pump", SENSOR_DEVICE_CLASS: PERCENTAGE, ATTR_UNIT_OF_MEASUREMENT: PERCENTAGE},
    VARIABLE: {ICON: "mdi:cog-outline"},
    VIRTUAL: {ICON: "mdi:cog-outline"},
}

MEASUREMENTS = {
    # is this due to a typo in the Apex system?
    "Celcius": UnitOfTemperature.CELSIUS,
    # in case they ever fix it
    "Celsius": UnitOfTemperature.CELSIUS,
    "Faren": UnitOfTemperature.FAHRENHEIT
}

UPDATE_INTERVAL = "update_interval"
UPDATE_INTERVAL_DEFAULT = 60
