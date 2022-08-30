import logging
import re

from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import SensorStateClass

from . import ApexEntity
from .const import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add the Entities from the config."""
    entry = hass.data[DOMAIN][config_entry.entry_id]

    for value in entry.data[INPUTS]:
        sensor = ApexSensor(entry, value, config_entry.options)
        async_add_entities([sensor], True)
    for value in entry.data[OUTPUTS]:
        if ApexEntityType.is_variable_type(value[TYPE]):
            sensor = ApexSensor(entry, value, config_entry.options)
            async_add_entities([sensor], True)


class ApexSensor(
    ApexEntity,
    Entity,
):
    def __init__(self, coordinator, sensor, options):

        self.sensor = sensor
        self.options = options
        self._attr = {}
        self.coordinator = coordinator
        self._device_id = f"apex_{sensor[DID]}"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_has_entity_name = True
        self._attr_name = f"apex_{sensor[DID]}-{sensor[NAME]}"

        # Required for HA 2022.7
        self.coordinator_context = object()

    # Need to tidy this section up and avoid using so many for loops
    def get_value(self, ftype):
        if ftype == "state":
            for value in self.coordinator.data[INPUTS]:
                if value[DID] == self.sensor[DID]:
                    return value["value"]
            for value in self.coordinator.data[OUTPUTS]:
                if value[DID] == self.sensor[DID]:
                    if self.sensor[TYPE] == ApexEntityType.DOS:
                        return value[STATUS][4]
                    if self.sensor[TYPE] == ApexEntityType.IOTA_PUMP:
                        return value[STATUS][1]
                    if (self.sensor[TYPE] == ApexEntityType.VIRTUAL) or (self.sensor[TYPE] == ApexEntityType.VARIABLE):
                        if CONFIG in self.coordinator.data:
                            for config in self.coordinator.data[CONFIG][OUTPUT_CONFIG]:
                                if config[DID] == self.sensor[DID]:
                                    if config[CTYPE] == ADVANCED:
                                        return ApexSensor.process_prog(config[PROG])
                                    else:
                                        return "Not an Advanced variable!"

        if ftype == "attributes":
            for value in self.coordinator.data[INPUTS]:
                if value[DID] == self.sensor[DID]:
                    return value
            for value in self.coordinator.data[OUTPUTS]:
                if value[DID] == self.sensor[DID]:
                    if self.sensor[TYPE] == ApexEntityType.DOS:
                        return value
                    if self.sensor[TYPE] == ApexEntityType.IOTA_PUMP:
                        return value
                    if self.sensor[TYPE] == ApexEntityType.VIRTUAL or self.sensor[TYPE] == ApexEntityType.VARIABLE:
                        if CONFIG in self.coordinator.data:
                            for config in self.coordinator.data[CONFIG][OUTPUT_CONFIG]:
                                if config[DID] == self.sensor[DID]:
                                    return config
                        else:
                            return value

    @staticmethod
    def process_prog(prog):
        if "Set PF" in prog:
            return prog
        test = re.findall("Set\s[^\d]*(\d+)", prog)
        if test:
            _LOGGER.debug(test[0])
            return int(test[0])
        else:
            return prog

    @property
    def state(self):
        return self.get_value("state")

    @property
    def extra_state_attributes(self):
        return self.get_value("attributes")

    @property
    def unit_of_measurement(self):
        if INPUT_CONFIG in self.coordinator.data[CONFIG]:
            for value in self.coordinator.data[CONFIG][INPUT_CONFIG]:
                if value[DID] == self.sensor[DID]:
                    if RANGE in value[EXTRA]:
                        if value[EXTRA][RANGE] in MEASUREMENTS:
                            return MEASUREMENTS[value[EXTRA][RANGE]]
        if self.sensor[TYPE] in SENSORS:
            if MEASUREMENT in SENSORS[self.sensor[TYPE]]:
                return SENSORS[self.sensor[TYPE]][MEASUREMENT]
        return None

    @property
    def icon(self):
        if self.sensor[TYPE] in SENSORS:
            return SENSORS[self.sensor[TYPE]][ICON]
        else:
            _LOGGER.debug("Missing icon: " + self.sensor[TYPE])
            return None
