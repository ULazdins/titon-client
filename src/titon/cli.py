"""Interactive console for poking at a Titon HRV unit.

Run with the unit's MAC address:

    python -m titon.cli AA-BB-CC-11-22-33

or set TITON_HRV_MAC in the environment.
"""

import asyncio
import logging
import os
import sys

import aioconsole

from .TitonClient import TitonClient
from .TitonFanSpeed import TitonFanSpeed
from .TitonGeneralInfo import TitonGeneralInfo
from .TitonKitchenTimer import TitonKitchenTimer

_LOGGER = logging.getLogger(__name__)


async def main(client):
    kitchen_request = TitonKitchenTimer(client)
    info_request = TitonGeneralInfo(client)
    fan_request = TitonFanSpeed(client)

    while True:
        print("\n")
        user_input = await aioconsole.ainput("Enter command: ")
        print("\n")

        if not client.is_connected:
            await client.connect()

        if user_input.lower() == "quit":
            print("Closing the connection")
            break
        elif user_input == "kitchen":
            response = await kitchen_request.perform()

            print(f"Kitchen timer is set to {response}")
        elif user_input == "set kitchen":
            value = kitchen_request.value + 1

            response = await kitchen_request.set_to(value)

            if response:
                print(f"Kitchen timer is set to {value}")
            else:
                print("Setting timer failed")
        elif user_input == "fan":
            response = await fan_request.perform()

            print(f"Fan speed is set to {response}")
        elif user_input == "set fan":
            value = await aioconsole.ainput("Enter value: ")
            value = int(value)

            response = await fan_request.set_to(value)

            if response:
                print(f"Fan speed is set to {value}")
            else:
                print("Setting fan speed failed")
        elif user_input == "info":
            await info_request.perform()
        else:
            await client.send_dat_message(user_input)


def run():
    """Entry point: resolve the MAC, then run the console."""
    mac = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("TITON_HRV_MAC")

    if not mac:
        sys.exit(
            "No HRV MAC address given.\n"
            "Usage: python -m titon.cli <MAC>   (e.g. AA-BB-CC-11-22-33)\n"
            "   or: set TITON_HRV_MAC in the environment."
        )

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    asyncio.run(main(TitonClient(mac)))


if __name__ == "__main__":
    run()
