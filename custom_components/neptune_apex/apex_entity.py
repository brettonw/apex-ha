import logging
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, MANUFACTURER, DID, STATUS, TYPE, SYSTEM
from .apex_data_update_coordinator import ApexDataUpdateCoordinator

logger = logging.getLogger(__name__)


class ApexEntity(CoordinatorEntity):
    def __init__(self, entity_type: str, entity: dict, coordinator: ApexDataUpdateCoordinator):
        super().__init__(coordinator)

        # we do not pass a name up the tree
        self._device_id = self._attr_unique_id = f"{coordinator.name}_{entity[NAME]}"
        logger.debug(f"{entity_type}.{self._device_id} = (NAME: {entity[NAME]}, DID: {entity[DID]}, TYPE: {entity[TYPE]})")

        # just a HASS requirement
        self.coordinator_context = object()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()

    @property
    def name(self):
        return self._device_id

    @property
    def unique_id(self):
        return self._device_id

    @property
    def device_id(self):
        return self._device_id

    @property
    def device_info(self):
        """Return device information about this device."""
        if self._device_id is None:
            return None

        return {
            "identifiers": {(DOMAIN, self.coordinator.deviceip)},
            NAME: f"Apex Controller ({self.coordinator.name})",
            "hw_version": self.coordinator.data[STATUS][SYSTEM]["hardware"],
            "sw_version": self.coordinator.data[STATUS][SYSTEM]["software"],
            "manufacturer": MANUFACTURER
        }