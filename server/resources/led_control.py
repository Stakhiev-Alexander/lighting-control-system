import RPi.GPIO as GPIO


GPIO.setwarnings(False)


class LedControl():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Create a dictionary called pins to store the pin number, name, and pin state:
        self.pins = {
            16: {'name': 'built-in LED'},
            23: {'name': 'GPIO 23'},
            24: {'name': 'GPIO 24'}
        }

        # Set each pin as an output and make it low:
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def set_pin_value(self, pin, value):
        message = 'Invalid value'
        if value == 1:
            # Set the pin high:
            GPIO.output(pin, GPIO.HIGH)
            # Save the status message to be passed into the template:
            message = f'Turned {pin} on.'
        elif value == 0:
            GPIO.output(pin, GPIO.LOW)
            message = f'Turned {pin} off.'

        print(message)
