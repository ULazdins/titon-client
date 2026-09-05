# titon

Async Python client for [Titon Aura-T](https://www.titon.com/) heat recovery
ventilation (HRV) units.

The unit does not expose a local API. It keeps an outbound connection to
Titon's relay at `app.manageiaq.com:6275`, and clients address a specific unit
by its MAC address over that relay. This library speaks that protocol.

> Reverse engineered from the vendor app's traffic. Unofficial and unaffiliated
> with Titon. The protocol may change without notice.

## Install

```sh
pip install titon
```

The interactive console needs one extra dependency:

```sh
pip install "titon[cli]"
```

## Usage

```python
import asyncio

from titon import TitonClient, TitonFanSpeed


async def main():
    client = TitonClient("AA-BB-CC-11-22-33")  # your unit's MAC
    await client.connect()

    fan = TitonFanSpeed(client)
    print("current fan speed:", await fan.perform())

    await fan.set_to(3)

    client.disconnect()


asyncio.run(main())
```

Each capability is a small request object wrapping the client:

| Class | Reads | Writes |
| --- | --- | --- |
| `TitonGeneralInfo` | temperatures, humidity, status flags | — |
| `TitonFanSpeed` | current fan speed | `set_to(speed)` |
| `TitonKitchenTimer` | kitchen boost timer | `set_to(minutes)` |
| `TitonHumidity` | humidity threshold | `set_to(percent)` |
| `TitonFilter` | filter change status | `set_changed()` |
| `TitonSummer` | `read_boost_status()` | — |
| `TitonHandshake` | performed automatically by `connect()` | — |

## Console

```sh
python -m titon.cli AA-BB-CC-11-22-33
```

Or set `TITON_HRV_MAC` and omit the argument. Commands: `info`, `fan`,
`set fan`, `kitchen`, `set kitchen`, `quit`. Anything else is sent as a raw
`DAT` message.

## Protocol notes

[`docs/HRV_PROTOCOL_REFERENCE.md`](docs/HRV_PROTOCOL_REFERENCE.md) is the
message reference; [`docs/protocol-notes.md`](docs/protocol-notes.md) holds
the raw capture notes.

> Your unit's MAC is effectively its credential on Titon's relay — the protocol
> carries no other authentication. Don't publish it.

## Home Assistant

The Home Assistant integration built on this library lives at
[ULazdins/titon-has](https://github.com/ULazdins/titon-has).

## License

MIT
