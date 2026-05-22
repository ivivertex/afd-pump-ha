import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN, DEFAULT_PREFIX, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

class AFDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AFD Pump Controller."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            prefix = user_input["topic_prefix"].strip().upper()
            # Validate prefix (simple check)
            if not prefix:
                errors["topic_prefix"] = "invalid_prefix"
            else:
                await self.async_set_unique_id(prefix)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"{DEFAULT_NAME} ({prefix})",
                    data={"topic_prefix": prefix}
                )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("topic_prefix", default=DEFAULT_PREFIX): str,
            }),
            errors=errors,
        )