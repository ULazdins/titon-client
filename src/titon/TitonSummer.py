import logging

from .helpers import get_symbol_hash, get_after_last_pipe


_LOGGER = logging.getLogger(__name__)


class TitonSummer:
    def __init__(self, client):
        self.client = client

        self.message = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|<stx>SB10{'%03d' % get_symbol_hash('SB10')}<etx>;"
        self.response_prefix = (
            f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>SB"
        )

    async def read_boost_status(self) -> bool:
        """Return True if summer boost is enabled, False if disabled, None if unknown."""
        response = await self.client.send_request_response(
            self.message, lambda x: x.startswith(self.response_prefix)
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        # App checks for SB1 vs SB0
        if "SB1" in payload:
            return True
        if "SB0" in payload:
            return False

        _LOGGER.debug("Unknown SB payload: %s", payload)
        return None
