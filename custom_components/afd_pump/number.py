from homeassistant.components.number import NumberEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, TOPIC_DISPENSE_VOLUME_SET, TOPIC_CALIBRATE_VOLUME_SET, TOPIC_BRIGHTNESS_SET

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    numbers = [
        AFDDispenseVolumeNumber(coordinator, entry),
        AFDCalibrateVolumeNumber(coordinator, entry),
        AFDBrightnessNumber(coordinator, entry),
    ]
    async_add_entities(numbers)

class AFDDispenseVolumeNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_unique_id = f"{coordinator.device_id}_dispense_volume_set"
        self._attr_name = "Set Dispense Volume"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 10000
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = "ml"
        self._attr_icon = "mdi:water-pump"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    @property
    def native_value(self):
        return self.coordinator.data.get("dispense_volume_ml", 0)
    
    async def async_set_native_value(self, value: float):
        await self.coordinator.async_publish(TOPIC_DISPENSE_VOLUME_SET, str(int(value)))

class AFDCalibrateVolumeNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_calibrate_volume"
        self._attr_name = "Calibration Target Volume"
        self._attr_native_min_value = 1
        self._attr_native_max_value = 10000
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = "ml"
        self._attr_icon = "mdi:test-tube"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    @property
    def native_value(self):
        return self.coordinator.data.get("target_volume", 0)
    
    async def async_set_native_value(self, value: float):
        await self.coordinator.async_publish(TOPIC_CALIBRATE_VOLUME_SET, str(int(value)))

class AFDBrightnessNumber(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_brightness_set"
        self._attr_name = "LED Brightness"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = "%"
        self._attr_icon = "mdi:led-on"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    @property
    def native_value(self):
        return self.coordinator.data.get("brightness_percent", 0)
    
    async def async_set_native_value(self, value: float):
        await self.coordinator.async_publish(TOPIC_BRIGHTNESS_SET, str(int(value)))