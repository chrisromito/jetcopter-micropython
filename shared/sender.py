"""
Sender/Controller (black ESP32):
human = '40:91:51:1d:f3:a0'
bytes = b'@\x91Q\x1d\xf3\xa0'

Receiver (red ESP32):
human = '7c:87:ce:f6:cf:64'
bytes = b'|\x87\xce\xf6\xcfd'

Micropython Docs: https://docs.micropython.org/en/latest/library/espnow.html#introduction
"""
import sys
from asyncio import create_task, sleep_ms, run
import network
from espnow import ESPNow
import time


DEBUG = True
receiver = b'|\x87\xce\xf6\xcfd'  # MAC address of peer's wifi interface


async def main():
    esp: ESPNow = await setup()
    log('main()')
    while True:
        message: bytes = get_message()
        esp.send(message)
        log('Sent message')
        await sleep_ms(500)


async def timestamp_server(esp: ESPNow, timeout_ms=3000):
    while True:
        message: bytes = get_message()
        # if not await esp.asend(receiver, message):
        #     print("Heartbeat: peer not responding:", receiver)
        # else:
        #     print("Heartbeat: ping", receiver)
        esp.send(message)
        await sleep_ms(timeout_ms)


def get_message()-> bytes:
    return str(time.time()).encode()


async def setup()-> ESPNow:
    log('setup()')
    await sleep_ms(1000)
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    e = ESPNow()
    e.active(True)
    e.add_peer(receiver)  # Must add_peer() before send()
    e.send(receiver, "Starting...")
    log('Setup complete')
    return e


def log(message):
    if DEBUG:
        try:
            print(str(message))
        except:
            print('Caught exception whilst logging a message')


try:
    run(main())
except KeyboardInterrupt:
    pass
except Exception as err:
    log('runtime error:')
    log(err)
    # Crash in debug mode so we can use the REPL
    # Otherwise, reboot
    if DEBUG:
        raise err
    else:
        sys.exit()
