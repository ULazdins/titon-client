class TitonHandshake:
    def __init__(self, client):
        self.client = client

        self.message_handshake = f":DLF||{client.my_mac};"
        self.message_handshake_ack = f":DLF||{client.my_mac}|PS;"
        self.message_register_hrv = f":_CX|{client.hrv_mac}|0;"
        self.message_register_hrv_ack = (
            f":_CX|{client.hrv_mac}|0|PS;"  # FA - response if HRV not found
        )

    async def perform(self):
        await self.client.send_request_response(
            self.message_handshake,
            lambda x: x == self.message_handshake_ack,
        )

        await self.client.send_request_response(
            self.message_register_hrv,
            lambda x: x == self.message_register_hrv_ack,
        )
