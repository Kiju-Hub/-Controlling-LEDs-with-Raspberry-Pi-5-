#!/usr/bin/env python3

from gpiozero import LED
from time import sleep
import signal, sys

pins = [17, 18, 27, 22]
leds = [LED(pin) for pin in pins]

def cleanup(sig, frame):
    for led in leds: led.off()
    print("💡 모든 LED OFF (정리 완료)")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

while True:
    for i, led in enumerate(leds):
        [l.off() for l in leds]
        led.on()
        sleep(1)

