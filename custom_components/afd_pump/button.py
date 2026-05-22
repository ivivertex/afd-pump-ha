from homeassistant.components.button import ButtonEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, TOPIC_CALIBRATE_START, TOPIC_CALIBRATE_STOP, TOPIC_DISPENSE_RUN, TOPIC_DISPENSE_STOP

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    buttons = [
        AFDCalibrateStartButton(coordinator, entry),
        AFDCalibrateStopButton(coordinator, entry),
        AFDDispenseRunButton(coordinator, entry),
        AFDDispenseStopButton(coordinator, entry),
    ]
    async_add_entities(buttons)

class AFDCalibrateStartButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_calibrate_start"
        self._attr_name = "Start Calibration"
        self._attr_icon = "mdi:play-circle"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    async def async_press(self):
        await self.coordinator.async_publish(TOPIC_CALIBRATE_START, "")

class AFDCalibrateStopButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_calibrate_stop"
        self._attr_name = "Stop Calibration"
        self._attr_icon = "mdi:stop-circle"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    async def async_press(self):
        await self.coordinator.async_publish(TOPIC_CALIBRATE_STOP, "")

class AFDDispenseRunButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_dispense_run"
        self._attr_name = "Run Dispense"
        self._attr_icon = "mdi:play"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    async def async_press(self):
        await self.coordinator.async_publish(TOPIC_DISPENSE_RUN, "")

class AFDDispenseStopButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_dispense_stop"
        self._attr_name = "Stop Dispense"
        self._attr_icon = "mdi:stop"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    async def async_press(self):
        await self.coordinator.async_publish(TOPIC_DISPENSE_STOP, "")