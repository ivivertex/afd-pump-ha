from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    sensors = [
        AFDFlowRateSensor(coordinator, entry),
        AFDCalibrationStateSensor(coordinator, entry),
        AFDDispenseVolumeSensor(coordinator, entry),
        AFDBrightnessSensor(coordinator, entry),
    ]
    async_add_entities(sensors)

class AFDFlowRateSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_unique_id = f"{coordinator.device_id}_flow_rate"
        self._attr_name = "Flow Rate"
        self._attr_native_unit_of_measurement = "ml/s"
        self._attr_icon = "mdi:gauge"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    @property
    def native_value(self):
        return self.coordinator.data.get("flow_rate", 0.0)
    
    @property
    def available(self):
        return self.coordinator.data.get("available", False)

class AFDCalibrationStateSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self._attr_unique_id = f"{coordinator.device_id}_calibration_state"
        self._attr_name = "Calibration State"
        self._attr_icon = "mdi:test-tube"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    @property
    def native_value(self):
        if self.coordinator.data.get("calibrating"):
            return "Calibrating"
        if self.coordinator.data.get("calibrated"):
            return "Calibrated"
        return "Not calibrated"
    
    @property
    def extra_state_attributes(self):
        return {
            "target_volume_ml": self.coordinator.data.get("target_volume"),
            "elapsed_seconds": self.coordinator.data.get("elapsed_sec"),
            "remaining_seconds": self.coordinator.data.get("remaining_sec"),
            "fixed_calibration": self.coordinator.data.get("fixed_calibration"),
        }

class AFDDispenseVolumeSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_dispense_volume"
        self._attr_name = "Dispense Volume"
        self._attr_native_unit_of_measurement = "ml"
        self._attr_icon = "mdi:water-pump"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    @property
    def native_value(self):
        return self.coordinator.data.get("dispense_volume_ml", 0)

class AFDBrightnessSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_id}_brightness"
        self._attr_name = "LED Brightness"
        self._attr_native_unit_of_measurement = "%"
        self._attr_icon = "mdi:led-on"
        self._attr_device_info = {"identifiers": {(DOMAIN, coordinator.device_id)}}
    
    @property
    def native_value(self):
        return self.coordinator.data.get("brightness_percent", 0)