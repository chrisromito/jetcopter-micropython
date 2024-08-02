from time import sleep
from machine import ADC, Pin


# Green = x = 27
# Yellow = y = 15

x_axis = ADC(Pin(27))
# y_axis = ADC(Pin(15))


while True:
    x_value = x_axis.read_u16()
    if x_value:
        print(x_value)
    sleep(0.1)
