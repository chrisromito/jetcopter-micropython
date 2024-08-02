from machine import Pin


class Button:
    def __init__(self, pin_number: int):
        self.pin = Pin(pin_number)
        self.pin.init(mode=Pin.IN, pull=Pin.PULL_DOWN)
        self._press_handled = False
        self._release_handled = False

    def is_pressed(self) -> bool:
        return bool(self.pin.value())

