""" name_port_gpio.py
 
    This is a demo python file showing how to take paramaters
    from command line for device name, port, and GPIO.
    All credit goes to https://github.com/toddmedema/echo/
    for making the first working versions of this code.
"""
 
import fauxmo
import logging
import time
import sys
import RPi.GPIO as GPIO ## Import GPIO library

#############Servo varianles
from gpiozero import Servo
from time import sleep

###################
from debounce_handler import debounce_handler
 
logging.basicConfig(level=logging.DEBUG)
 
class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    #TRIGGERS = {str(sys.argv[1]): int(sys.argv[2])}
    #TRIGGERS = {"Light": 52000}
    TRIGGERS = {"FLORA": 52000}

    def act(self, client_address, state, name):
        print("State", state, "from client @", client_address)
        if name=="FLORA":
            ServoPin=11
            Angulo=100
            PWM_start=3

            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(ServoPin, GPIO.OUT)
            GPIO.output(ServoPin, state)
            pwm=GPIO.PWM(ServoPin, 50)
 
            pwm.start(PWM_start)
            sleep(1)

            DC=1./18.*(Angulo)+2
            pwm.ChangeDutyCycle(DC)
            sleep(0.8)

            pwm.start(PWM_start)
            sleep(2)
            pwm.stop()
            GPIO.cleanup()

        else:
            print("Device not found!")
        return True
 
if __name__ == "__main__":
    sleep(10)
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)
 
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception as e:
            logging.critical("Critical exception: "+ e.args  )
            break
