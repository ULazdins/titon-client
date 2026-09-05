import logging
import re

from .helpers import get_symbol_hash, get_after_last_pipe


_LOGGER = logging.getLogger(__name__)


class TitonHumidity:
    def __init__(self, client):
        self.client = client

        self.message = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|<stx>SH1000{'%03d' % get_symbol_hash('SH1000')}<etx>;"
        self.response_prefix = (
            f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>SH"
        )

    async def perform(self):
        """Read current humidity threshold/setting. Returns percentage (int)."""
        response = await self.client.send_request_response(
            self.message, lambda x: x.startswith(self.response_prefix)
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        # Find first 3-digit number in payload and subtract 30 (app logic)
        m = re.search(r"(\d{3})", payload)
        if not m:
            _LOGGER.debug("No humidity value found in payload: %s", payload)
            return None

        raw = int(m.group(1))
        value = raw - 30

        _LOGGER.debug("Humidity payload=%s -> %s%%", raw, value)

        return value

    async def set_to(self, percent: int):
        """Set humidity threshold. percent is 0-100."""
        if percent < 0 or percent > 100:
            raise ValueError("percent must be 0-100")

        inner = percent + 30

        # Try simple form first (device app composes additional checksum, but server accepts SH0nnn)
        message = self.client.get_full_message(f"SH0{inner:03d}")
        response_prefix = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>S"

        if not self.client.is_connected:
            await self.client.connect()

        try:
            response = await self.client.send_request_response(
                message, lambda x: x.startswith(response_prefix)
            )
            payload = (
                get_after_last_pipe(response)
                .removeprefix("<stx>")
                .removesuffix("<etx>;")
            )
            return payload.find("S<ack>") >= 0 or payload.startswith("S")
        except Exception:
            _LOGGER.debug("Setting humidity via simplified message failed, giving up")
            return False
