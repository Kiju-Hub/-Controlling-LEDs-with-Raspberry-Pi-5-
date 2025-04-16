#!/usr/bin/env python
from gpiozero import LED
from time import sleep
import signal
import sys

# 사용할 GPIO 핀 번호 (가장 큰 비트부터)
pins = [17, 18, 27]
leds = [LED(pin) for pin in pins]

# 종료 시 모든 LED OFF
def cleanup(signal_received, frame):
    print("💡 모든 LED OFF (정리 완료)")
    for led in leds:
        led.off()
    sys.exit(0)

# SIGINT (Ctrl+C), SIGTERM 처리
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# 무한 루프
while True:
    for i in range(8):
        print(f"Count: {i:03b}")
        for j in range(3):
            if (i >> (2 - j)) & 1:
                leds[j].on()
            else:
                leds[j].off()
        sleep(1)
