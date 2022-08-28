import logging

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


class Switch(ApexEntity, SwitchEntity):
    def __init__(self, coordinator, switch, options):

        self._device_id = "apex_" + switch[DID]
        self.switch = switch
        self.coordinator = coordinator
        self._state = None
        # Required for HA 2022.7
        self.coordinator_context = object()

    async def async_turn_on(self, **kwargs):
        update = await self.coordinator.hass.async_add_executor_job(
            self.coordinator.apex.toggle_output,
            self.switch[DID],
            ON
        )
        if (update[STATUS][0] == ON) or (update[STATUS][0] == AUTO_ON):
            self._state = True
            self.switch[STATUS] = update[STATUS]
            _LOGGER.debug("Writing state ON")
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        update = await self.coordinator.hass.async_add_executor_job(
            self.coordinator.apex.toggle_output,
            self.switch[DID],
            OFF
        )
        if (update[STATUS][0] == OFF) or (update[STATUS][0] == AUTO_OFF):
            self._state = False
            self.switch[STATUS] = update[STATUS]
            _LOGGER.debug("Writing state OFF")
            self.async_write_ha_state()

    @property
    def name(self):
        return "apex_" + self.switch["name"]

    @property
    def device_id(self):
        return self.device_id

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
                if value[STATUS][0] == ON or value[STATUS][0] == AUTO_ON:
                    return True
                else:
                    return False

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
