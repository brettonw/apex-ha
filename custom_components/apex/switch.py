import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity

from . import ApexEntity
from .const import *

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add the Switch from the config."""
    entry = hass.data[DOMAIN][config_entry.entry_id]

    for value in entry.data[OUTPUTS]:
        sw = Switch(entry, value, config_entry.options)
        async_add_entities([sw], False)


class ApexSwitchState:
    ON = "ON"
    OFF = "OFF"
    AUTO_ON = "AON"
    AUTO_OFF = "AOF"

    @staticmethod
    def is_on(state):
        return (state == ApexSwitchState.ON) or (state == ApexSwitchState.AUTO_ON)

    @staticmethod
    def is_off(state):
        return (state == ApexSwitchState.OFF) or (state == ApexSwitchState.AUTO_OFF)


class Switch(ApexEntity, SwitchEntity):
    def __init__(self, coordinator, switch, options):

        self._device_id = "apex_" + switch[DID]
        self._attr_has_entity_name = True
        self._attr_name = switch[DID] + switch["name"]
        self.switch = switch
        self.coordinator = coordinator
        self._state = None
        # Required for HA 2022.7
        self.coordinator_context = object()

    async def async_turn_on(self, **kwargs):
        update = await self.coordinator.hass.async_add_executor_job(
            self.coordinator.apex.toggle_output,
            self.switch[DID],
            ApexSwitchState.ON
        )
        if ApexSwitchState.is_on(update[STATUS][0]):
            self._state = True
            self.switch[STATUS] = update[STATUS]
            _LOGGER.debug("Writing state ON")
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        update = await self.coordinator.hass.async_add_executor_job(
            self.coordinator.apex.toggle_output,
            self.switch[DID],
            ApexSwitchState.OFF
        )
        if ApexSwitchState.is_off(update[STATUS][0]):
            self._state = False
            self.switch[STATUS] = update[STATUS]
            _LOGGER.debug("Writing state OFF")
            self.async_write_ha_state()

    @property
    def is_on(self):
        if self._state is True:
            self._state = None
            return True
        elif self._state is False:
            self._state = None
            return False
        for value in self.coordinator.data[OUTPUTS]:
            if value[DID] == self.switch[DID]:
                return ApexSwitchState.is_on(value[STATUS][0])

    @property
    def icon(self):
        if self.switch[TYPE] in SWITCHES:
            return SWITCHES[self.switch[TYPE]][ICON]
        else:
            _LOGGER.debug("Missing icon: " + self.switch[TYPE])
            return None

    @property
    def extra_state_attributes(self):
        return self.switch

    def turn_on(self, **kwargs: Any) -> None:
        pass

    def turn_off(self, **kwargs: Any) -> None:
        pass

