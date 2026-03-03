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

        # parsed flags
        self.filter_flag = None
        self.frost_flag = None
        self.summer_flag = None

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

        # FunModel bits (Byte1)
        _LOGGER.debug("Byte1 %s", bits1)
        _LOGGER.debug("Speed1 %s", bits1[0])
        _LOGGER.debug("Speed2 %s", bits1[1])
        _LOGGER.debug("Speed3 %s", bits1[2])
        _LOGGER.debug("Speed4 %s", bits1[3])
        _LOGGER.debug("Timer %s", bits1[4])
        _LOGGER.debug("Switch %s", bits1[5])

        # Byte2 contains status flags such as Filter, Frost, Boost
        _LOGGER.debug("\nByte2 %s", bits2)
        _LOGGER.debug("Sensor %s", bits2[0])
        _LOGGER.debug("Filter %s", bits2[1])
        _LOGGER.debug("Inhibit %s", bits2[2])
        _LOGGER.debug("Boost %s", bits2[3])
        _LOGGER.debug("Frost %s", bits2[4])
        _LOGGER.debug("Internal %s", bits2[5])

        # store parsed flags for external use
        self.filter_flag = bool(bits2[1])
        self.frost_flag = bool(bits2[4])

        # Byte3 contains summer and other flags
        _LOGGER.debug("\nByte3 %s", bits3)
        _LOGGER.debug("Summer %s", bits3[0])
        _LOGGER.debug("Attention %s", bits3[1])
        _LOGGER.debug("Duct heater %s", bits3[2])

        self.summer_flag = bool(bits3[0])

        return {
            "filter": self.filter_flag,
            "frost": self.frost_flag,
            "summer": self.summer_flag,
        }
