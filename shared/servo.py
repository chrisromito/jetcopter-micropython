from micropython import const
from machine import Pin, PWM

MILLION = const(1000000)
MAX_DUTY = const(1023)


def scale(from_min, from_max, to_min, to_max):
    to_diff = to_max - to_min
    from_diff = from_max - from_min

    def _scale(value):
        return value - from_min * to_diff / from_diff + to_min

    return _scale


def clamp(lower, upper, value):
    return max(lower, min(value, upper))


def microsec_to_duty(freq, pulse_min, pulse_max, microsec):
    width = clamp(pulse_min, pulse_max, microsec)
    return ((width * MAX_DUTY) * freq) // MILLION


class Servo:
    """
    Params
    :param Pin pin: Pin object for the Servo control wire
    :param int angle: Max angle of the servo.  Ex. my cheapo servo goes from 0-160,
    so I used 160 as the default
    :param int pulse_min: Min pulse width in microsec
    :param int pulse_max: Max pulse width in microsec
    :param int freq: PWM signal frequency in hertz.  Most servos are 50hz
    """

    def __init__(self, pin, angle=160, pulse_min=600, pulse_max=2400, freq=50):
        self.pin = pin
        self.pwm = PWM(self.pin, freq=freq, duty=0)
        self.angle = angle
        self.value = 0
        self.pulse_min = pulse_min
        self.pulse_max = pulse_max
        self.freq = freq

    def to(self, degrees):
        """
        Set the servo angle to "degrees"
        """
        if self.value == degrees:
            return self
        degrees = clamp(0, self.angle, degrees)
        self.value = degrees
        total_range = self.pulse_max - self.pulse_min
        microsec = (total_range * degrees // self.angle) + self.pulse_min
        return self.write_microsec(microsec)

    def write_microsec(self, microsec):
        """
        PWM write a signal "microsec" long
        Pass in a falsy value to disable PWM
        """
        self.pwm.duty(
            int(microsec_to_duty(self.freq, self.pulse_min, self.pulse_max, microsec))
        )
        return self


class Esc(Servo):
    """
    Esc controller class
    All gas, no brakes

    :param Pin pin: Pin object for the ESC control wire
    :param int pulse_min: Min pulse width in microsec. You can set this
    in your BLHeli config
    :param int pulse_max: Max pulse width in microsec. You can set this
    in your BLHeli config
    :param int freq: PWM signal frequency in hertz.  Most ESCs are 50hz
    """

    def __init__(self, pin, pulse_min=1040, pulse_max=1960, freq=50):
        super().__init__(pin, 100, pulse_min, pulse_max, freq)

    def throttle(self, value):
        """
        :param int value: Throttle value from 0-100
        0 = 0% throttle
        100 = 100% (max) throttle
        """
        return self.to(value)
