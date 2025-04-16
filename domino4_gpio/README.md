# gpiozero_domino4 🔁

Python(`gpiozero` 라이브러리)를 활용하여 Raspberry Pi의 GPIO 핀에 연결된 LED를 순차적으로 점등하는 도미노 스타일 프로젝트입니다.  
쉘 스크립트 버전(`domino4.sh`)과 동일한 로직을 Python으로 재구현했습니다.

---


## 🔴 시연 동영상  
> (https://youtube.com/shorts/bE27yohYqBE?feature=share)

---

## 📌 프로젝트 개요

- **목적**: Raspberry Pi 5의 GPIO 핀을 활용한 **LED 순차 점등 애니메이션**
- **핵심 기능**:
  - Python 스크립트를 통해 4개의 LED를 제어
  - 한 번에 하나의 LED만 켜지고, 나머지는 꺼짐
  - 좌 → 우 순서로 도미노처럼 LED가 1초 간격으로 점등
  - 무한 반복 실행

---

## ⚙️ 기술 스택 및 환경

| 항목             | 내용                              |
|------------------|-----------------------------------|
| Platform         | Raspberry Pi 5 (64-bit)           |
| OS               | Raspberry Pi OS (Debian 기반)     |
| Language         | Python 3                          |
| GPIO Control     | `RPi.GPIO` (GPIO 핀 제어 라이브러리) |
| Script Name      | `domino4.py`                      |

---

## 🧠 작동 원리

1. 4개의 GPIO 핀을 출력 모드로 설정 (예: 17, 18, 27, 22번 핀)
2. 반복문을 통해 각 핀을 하나씩 HIGH로 만들고 1초간 대기
3. 다음 핀으로 이동하면서 이전 핀은 LOW로 끔
4. 끝까지 가면 다시 처음 핀으로 돌아가 반복

---


## 💡 회로 구성도


- **GPIO 17** → LED 1
- **GPIO 18** → LED 2  
- **GPIO 27** → LED 3  
- **GPIO 22** → LED 4  

- 각 LED는 **330Ω 저항**과 함께 직렬 연결
- 공통 GND는 라즈베리파이의 **GND 핀**에 연결

📸 **![image](https://github.com/user-attachments/assets/a3ee14e2-00fb-4a51-bd81-8fb8d52e6c55)** 

---



## 📂 파일 구성

- `domino4.py` : Python 코드 본체  
- `README.md` : 프로젝트 설명서  

---

## 🧠 코드 설명 (`domino4.py`)

```python
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
✅ 주요 동작 흐름
GPIO 핀 설정:
pins = [17, 18, 27, 22]를 리스트로 선언하고, 각 핀을 LED(pin) 객체로 구성

인터럽트 처리:
signal.signal()을 통해 SIGINT(Ctrl+C) 또는 SIGTERM 발생 시
→ cleanup() 함수가 호출되어 모든 LED를 끄고 종료됨

반복 루프 동작:

모든 LED를 끔 → [l.off() for l in leds]

현재 차례의 LED만 켬 → led.on()

1초 대기 → sleep(1)

실행 방법:
chmod +x domino.py
./domino.py        # 또는
python3 domino.py


🔁 동작 시퀀스 예시

시간	점등된 GPIO 핀	LED 상태
1초	17		O X X X
2초	18		X O X X
3초	27		X X O X
4초	22		X X X O
5초~	17 (반복)	O X X X


```

## 🆚 기존 `domino4.sh`와의 차이점

| 항목             | Bash 버전 (`domino4.sh`)         | Python 버전 (`gpiozero_domino4.py`)         |
|------------------|----------------------------------|----------------------------------------------|
| **언어**         | Bash                             | Python (`gpiozero` 라이브러리 기반)          |
| **GPIO 제어**    | `pinctrl` 명령어 사용             | `gpiozero.LED` 객체로 제어                   |
| **인터럽트 처리**| `trap` + `cleanup` 함수           | `signal.signal()` + `cleanup()` 함수         |
| **실행 방식**    | `bash domino4.sh`                 | `./domino4.py` 또는 `python3 domino4.py`     |
| **코드 간결성**  | 반복 코드 많음                    | 리스트/루프 활용으로 간결하고 직관적        |

---

## 🧾 결론 및 기대 효과

이 프로젝트는 **GPIO 순차 제어**, **Python 기본 문법 학습**,  
그리고 **인터럽트 처리(`signal`)**를 실습할 수 있도록 구성된  
**기초 임베디드 개발 입문용 프로젝트**입니다.

또한 `gpiozero` 라이브러리를 활용하면  
GPIO를 **더 직관적이고 안전하게 제어**할 수 있기 때문에,  
**Python 기반의 GPIO 제어 프로젝트**에 처음 입문하는 사용자에게 매우 적합합니다.

