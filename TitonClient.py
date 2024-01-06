import asyncio
import logging

from .helpers import get_symbol_hash
from .TitonHandshake import TitonHandshake

_LOGGER = logging.getLogger(__name__)


class TitonClient:
    messages = []
    callbacks = []
    my_mac = "12-34-56-78-12-34"
    is_connected = False
    is_connecting = False
    connecting_callbacks = []

    def __init__(self, hrv_mac):
        self.hrv_mac = hrv_mac

    async def connect(self):
        _LOGGER.debug("-- connecting")

        if self.is_connecting:
            future = asyncio.Future()
            self.connecting_callbacks.append(future)
            return future

        self.is_connecting = True
        self.reader, self.writer = await asyncio.open_connection(
            "app.manageiaq.com", 6275
        )

        reader_task = asyncio.ensure_future(self.receive_messages_loop(self.reader))
        asyncio.ensure_future(self.send_messages_loop(self.writer))
        reader_task.add_done_callback(self.handle_future_exception)

        handhske = TitonHandshake(self)
        await handhske.perform()
        _LOGGER.debug("-- connected\n")
        self.is_connecting = False
        self.is_connected = True

        for x in self.connecting_callbacks:
            x.set_result(True)

    def handle_future_exception(self, future):
        exception = future.exception()
        if exception:
            _LOGGER.debug(f"An exception occurred: {exception}")

            self.disconnect()

    def disconnect(self):
        self.writer.close()

        self.is_connected = False
        _LOGGER.debug("-- disconnected")

    async def receive_messages_loop(self, reader):
        while True:
            data = await reader.readuntil(b";")
            if not data:
                break

            string = data.decode()
            _LOGGER.debug(f"<<< {string}")

            for callback in self.callbacks:
                callback(string)

    async def send_messages_loop(self, writer):
        while True:
            try:
                message = self.messages.pop()
                message = message
                _LOGGER.debug(f">>> {message}")
                writer.write(message.encode())
                await writer.drain()
            except IndexError:
                await asyncio.sleep(0.1)  # Avoid blocking the event loop

    def get_full_message(self, msg):
        payload = f"{msg}{ '%03d' % get_symbol_hash(msg) }"
        return f":DAT|{self.hrv_mac}|{self.my_mac}|<stx>{payload}<etx>;"

    async def send_request_response(self, request, check_if_wants_to_handle_response):
        future = asyncio.Future()

        # Send message
        self.messages.append(request)

        # Await response
        def callback(message):
            if check_if_wants_to_handle_response(message):
                future.set_result(message)
                self.callbacks.remove(callback)

        self.callbacks.append(callback)

        # Timeout handling
        async def schedule_timeout_job():
            await asyncio.sleep(5)

            if not future.done():
                _LOGGER.debug("- handling timeout")
                self.callbacks.remove(callback)

                future.set_exception(ValueError("Timeout"))

        loop = asyncio.get_event_loop()
        loop.create_task(schedule_timeout_job())

        # Return future
        return await future

    async def send_dat_message(self, message):
        payload = self.get_full_message(message)
        self.messages.append(payload)
