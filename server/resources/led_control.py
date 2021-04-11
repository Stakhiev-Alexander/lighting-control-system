import logging

import RPi.GPIO as GPIO


class LedControl():
    def __inti__(self):
        GPIO.setmode(GPIO.BCM)

        # Create a dictionary called pins to store the pin number, name, and pin state:
        self.pins = {
            23: {'name': 'GPIO 23', 'state': GPIO.LOW},
            24: {'name': 'GPIO 24', 'state': GPIO.LOW}
        }

        # Set each pin as an output and make it low:
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def set_pin_value(self, pin, value):
        device_name = self.pins[pin]['name']
        # If the action part of the URL is "on," execute the code indented below:
        if value == 1:
            # Set the pin high:
            GPIO.output(pin, GPIO.HIGH)
            # Save the status message to be passed into the template:
            message = "Turned " + device_name + " on."
        elif value == 0:
            GPIO.output(pin, GPIO.LOW)
            message = "Turned " + device_name + " off."

        logging.info(message)
