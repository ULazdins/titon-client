from .helpers import get_symbol_hash, get_after_last_pipe


class TitonKitchenTimer:
    update_callbacks = []
    value = None

    def __init__(self, client):
        self.client = client

    async def perform(self):
        message = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|<stx>SK10{ '%03d' % get_symbol_hash('SK10') }<etx>;"
        response_prefix = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>SK"

        response = await self.client.send_request_response(
            message,
            lambda x: x.startswith(response_prefix),
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        byte1 = payload[2:5]

        self.set_value(int(byte1, 10))

        return self.value

    async def set_to(self, value):
        if value < 0 or value > 100:
            pass

        message = self.client.get_full_message(f"SK0{ '%03d' % value }")
        response_prefix = f":DAT|{self.client.hrv_mac}|{self.client.my_mac}|PS|<stx>S"

        response = await self.client.send_request_response(
            message,
            lambda x: x.startswith(response_prefix),
        )

        payload = get_after_last_pipe(response)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        success = payload == "S<ack>"

        if success:
            self.set_value(value)

        return success

    def set_value(self, value):
        notify_observers = self.value != value
        self.value = value

        if notify_observers:
            for callback in self.update_callbacks:
                callback()
