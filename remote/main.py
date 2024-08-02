from time import sleep
from machine import ADC, Pin

# Green = x = 25
# Yellow/blue = y = 26

x_axis = ADC(Pin(25))
x_axis.atten(ADC.ATTN_11DB)
y_axis = ADC(Pin(26))
y_axis.atten(ADC.ATTN_11DB)


# Default voltage = 1775
# Positive value voltage >= 4000
# Negative value voltage <= 600


class Joystick:
    def __init__(self, x_pin_n: int, y_pin_n: int):
        self.x_adc = ADC(Pin(x_pin_n))
        self.x_adc.atten(ADC.ATTN_11DB)
        self.y_adc = ADC(Pin(y_pin_n))
        self.y_adc.atten(ADC.ATTN_11DB)

    def read(self, _adc):
        value = _adc.read()
        if value <= 600:
            return -1
        elif value >= 4000:
            return 1
        return 0

    def x_value(self):
        return self.read(self.x_adc)

    def y_value(self):
        return self.read(self.y_adc)


stick = Joystick(25, 26)

while True:
    x_value = stick.x_value()
    if x_value:
        print('x: ', str(x_value))
    y_value = stick.y_value()
    if y_value:
        print('y: ', str(y_value))
    sleep(0.1)

