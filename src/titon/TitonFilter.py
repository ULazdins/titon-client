import logging

from .helpers import get_symbol_hash, get_after_last_pipe


_LOGGER = logging.getLogger(__name__)


class TitonFilter:
    def __init__(self, client):
        self.client = client

        self.message = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|<stx>SF1{'%03d' % get_symbol_hash('SF1')}<etx>;"
        self.response_prefix = (
            f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>SF"
        )

    async def perform(self):
        """Query filter change status."""
        response = await self.client.send_request_response(
            self.message, lambda x: x.startswith(self.response_prefix)
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        # Return the raw payload and any numeric value present
        nums = [int(x) for x in __import__("re").findall(r"\d{1,4}", payload)]

        _LOGGER.debug("Filter payload: %s nums: %s", payload, nums)

        return {"raw": payload, "numbers": nums}

    async def set_changed(self):
        """Save filter-changed state (SF01)."""
        message = self.client.get_full_message("SF01")
        response_prefix = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>S"

        if not self.client.is_connected:
            await self.client.connect()

        response = await self.client.send_request_response(
            message, lambda x: x.startswith(response_prefix)
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        return payload.find("S<ack>") >= 0 or payload.startswith("S")
