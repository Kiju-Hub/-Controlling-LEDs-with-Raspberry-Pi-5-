#!/usr/bin/env python3

import os
import time

# 스위치와 LED 핀 번호
SWPIN = 25
GPIO_PINS = [8, 7, 16, 20]

# 초기 설정
def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
    for pin in GPIO_PINS:
        print(f"Setting GPIO {pin} as output")
        os.system(f"pinctrl set {pin} op")

# 현재 스위치 상태 읽기
def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"

# LED 전체 ON 또는 OFF
def set_leds(on):
    for pin in GPIO_PINS:
        state = "dh" if on else "dl"
        os.system(f"pinctrl set {pin} {state}")
    print("LED ON" if on else "LED OFF")

def main():
    setup()
    previous_state = "hi"
    led_on = False

    while True:
        switch_state = get_switch_state()

        # 버튼이 눌리는 순간만 감지
        if switch_state == "lo" and previous_state == "hi":
            led_on = not led_on
            set_leds(led_on)

        previous_state = switch_state
        time.sleep(0.05)

if __name__ == "__main__":
    main()
