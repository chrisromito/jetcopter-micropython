"""
Sender/Controller (black ESP32):
human = '40:91:51:1d:f3:a0'
bytes = b'@\x91Q\x1d\xf3\xa0'

Receiver (this ESP32):
human = '7c:87:ce:f6:cf:64'
bytes = b'|\x87\xce\xf6\xcfd'

Micropython Docs: https://docs.micropython.org/en/latest/library/espnow.html#introduction
"""
import sys
from asyncio import create_task, sleep_ms, run
import network
import espnow
from espnow import ESPNow
import time

DEBUG = True
sender = b'@\x91Q\x1d\xf3\xa0'  # MAC address of peer's wifi interface


async def main():
    esp: ESPNow = await setup()
    log('main()')
    for host, message in esp:
        print('Message: ', str(message))
        print('Host: ', str(host))
        log_sender_rssi(esp)


def log_sender_rssi(esp: ESPNow):
    peer_record = esp.peers_table.get(sender, None)
    if peer_record is not None:
        rssi, _ = peer_record
        print('Sender RSSI: ', str(rssi))
    else:
        print('Could not find sender in the peer table')


async def setup() -> ESPNow:
    log('setup()')
    await sleep_ms(1000)
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    e = ESPNow()
    e.active(True)
    e.add_peer(sender)  # Must add_peer() before send()
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
    print('-- End main --')
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
