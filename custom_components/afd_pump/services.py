import json
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import entity_platform
from .const import DOMAIN, TOPIC_DISPENSE_VOLUME_SET, TOPIC_CALIBRATE_VOLUME_SET, TOPIC_BRIGHTNESS_SET
from .const import TOPIC_CALIBRATE_START, TOPIC_CALIBRATE_STOP, TOPIC_DISPENSE_RUN, TOPIC_DISPENSE_STOP
from .const import TOPIC_SCHEDULE_ADD, TOPIC_SCHEDULE_REMOVE, TOPIC_SCHEDULE_UPDATE, TOPIC_SCHEDULE_GET

async def async_setup_services(hass: HomeAssistant, coordinator):
    """Register custom services for AFD Pump."""
    
    platform = entity_platform.current_platform.get()
    
    async def async_service_calibrate_start(call: ServiceCall):
        entity_id = call.data.get("entity_id")
        # Просто отправляем команду старта, объём уже установлен через number
        await coordinator.async_publish(TOPIC_CALIBRATE_START, "")
    
    async def async_service_calibrate_stop(call: ServiceCall):
        await coordinator.async_publish(TOPIC_CALIBRATE_STOP, "")
    
    async def async_service_calibrate_set_volume(call: ServiceCall):
        volume = int(call.data["volume"])
        await coordinator.async_publish(TOPIC_CALIBRATE_VOLUME_SET, str(volume))
    
    async def async_service_dispense_run(call: ServiceCall):
        await coordinator.async_publish(TOPIC_DISPENSE_RUN, "")
    
    async def async_service_dispense_stop(call: ServiceCall):
        await coordinator.async_publish(TOPIC_DISPENSE_STOP, "")
    
    async def async_service_dispense_set_volume(call: ServiceCall):
        volume = int(call.data["volume"])
        await coordinator.async_publish(TOPIC_DISPENSE_VOLUME_SET, str(volume))
    
    async def async_service_set_brightness(call: ServiceCall):
        percent = int(call.data["brightness_percent"])
        await coordinator.async_publish(TOPIC_BRIGHTNESS_SET, str(percent))
    
    async def async_service_schedule_add(call: ServiceCall):
        job = {
            "hour": call.data["hour"],
            "minute": call.data["minute"],
            "daysMask": call.data["days_mask"],
            "volume": call.data["volume"],
            "enabled": call.data.get("enabled", True)
        }
        await coordinator.async_publish(TOPIC_SCHEDULE_ADD, json.dumps(job))
    
    async def async_service_schedule_remove(call: ServiceCall):
        job = {"id": call.data["job_id"]}
        await coordinator.async_publish(TOPIC_SCHEDULE_REMOVE, json.dumps(job))
    
    async def async_service_schedule_update(call: ServiceCall):
        job = {"id": call.data["job_id"]}
        if "hour" in call.data: job["hour"] = call.data["hour"]
        if "minute" in call.data: job["minute"] = call.data["minute"]
        if "days_mask" in call.data: job["daysMask"] = call.data["days_mask"]
        if "volume" in call.data: job["volume"] = call.data["volume"]
        if "enabled" in call.data: job["enabled"] = call.data["enabled"]
        await coordinator.async_publish(TOPIC_SCHEDULE_UPDATE, json.dumps(job))
    
    async def async_service_schedule_get(call: ServiceCall):
        await coordinator.async_publish(TOPIC_SCHEDULE_GET, "")
    
    # Register services on the platform
    platform.async_register_entity_service(
        "calibrate_start", {}, async_service_calibrate_start
    )
    platform.async_register_entity_service(
        "calibrate_stop", {}, async_service_calibrate_stop
    )
    platform.async_register_entity_service(
        "calibrate_set_volume",
        {vol.Required("volume"): vol.Coerce(int)},
        async_service_calibrate_set_volume
    )
    platform.async_register_entity_service(
        "dispense_run", {}, async_service_dispense_run
    )
    platform.async_register_entity_service(
        "dispense_stop", {}, async_service_dispense_stop
    )
    platform.async_register_entity_service(
        "dispense_set_volume",
        {vol.Required("volume"): vol.Coerce(int)},
        async_service_dispense_set_volume
    )
    platform.async_register_entity_service(
        "set_brightness",
        {vol.Required("brightness_percent"): vol.Coerce(int)},
        async_service_set_brightness
    )
    platform.async_register_entity_service(
        "schedule_add",
        {
            vol.Required("hour"): vol.Coerce(int),
            vol.Required("minute"): vol.Coerce(int),
            vol.Required("days_mask"): vol.Coerce(int),
            vol.Required("volume"): vol.Coerce(int),
            vol.Optional("enabled", default=True): bool,
        },
        async_service_schedule_add
    )
    platform.async_register_entity_service(
        "schedule_remove",
        {vol.Required("job_id"): vol.Coerce(int)},
        async_service_schedule_remove
    )
    platform.async_register_entity_service(
        "schedule_update",
        {
            vol.Required("job_id"): vol.Coerce(int),
            vol.Optional("hour"): vol.Coerce(int),
            vol.Optional("minute"): vol.Coerce(int),
            vol.Optional("days_mask"): vol.Coerce(int),
            vol.Optional("volume"): vol.Coerce(int),
            vol.Optional("enabled"): bool,
        },
        async_service_schedule_update
    )
    platform.async_register_entity_service(
        "schedule_get", {}, async_service_schedule_get
    )