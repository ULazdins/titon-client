import logging

from .helpers import get_symbol_hash, get_after_last_pipe, split_into_bits


_LOGGER = logging.getLogger(__name__)


class TitonGeneralInfo:
    def __init__(self, client):
        self.client = client

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
        byte2 = payload[10:12]
        byte3 = payload[16:18]

        bits1 = split_into_bits(int(byte1, 16))
        bits2 = split_into_bits(int(byte2, 16))
        bits3 = split_into_bits(int(byte3, 16))

        # FunModel
        _LOGGER.debug(f"Byte1 {bits1}")
        _LOGGER.debug(f"Speed1 {bits1[0]}")
        _LOGGER.debug(f"Speed2 {bits1[1]}")
        _LOGGER.debug(f"Speed3 {bits1[2]}")
        _LOGGER.debug(f"Speed4 {bits1[3]}")
        _LOGGER.debug(f"Timer {bits1[4]}")
        _LOGGER.debug(f"Switch {bits1[5]}")

        _LOGGER.debug(f"\nByte2 {bits2}")
        _LOGGER.debug(f"Sensor {bits2[0]}")
        _LOGGER.debug(f"Filter {bits2[1]}")
        _LOGGER.debug(f"Inhibit {bits2[2]}")
        _LOGGER.debug(f"Boost {bits2[3]}")
        _LOGGER.debug(f"Frost {bits2[4]}")
        _LOGGER.debug(f"Internal {bits2[5]}")

        _LOGGER.debug(f"\nByte3 {bits3}")
        _LOGGER.debug(f"Summer {bits3[0]}")
        _LOGGER.debug(f"Attention {bits3[1]}")
        _LOGGER.debug(f"Duct heater {bits3[2]}")
