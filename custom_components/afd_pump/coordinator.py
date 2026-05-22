import json
import logging
from typing import Optional
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from homeassistant.components import mqtt
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, DEFAULT_PREFIX
from .const import (
    TOPIC_STATE, TOPIC_LEVEL, TOPIC_AVAILABILITY,
    TOPIC_CALIBRATE_STATE, TOPIC_BRIGHTNESS,
    TOPIC_DISPENSE_VOLUME, TOPIC_SCHEDULE
)

_LOGGER = logging.getLogger(__name__)

class AFDDataCoordinator(DataUpdateCoordinator):
    """Coordinator to manage AFD device state."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self.prefix = entry.data["topic_prefix"]
        self.device_id = f"afd_{self.prefix.lower()}"
        
        self._state = {}  # хранилище всех состояний
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"AFD Pump ({self.prefix})",
            update_interval=None,  # обновления через MQTT
        )
    
    async def async_config_entry_first_refresh(self):
        """Subscribe to MQTT topics and set up listeners."""
        await self._subscribe_topics()
        await super().async_config_entry_first_refresh()
    
    async def _subscribe_topics(self):
        """Subscribe to all relevant MQTT topics."""
        topics = {
            TOPIC_STATE: self._update_state,
            TOPIC_LEVEL: self._update_level,
            TOPIC_AVAILABILITY: self._update_availability,
            TOPIC_CALIBRATE_STATE: self._update_calibration,
            TOPIC_BRIGHTNESS: self._update_brightness,
            TOPIC_DISPENSE_VOLUME: self._update_dispense_volume,
            TOPIC_SCHEDULE: self._update_schedule,
        }
        for topic_suffix, handler in topics.items():
            full_topic = f"{self.prefix}/{topic_suffix}"
            await mqtt.async_subscribe(
                self.hass, full_topic, handler, 1, None, None
            )
    
    async def _update_state(self, msg):
        """Handle state updates."""
        payload = msg.payload
        self._state["pump"] = payload == "ON"
        self.async_set_updated_data(self._state)
    
    async def _update_level(self, msg):
        self._state["level_ok"] = msg.payload == "OK"
        self.async_set_updated_data(self._state)
    
    async def _update_availability(self, msg):
        self._state["available"] = msg.payload == "online"
        self.async_set_updated_data(self._state)
    
    async def _update_calibration(self, msg):
        try:
            data = json.loads(msg.payload)
            self._state["calibrating"] = data.get("calibrating", False)
            self._state["calibrated"] = data.get("calibrated", False)
            self._state["flow_rate"] = data.get("flowRate", 0.0)
            self._state["target_volume"] = data.get("targetVolume", 0)
            self._state["elapsed_sec"] = data.get("elapsedSec", 0)
            self._state["remaining_sec"] = data.get("remainingSec", 0)
            self._state["fixed_calibration"] = data.get("fixed", False)
        except Exception:
            _LOGGER.warning("Failed to parse calibration JSON: %s", msg.payload)
        self.async_set_updated_data(self._state)
    
    async def _update_brightness(self, msg):
        try:
            self._state["brightness_percent"] = int(msg.payload)
        except ValueError:
            pass
        self.async_set_updated_data(self._state)
    
    async def _update_dispense_volume(self, msg):
        try:
            self._state["dispense_volume_ml"] = float(msg.payload)
        except ValueError:
            pass
        self.async_set_updated_data(self._state)
    
    async def _update_schedule(self, msg):
        try:
            self._state["schedule"] = json.loads(msg.payload)
        except Exception:
            pass
        self.async_set_updated_data(self._state)
    
    async def async_publish(self, topic_suffix: str, payload: str, qos=1, retain=False):
        """Publish a command to the device."""
        full_topic = f"{self.prefix}/{topic_suffix}"
        await mqtt.async_publish(self.hass, full_topic, payload, qos, retain)
    
    async def async_shutdown(self):
        """Shutdown coordinator, unsubscribe topics if needed."""
        # MQTT subscriptions are automatically cleaned up on entry unload
        pass