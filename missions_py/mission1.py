#!/usr/bin/env python3

import os
import time

# 스위치 핀 번호
SWPIN = 25

# LED 핀 번호들
GPIO_PINS = [8, 7, 16, 20]

# GPIO 설정 함수
def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
    for pin in GPIO_PINS:
        print(f"Setting GPIO {pin} as output")
        os.system(f"pinctrl set {pin} op")

# GPIO 상태 읽기
def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"

# LED 상태 설정
def set_leds(state):  # state = 'dh' or 'dl'
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} {state}")

# 메인 루프
def main():
    setup()
    while True:
        switch_state = get_switch_state()

        if switch_state == "lo":
            set_leds("dh")  # 버튼 누르면 ON
        else:
            set_leds("dl")  # 버튼 떼면 OFF

        time.sleep(0.05)

if __name__ == "__main__":
    main()
