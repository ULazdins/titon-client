import asyncio
from helpers import get_symbol_hash, get_after_last_pipe, split_into_bits


class TitonClient:
    messages = []
    my_mac = "12-34-56-78-12-34"

    def __init__(self, hrv_mac):
        self.hrv_mac = hrv_mac

        self.message_handshake = f":DLF||{self.my_mac};"
        self.message_handshake_ack = f":DLF||{self.my_mac}|PS;"
        self.message_register_hrv = f":_CX|{hrv_mac}|0;"
        self.message_register_hrv_ack = (
            f":_CX|{hrv_mac}|0|PS;"  # FA - response if HRV not found
        )

    def get_full_message(self, msg):
        payload = f"{msg}{ '%03d' % get_symbol_hash(msg) }"
        return f":DAT|{self.hrv_mac}|{self.my_mac}|<stx>{payload}<etx>;"

    async def receive_messages(self, reader):
        is_ready = False

        while True:
            data = await reader.readuntil(b";")
            if not data:
                break

            string = data.decode()
            print(f"<<< {string}")

            if not is_ready:
                if string == self.message_handshake_ack:
                    self.messages.append(self.message_register_hrv)
                if string == self.message_register_hrv_ack:
                    is_ready = True
            else:
                self.handle_response(string)

    async def send_messages(self, writer):
        while True:
            try:
                message = self.messages.pop()
                message = message
                print(f">>> {message}")
                writer.write(message.encode())
                await writer.drain()
            except IndexError:
                await asyncio.sleep(0.1)  # Avoid blocking the event loop

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            "app.manageiaq.com", 6275
        )

        asyncio.get_event_loop().create_task(self.receive_messages(self.reader))
        asyncio.get_event_loop().create_task(self.send_messages(self.writer))

        self.messages.append(self.message_handshake)

    async def disconnect(self):
        self.writer.close()

    def send_raw_message(self, message):
        payload = self.get_full_message(message)
        self.messages.append(payload)

    def handle_response(self, msg):
        payload = get_after_last_pipe(msg)
        payload = payload.removeprefix("<stx>").removesuffix("<etx>;")

        if payload.startswith("L"):
            byte1 = payload[4:6]
            byte2 = payload[10:12]
            byte3 = payload[16:18]

            print(byte1, byte2, byte3)

            bits1 = split_into_bits(int(byte1, 16))
            bits2 = split_into_bits(int(byte2, 16))
            bits3 = split_into_bits(int(byte3, 16))

            # FunModel
            print("Byte1", bits1)
            print("Speed1", bits1[0])
            print("Speed2", bits1[1])
            print("Speed3", bits1[2])
            print("Speed4", bits1[3])
            print("Timer", bits1[4])
            print("Switch", bits1[5])

            print("\nByte2", bits2)
            print("Sensor", bits2[0])
            print("Filter", bits2[1])
            print("Inhibit", bits2[2])
            print("Boost", bits2[3])
            print("Frost", bits2[4])
            print("Internal", bits2[5])

            print("\nByte3", bits3)
            print("Summer", bits3[0])
            print("Attention", bits3[1])
            print("Duct heater", bits3[2])
