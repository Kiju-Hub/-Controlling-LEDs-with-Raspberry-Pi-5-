#!/usr/bin/env python3

import os
import time

# 스위치와 LED 핀 설정
SWPIN = 25
GPIO_PINS = [8, 7, 16, 20]  # Bit3 Bit2 Bit1 Bit0

# GPIO 초기 설정
def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} op")
        print(f"GPIO {pin} set as output")

# 버튼 상태 확인
def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"

# 4-bit 값을 LED로 출력
def display_binary(counter):
    for i in range(4):
        bit_val = (counter >> (3 - i)) & 1  # 상위 비트부터
        pin = GPIO_PINS[i]
        if bit_val == 1:
            os.system(f"pinctrl set {pin} dh")
        else:
            os.system(f"pinctrl set {pin} dl")

def main():
    setup()
    counter = 0
    previous_state = "hi"

    try:
        while True:
            switch_state = get_switch_state()

            # 버튼이 눌리는 순간 (hi → lo)
            if switch_state == "lo" and previous_state == "hi":
                counter = (counter + 1) % 16  # 0~15 반복
                print(f"Button pressed → Counter: {counter}")
                display_binary(counter)

            previous_state = switch_state
            time.sleep(0.05)  # 디바운싱 및 CPU 보호

    except KeyboardInterrupt:
        print("\n[Ctrl+C] 종료됨.")
        # 모든 LED 끄기
        for pin in GPIO_PINS:
            os.system(f"pinctrl set {pin} dl")

if __name__ == "__main__":
    main()
