"""
Example:
LED_PINS = [
    21,
    17,
    16
]
leds = Leds(ORANGE_PINS)
leds.on()
leds.off()
# Set brightness to 50%
await leds.set_brightness(50)
"""
import math
from uasyncio import gather, sleep_ms
from micropython import const
from machine import Pin, PWM

MAX_DUTY = const(1024)
MIN_DUTY = const(0)
MAX_BRIGHTNESS = const(100)


# Individual LEDs
# ########################
class Led:
    def __init__(self, pin):
        self.pin = pin
        self.pwm = PWM(self.pin, freq=2000)

    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

    def update(self, value):
        self.pin.value(1 if value else 0)

    async def fade_to(self, brightness, total_duration_ms=100):
        duty = brightness_to_duty(brightness)
        sleep_duration = int(total_duration_ms / duty)
        pwm = self.pwm
        for loop_duty in range(0, duty):
            pwm.duty(loop_duty)
            await sleep_ms(sleep_duration)

    async def pulse(self, duration_ms=1000):
        pwm = self.pwm
        pwm.init(freq=1000)
        loop_duration = int(duration_ms / 20)
        for i in range(20):
            pwm.duty(
                int(math.sin(i / 10 * math.pi) * 500 + 500)
            )
            await sleep_ms(loop_duration)
        pwm.init(freq=2000)

    @staticmethod
    def of(pin_number):
        return Led(Pin(pin_number, mode=Pin.OUT))


def brightness_to_duty(brightness):
    """
    B = Brightness % (0-100)
    N = Duty cycle

     B     N
    --- = ----
    100   1024

    Can be rewritten as:
    N = (1024*B)/100
    Therefore, duty cycle = (1024 * brightness)/100
    :param brightness:
    :return:
    """
    return (MAX_DUTY * brightness) / MAX_BRIGHTNESS


class Leds:
    def __init__(self, pins):
        self.leds = [
            Led.of(pin) for pin in pins
        ]

    async def set_brightness(self, brightness, total_duration_ms=100):
        tasks = [
            led.fade_to(brightness, total_duration_ms) for led in self.leds
        ]
        await gather(*tasks)

    def off(self):
        for led in self.leds:
            led.pwm.duty(0)

    def on(self):
        for led in self.leds:
            led.pwm.duty(MAX_DUTY - 1)
