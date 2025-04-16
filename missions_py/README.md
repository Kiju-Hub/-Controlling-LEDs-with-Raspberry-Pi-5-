# 🔧 GPIO Button & LED Control – Mission Series (1~4)

Raspberry Pi의 GPIO 핀을 활용해
스위치 입력에 따라 LED를 제어하는 실습 프로젝트입니다.
총 4개의 미션으로 구성되어 있으며, 단계별로 기능이 점차 확장됩니다.
![Uploading image.png…]()

---

## 🔴 시연 동영상
> (https://youtube.com/shorts/bE27yohYqBE?feature=share)

---
## 📁 미션 구성

| 파일명         | 설명                                      |
|----------------|-------------------------------------------|
| mission1.py  | 버튼이 눌리면 LED 4개 ON, 떼면 OFF         |
| mission2.py  | 버튼을 누를 때마다 LED 상태 토글           |
| mission3.py  | 도미노 LED 점등 시퀀스 + 버튼 중단 기능    |
| mission4.py  | 버튼 누를 때마다 4비트 이진수 LED 카운터   |

---
## 🧩 회로도 구성

아래는 미션 공통 회로 구성입니다.
스위치와 LED는 다음과 같이 Raspberry Pi의 GPIO에 연결됩니다.

| 구성 요소     | 핀 번호 | 연결 설명                        |
|--------------|---------|----------------------------------|
| 스위치 (버튼) | GPIO 25 | 풀업 설정 후 GND와 연결         |
| LED 1        | GPIO 8  | 330Ω 저항 → GND로 연결           |
| LED 2        | GPIO 7  | 330Ω 저항 → GND로 연결           |
| LED 3        | GPIO 16 | 330Ω 저항 → GND로 연결           |
| LED 4        | GPIO 20 | 330Ω 저항 → GND로 연결           |

> 모든 LED는 공통 GND에 연결되며, 전류 제한용 저항(330Ω)을 반드시 사용해야 합니다.

---


## ⚙️ 기술 스택 및 환경

| 항목              | 내용                                      |
|-------------------|-------------------------------------------|
| 플랫폼            | Raspberry Pi 5 (64-bit)                   |
| 운영체제          | Raspberry Pi OS (Debian 기반)             |
| 프로그래밍 언어   | Python 3                                  |
| GPIO 제어 방식    | pinctrl 명령어 기반 (os.system) 사용 |
| LED 제어          | 디지털 출력 (High: dh, Low: dl)       |
| 스위치 입력 방식  | 디지털 입력 + 풀업 설정 (ip, pu)      |
| 프로젝트 파일     | mission1.py ~ mission4.py             |


---


## 📘 코드 설명 – mission1.py

Raspberry Pi의 pinctrl 명령어를 사용해,
**스위치 입력(GPIO 25)** 상태에 따라 **LED 4개(GPIO 8, 7, 16, 20)**를 ON/OFF하는 코드입니다.

---
## 🟥 Mission1.py 코드 설명

python
#!/usr/bin/env python3
이 스크립트를 Python 3 인터프리터로 실행하겠다는 선언 (리눅스 실행 환경에서 사용)


import os, time
os: 터미널 명령어 실행 (os.system, os.popen)

time: 시간 지연을 위한 sleep() 함수 사용

SWPIN = 25
GPIO_PINS = [8, 7, 16, 20]
SWPIN: 스위치 입력을 받을 GPIO 핀 번호

GPIO_PINS: 제어할 4개의 LED 핀 번호 (왼쪽부터 순서대로)

🔧 setup() – GPIO 초기 설정 함수

def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
스위치 핀(SWPIN)을 **입력 모드(input)**로 설정하고,
**풀업 저항(pull-up)**을 활성화하여 스위치가 눌렸는지 안정적으로 감지 가능하게 함


    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} op")
LED 핀들을 **출력 모드(output)**로 설정함

🔍 get_switch_state() – 스위치 상태 읽기 함수

def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"
pinctrl get 명령어로 스위치 핀의 현재 상태를 읽어옴

"lo" → 스위치가 눌린 상태 (GND에 연결)

"hi" → 스위치가 눌리지 않은 상태 (기본 풀업 상태)

💡 set_leds(state) – LED 일괄 제어 함수

def set_leds(state):
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} {state}")
전달받은 상태("dh": ON, "dl": OFF)를 모든 LED 핀에 적용

반복문을 통해 LED 4개를 동시에 제어함

🚦 main() – 메인 제어 루프

def main():
    setup()
실행되자마자 GPIO 핀 설정(setup) 수행


    while True:
무한 루프: 스위치 상태를 계속 감지하면서 LED를 실시간 제어


        switch_state = get_switch_state()
현재 스위치 상태 읽기


        if switch_state == "lo":
            set_leds("dh")
스위치가 눌렸으면 → 모든 LED ON


        else:
            set_leds("dl")
스위치가 떼졌으면 → 모든 LED OFF

        time.sleep(0.05)
너무 빠른 루프를 방지하고 디바운싱 처리 역할도 겸함 (50ms 대기)

▶ 프로그램 실행 조건


if __name__ == "__main__":
    main()
이 파일이 직접 실행될 경우에만 main() 함수를 호출하여 프로그램 시작

✅ 요약
스위치를 누르면 LED 4개가 동시에 켜지고

손을 떼면 LED가 꺼지는 단순 반응형 제어 구조

실시간 감지 및 제어를 위한 while 루프와

pinctrl 명령어 기반의 입출력 제어 구조를 이해하는 데 좋은 예제입니다.



---


## 🟡 코드 설명 – mission2.py

버튼을 누를 때마다 LED 상태가 **ON/OFF로 토글되는** 구조입니다.
스위치의 상태 변화(hi → lo)를 감지하여 동작을 트리거합니다.

---

python
#!/usr/bin/env python3
Python 3 인터프리터로 실행되도록 지정


import os, time
os: 시스템 명령어 실행 (pinctrl)

time: 시간 지연을 위한 sleep() 사용


SWPIN = 25
GPIO_PINS = [8, 7, 16, 20]
스위치 입력 핀: 25번

제어할 LED 핀들: 8, 7, 16, 20 (총 4개)

🔧 setup() – GPIO 초기 설정

def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
    for pin in GPIO_PINS:
        print(f"Setting GPIO {pin} as output")
        os.system(f"pinctrl set {pin} op")
스위치 핀을 입력 모드 + 풀업 설정

각 LED 핀을 출력 모드로 설정

🔍 get_switch_state() – 현재 스위치 상태 읽기

def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"
pinctrl get 명령어 결과에 "lo"가 포함되어 있으면 → 버튼이 눌린 상태로 판단

💡 set_leds(on) – LED 전체 ON/OFF

def set_leds(on):
    for pin in GPIO_PINS:
        state = "dh" if on else "dl"
        os.system(f"pinctrl set {pin} {state}")
    print("LED ON" if on else "LED OFF")
인자로 받은 True/False 값에 따라 모든 LED 핀을 켜거나 끔

터미널에 현재 상태 출력

🚦 main() – 버튼 상태 변화에 따른 LED 토글

def main():
    setup()
    previous_state = "hi"
    led_on = False
이전 스위치 상태와 LED의 현재 상태를 추적할 변수 초기화


    while True:
        switch_state = get_switch_state()
현재 스위치 상태 읽기


        if switch_state == "lo" and previous_state == "hi":
            led_on = not led_on
            set_leds(led_on)
버튼이 눌리는 순간(hi → lo)을 감지했을 때만 동작

LED 상태를 반대로 뒤집고 전체 LED에 적용


        previous_state = switch_state
        time.sleep(0.05)
다음 루프를 위해 현재 상태 저장

50ms 대기 → 디바운싱 방지 + CPU 과부하 방지

▶ 프로그램 실행 조건

if __name__ == "__main__":
    main()
이 파일이 직접 실행되는 경우에만 main()을 실행

✅ 요약
버튼이 눌리는 순간(hi → lo)을 감지해
LED ON/OFF 상태를 토글하는 방식입니다.

이전 상태를 기억하는 previous_state와
현재 ON/OFF 상태를 저장하는 led_on 변수로
스위치 누름에 대한 반응을 한 번만 실행하게 만듭니다.

pinctrl 명령어 기반의 GPIO 제어와
입력 감지 → 상태 변화 → 출력 적용 흐름을 익히기 좋은 구조입니다.



## 🔵 코드 설명 – mission3.py

버튼을 누르면 도미노처럼 LED가 순서대로 켜지고,
다시 누르면 **도중에도 즉시 중단**되는 구조입니다.

---

python
#!/usr/bin/env python3
import os, time
OS 명령어 실행 및 시간 제어를 위한 기본 라이브러리


SWPIN = 25
GPIO_PINS = [8, 7, 16, 20]
스위치 핀 번호 및 도미노 방식으로 점등할 LED 핀 번호 리스트

🔧 setup() – GPIO 핀 설정

def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} op")
스위치는 입력/풀업 설정, LED는 출력 모드 설정

🔍 get_switch_state()

def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"
"lo"는 스위치가 눌린 상태, "hi"는 눌리지 않은 상태

💡 turn_off_all_leds()

def turn_off_all_leds():
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} dl")
    print("모든 LED OFF")
모든 LED를 꺼주는 보조 함수

🔁 run_domino_one_cycle_interruptible()

def run_domino_one_cycle_interruptible():
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} dh")
각 LED를 하나씩 순서대로 켜고


        duration = 1.0
        check_interval = 0.05
        elapsed = 0
1초 대기를 짧게 쪼개어 버튼 눌림을 중간에 확인할 수 있도록 설정


        while elapsed < duration:
            if get_switch_state() == "lo":
                os.system(f"pinctrl set {pin} dl")
                return False
            time.sleep(check_interval)
            elapsed += check_interval
중간에 버튼이 눌리면 즉시 중단하고 현재 LED를 끄고 False 반환


        os.system(f"pinctrl set {pin} dl")
        if get_switch_state() == "lo":
            return False
각 LED를 꺼주고 다음 LED로 이동, 다시 눌림 여부 재확인


    return True
전체 도미노 한 사이클이 정상 종료되면 True 반환

🚦 main()

def main():
    setup()
    previous_state = "hi"
    running = False
running: 도미노 작동 여부

previous_state: 버튼 눌림 상태 변화 감지를 위한 변수

    try:
        while True:
            switch_state = get_switch_state()

            if switch_state == "lo" and previous_state == "hi":
                running = not running
                print("▶ 도미노 시작" if running else "⏹ 도미노 정지")
                while get_switch_state() == "lo":
                    time.sleep(0.05)

            previous_state = switch_state
버튼을 누르는 순간을 감지해 도미노를 시작하거나 멈춤

            if running:
                keep_going = run_domino_one_cycle_interruptible()
                if not keep_going:
                    print("⏹ 도미노 도중 중단")
                    running = False
                    turn_off_all_leds()
            else:
                time.sleep(0.05)
도중에 버튼이 눌리면 도미노 동작을 중단하고 모든 LED 끔


    except KeyboardInterrupt:
        print("\n[Ctrl+C] 종료 요청됨.")
    finally:
        turn_off_all_leds()
종료 시에도 모든 LED OFF


if __name__ == "__main__":
    main()
✅ 요약
버튼을 누르면 LED가 순차적으로 켜졌다 꺼지는 도미노 효과 실행

실행 중 다시 버튼을 누르면 즉시 중단되고 모든 LED OFF

반복 루프와 인터럽트 감지를 함께 구현한 실전형 예제

---

## 🟥 코드 설명 – mission4.py

버튼을 누를 때마다 숫자를 1씩 증가시키고,
해당 숫자를 **4비트 이진수로 변환해 LED로 표시**하는 카운터입니다.

---

python
#!/usr/bin/env python3
import os, time
명령어 실행과 시간 지연을 위한 기본 라이브러리


SWPIN = 25
GPIO_PINS = [8, 7, 16, 20]
스위치 입력 핀과 4개의 LED 출력 핀 정의

🔧 setup()

def setup():
    os.system(f"pinctrl set {SWPIN} ip")
    os.system(f"pinctrl set {SWPIN} pu")
    for pin in GPIO_PINS:
        os.system(f"pinctrl set {pin} op")
스위치와 LED 핀 초기 설정

🔍 get_switch_state()

def get_switch_state():
    result = os.popen(f"pinctrl get {SWPIN}").read()
    return "lo" if "lo" in result else "hi"
스위치 상태 확인

💡 display_binary(counter)

def display_binary(counter):
    for i in range(4):
        bit_val = (counter >> (3 - i)) & 1
        pin = GPIO_PINS[i]
        if bit_val == 1:
            os.system(f"pinctrl set {pin} dh")
        else:
            os.system(f"pinctrl set {pin} dl")
입력된 숫자(counter)를 4비트 이진수로 변환 후
각 비트 값을 LED에 반영 (MSB부터)

🚦 main()

def main():
    setup()
    counter = 0
    previous_state = "hi"
숫자 카운터 초기화, 버튼 상태 변화 감지 준비

    try:
        while True:
            switch_state = get_switch_state()

            if switch_state == "lo" and previous_state == "hi":
                counter = (counter + 1) % 16
                print(f"Button pressed → Counter: {counter}")
                display_binary(counter)
버튼이 눌리는 순간만 감지

0부터 15까지 증가 → 16이면 다시 0으로 순환


            previous_state = switch_state
            time.sleep(0.05)
디바운싱 및 CPU 보호


    except KeyboardInterrupt:
        for pin in GPIO_PINS:
            os.system(f"pinctrl set {pin} dl")
Ctrl+C 종료 시 LED OFF


if __name__ == "__main__":
    main()
✅ 요약
버튼을 누를 때마다 숫자 카운터 증가

해당 숫자를 4비트 이진수로 LED 표시

반복 구조와 비트 연산, 디지털 출력 제어 학습에 유용한 예제
