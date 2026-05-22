from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, TOPIC_SET, TOPIC_STATE
from .coordinator import AFDDataCoordinator

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the pump switch."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AFDPumpSwitch(coordinator, entry)])

class AFDPumpSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of the pump switch."""

    def __init__(self, coordinator: AFDDataCoordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_unique_id = f"{coordinator.device_id}_pump"
        self._attr_name = "Pump"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.device_id)},
            "name": f"AFD Pump ({coordinator.prefix})",
            "manufacturer": "Custom",
            "model": "ESP8266 Pump Controller",
            "sw_version": "5.5.4",
        }
    
    @property
    def is_on(self) -> bool:
        return self.coordinator.data.get("pump", False)
    
    @property
    def available(self) -> bool:
        return self.coordinator.data.get("available", False)
    
    async def async_turn_on(self, **kwargs):
        await self.coordinator.async_publish(TOPIC_SET, "ON")
    
    async def async_turn_off(self, **kwargs):
        await self.coordinator.async_publish(TOPIC_SET, "OFF")
    
    @callback
    def _handle_coordinator_update(self):
        self.async_write_ha_state()