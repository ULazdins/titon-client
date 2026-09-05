import logging

from .helpers import get_symbol_hash, get_after_last_pipe, split_into_bits


_LOGGER = logging.getLogger(__name__)


class TitonFanSpeed:
    update_callbacks = []

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

        value = 0
        for x in range(0, 4):
            if bits1[x] != 0:
                value = x + 1
                break

        self.set_value(value)

        return value

    async def set_to(self, value):
        try:
            if value < 0 or value > 4:
                return False

            message = self.client.get_full_message(f"F{ '%d' % value }")
            response_prefix = (
                f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>F"
            )

            if not self.client.is_connected:
                await self.client.connect()

            response = await self.client.send_request_response(
                message,
                lambda x: x.startswith(response_prefix),
            )

            payload = get_after_last_pipe(response)
            payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

            success = payload == "F<ack>"

            if success:
                self.set_value(value)

            return success
        except Exception as e:
            _LOGGER.exception(f"Failed to set fan speed ${e}")

    def set_value(self, value):
        notify_observers = self.value != value
        self.value = value

        if notify_observers:
            for callback in self.update_callbacks:
                callback()
