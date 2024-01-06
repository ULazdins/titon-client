import asyncio
import logging

import aioconsole  # 3rd party dep

from TitonClient import TitonClient
from TitonGeneralInfo import TitonGeneralInfo
from TitonKitchenTimer import TitonKitchenTimer

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s - %(levelname)s - %(message)s",
    # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


async def main(client):
    kitchen_request = TitonKitchenTimer(client)
    info_request = TitonGeneralInfo(client)

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
        elif user_input == "info":
            response = await info_request.perform()
        else:
            await client.send_dat_message(user_input)


if __name__ == "__main__":
    client = TitonClient("D2-95-00-00-00-9E")

    asyncio.run(main(client))
