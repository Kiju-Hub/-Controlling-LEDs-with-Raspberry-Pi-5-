#!/usr/bin/env python3

import os
import time

# 설정
SWPIN = 25
GPIO_PINS = [8, 7, 16, 20]

# 초기 GPIO 설정
def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} op")

# 버튼 상태 읽기
def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"

# 모든 LED 끄기
def turn_off_all_leds():
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} dl")
    print("모든 LED OFF")

# 도미노 시퀀스 한 번 실행 (중간에 버튼 눌림 감지)
def run_domino_one_cycle_interruptible():
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} dh")

        # 1초 동안 sleep하지 말고 → 짧게 쪼개서 버튼 상태 확인
        duration = 1.0  # 총 1초간 대기
        check_interval = 0.05  # 50ms마다 버튼 상태 확인
        elapsed = 0

        while elapsed < duration:
            if get_switch_state() == "lo":
                os.system(f"pinctrl set {pin} dl")  # 현재 LED 꺼주기
                return False
            time.sleep(check_interval)
            elapsed += check_interval

        os.system(f"pinctrl set {pin} dl")

        # 또 눌렸는지 확인 (안전망)
        if get_switch_state() == "lo":
            return False

    return True


# 메인 루프
def main():
    setup()
    previous_state = "hi"
    running = False

    try:
        while True:
            switch_state = get_switch_state()

            # 버튼이 눌리는 순간: 토글
            if switch_state == "lo" and previous_state == "hi":
                running = not running
                print("▶ 도미노 시작" if running else "⏹ 도미노 정지")

                # 버튼 떼기를 기다림 (디바운싱)
                while get_switch_state() == "lo":
                    time.sleep(0.05)

            previous_state = switch_state

            if running:
                keep_going = run_domino_one_cycle_interruptible()
                if not keep_going:
                    print("⏹ 도미노 도중 중단")
                    running = False
                    turn_off_all_leds()
            else:
                time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n[Ctrl+C] 종료 요청됨.")
    finally:
        turn_off_all_leds()

if __name__ == "__main__":
    main()
