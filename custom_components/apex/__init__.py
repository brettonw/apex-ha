"""The Apex Controller integration."""
import asyncio
import logging
from datetime import timedelta

import async_timeout
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, NAME, DEVICEIP, MANUFACTURER, UPDATE_INTERVAL, UPDATE_INTERVAL_DEFAULT, DID, STATUS, CONFIG
from .apex import Apex

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["sensor", "switch"]

logger = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Apex component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Apex Device from a config entry."""
    user = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    deviceip = entry.data[DEVICEIP]
    if UPDATE_INTERVAL in entry.options:
        update_interval = entry.options[UPDATE_INTERVAL]
    else:
        update_interval = UPDATE_INTERVAL_DEFAULT
    logger.debug(update_interval)
    for ar in entry.data:
        logger.debug(ar)

    coordinator = ApexDataUpdateCoordinator(hass, user, password, deviceip, update_interval)

    await coordinator.async_refresh()  # Get initial data

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for component in PLATFORMS:
        await hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, component))

    async def async_set_options_service(service_call):
        await hass.async_add_executor_job(set_output, hass, service_call, coordinator)

    async def async_set_variable_service(service_call):
        await hass.async_add_executor_job(set_variable, hass, service_call, coordinator)

    async def async_set_dos_rate_service(service_call):
        await hass.async_add_executor_job(set_dos_rate, hass, service_call, coordinator)

    async def async_set_temperature(service_call):
        await hass.async_add_executor_job(set_temperature, hass, service_call, coordinator)

    async def async_refill_dos_reservoir(service_call):
        await hass.async_add_executor_job(refill_dos_reservoir, hass, service_call, coordinator)

    hass.services.async_register(DOMAIN, "set_output", async_set_options_service)
    hass.services.async_register(DOMAIN, "set_variable", async_set_variable_service)
    hass.services.async_register(DOMAIN, "set_dos_rate", async_set_dos_rate_service)
    hass.services.async_register(DOMAIN, "set_temperature", async_set_temperature)
    hass.services.async_register(DOMAIN, "refill_dos_reservoir", async_refill_dos_reservoir)

    return True


def set_output(hass, service, coordinator):
    did = service.data.get(DID).strip()
    setting = service.data.get("setting").strip()
    coordinator.apex.set_output_state(did, setting)


def set_variable(hass, service, coordinator):
    did = service.data.get(DID).strip()
    code = service.data.get("code")
    coordinator.apex.set_variable(did, code)


def set_dos_rate(hass, service, coordinator):
    did = service.data.get(DID).strip()
    profile_id = int(service.data.get("profile_id"))
    rate = float(service.data.get("rate"))
    coordinator.apex.set_dos_rate(did, profile_id, rate)


def set_temperature(hass, service, coordinator):
    did = service.data.get(DID).strip()
    temperature = float(service.data.get("temperature"))
    coordinator.apex.set_temperature(did, temperature)


def refill_dos_reservoir(hass, service, coordinator):
    module_number = int(service.data.get("module_number"))
    pump_number = int(service.data.get("pump_number"))
    coordinator.apex.refill_dos_reservoir(module_number, pump_number)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[hass.config_entries.async_forward_entry_unload(entry, component) for component in PLATFORMS]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class ApexDataUpdateCoordinator(DataUpdateCoordinator):
    """DataUpdateCoordinator to handle fetching new data about the Apex Controller."""

    def __init__(self, hass, user, password, deviceip, update_interval):
        """Initialize the coordinator and set up the Controller object."""
        self._hass = hass
        self.deviceip = deviceip
        self.apex = Apex(user, password, deviceip)
        self._available = True

        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        """Fetch data from Apex Controller."""
        try:
            async with async_timeout.timeout(30):
                data = {
                    STATUS: await self._hass.async_add_executor_job(self.apex.status),
                    CONFIG: await self._hass.async_add_executor_job(self.apex.config)
                }
                logger.debug("Refreshing Now")
                # logger.debug(data)
                return data
        except Exception as ex:
            self._available = False  # Mark as unavailable
            logger.warning(str(ex))
            logger.warning("Error communicating with Apex for %s", self.deviceip)
            raise UpdateFailed(
                f"Error communicating with Apex for {self.deviceip}"
            ) from ex


class ApexEntity(CoordinatorEntity):
    """Defines a base Apex entity."""

    def __init__(self, *, device_id: str, name: str, coordinator: ApexDataUpdateCoordinator):
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._name = name

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()

    @property
    def name(self):
        """Return the name of the entity."""
        logger.debug(self._name)
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the entity."""
        return f"{self.coordinator.deviceip}-{self._device_id}"

    @property
    def device_info(self):
        """Return device information about this device."""
        if self._device_id is None:
            return None

        return {
            "identifiers": {(DOMAIN, self.coordinator.deviceip)},
            NAME: f"Apex Controller ({self.coordinator.deviceip})",
            "hw_version": self.coordinator.data[STATUS]["system"]["hardware"],
            "sw_version": self.coordinator.data[STATUS]["system"]["software"],
            "manufacturer": MANUFACTURER
        }
