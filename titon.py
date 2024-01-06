import asyncio
import aioconsole  # 3rd party dep
from TitonClient import TitonClient


async def main(client):
    await client.connect()

    while True:
        await asyncio.sleep(
            2
        )  # TODO: FIX - awaits fro server to return before accepting a new command
        print("\n")
        user_input = await aioconsole.ainput("Enter command: ")
        if user_input.lower() == "quit":
            print("Closing the connection")
            break
        else:
            client.send_raw_message(user_input)


if __name__ == "__main__":
    client = TitonClient("D2-95-00-00-00-9E")

    asyncio.run(main(client))
