from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AFDLevelSensor(coordinator, entry)])

class AFDLevelSensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for water level (LOW = problem)."""

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_unique_id = f"{coordinator.device_id}_level"
        self._attr_name = "Water Level"
        self._attr_device_class = "problem"
        self._attr_icon = "mdi:water"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
        }
    
    @property
    def is_on(self) -> bool:
        # returns True when level is LOW (problem)
        return not self.coordinator.data.get("level_ok", True)
    
    @property
    def available(self) -> bool:
        return self.coordinator.data.get("available", False)