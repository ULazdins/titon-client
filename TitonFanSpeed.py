import logging

from helpers import get_symbol_hash, get_after_last_pipe, split_into_bits


_LOGGER = logging.getLogger(__name__)


class TitonFanSpeed:
    def __init__(self, client):
        self.client = client
        self.value = None

        self.message = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|<stx>L{ '%03d' % get_symbol_hash('L') }<etx>;"
        self.response_prefix = (
            f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>L"
        )

    async def perform(self):
        response = await self.client.send_request_response(
            self.message,
            lambda x: x.startswith(self.response_prefix),
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        byte1 = payload[4:6]

        bits1 = split_into_bits(int(byte1, 16))

        self.value = 0
        for x in range(0, 4):
            if bits1[x] != 0:
                self.value = x + 1
                break

        return self.value

    async def set_to(self, value):
        if value < 0 or value > 4:
            return False

        message = self.client.get_full_message(f"F{ '%d' % value }")
        response_prefix = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>F"

        response = await self.client.send_request_response(
            message,
            lambda x: x.startswith(response_prefix),
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        return payload == "F<ack>"
