# count8.py 🔢

Python(`gpiozero` 라이브러리)을 활용하여  
Raspberry Pi의 GPIO 핀에 연결된 LED 3개를 사용해 **0부터 7까지 이진수(3비트)로 카운트**하는 프로젝트입니다.

---

## 🔴 시연 동영상  
> (https://youtube.com/shorts/bE27yohYqBE?feature=share)

---

## 📌 프로젝트 개요

- **목적**: GPIO 핀을 통해 **3비트 이진수(000~111)**를 LED로 시각적으로 표현
- **핵심 기능**:
  - 숫자 0부터 7까지 1초 간격으로 1씩 증가
  - 각 숫자를 3비트 이진수로 변환하여 3개의 LED에 반영
  - 예: `3 → 011 → [OFF, ON, ON]`

Count: 0 → LED 상태: OFF OFF OFF  
Count: 1 → LED 상태: OFF OFF ON  
Count: 2 → LED 상태: OFF ON OFF  
...  
Count: 7 → LED 상태: ON ON ON  

---

## ⚙️ 기술 스택 및 환경

| 항목             | 내용                              |
|------------------|-----------------------------------|
| Platform         | Raspberry Pi 5 (64-bit)           |
| OS               | Raspberry Pi OS (Debian 기반)     |
| Language         | Python 3                          |
| GPIO Control     | `gpiozero` (LED 제어 라이브러리)  |
| Script Name      | `count8.py`                       |

---


## 💡 회로 구성도

- **GPIO 17** → LED (최상위 비트)  
- **GPIO 18** → LED (중간 비트)  
- **GPIO 27** → LED (최하위 비트)   
- LED 각각에는 **저항**을 직렬로 연결  
- 공통 GND는 라즈베리파이의 **GND 핀**    

| GPIO 핀 | 역할 | LED 위치 |
|---------|------|-----------|
| 17번    | 2의 자리 비트 (MSB) | LED 1 |
| 18번    | 1의 자리 비트      | LED 2 |
| 27번    | 0의 자리 비트 (LSB) | LED 3 |

- 각 LED는 **330Ω 저항**과 **공통 GND**로 연결되어야 함  


📸 **![image](https://github.com/user-attachments/assets/a3ee14e2-00fb-4a51-bd81-8fb8d52e6c55)**  
❗( GPIO PIN 22번 LED핀, 저항, GND연결은 무시하셔도 좋습니다.)

---

## 🧠 작동 원리

1. **핀 선언**: `[17, 18, 27]` 핀을 순서대로 배열 (가장 큰 비트부터)
2. **0~7까지 반복문 실행** (총 3비트 이진수)
3. 각 비트마다 `1`이면 해당 LED를 **켜고**, `0`이면 **끔**
4. 1초 간격으로 다음 숫자 표시


---

## 📂 파일 구성

- `count8.py` : Python LED 카운터 코드
- `README.md` : 설명 문서

---


## ✅ 코드 설명 (`count8.py`)

```python
from gpiozero import LED
gpiozero 라이브러리에서 LED 클래스를 불러옴

특정 GPIO 핀을 on/off 제어할 수 있는 객체 제공

from time import sleep
일정 시간 동안 대기할 수 있는 sleep() 함수 사용

import signal, sys
signal: 종료 신호(Ctrl+C 등) 처리

sys: 안전한 프로그램 종료 (sys.exit())


pins = [17, 18, 27]
leds = [LED(pin) for pin in pins]
사용할 GPIO 핀 번호를 리스트로 정의 (MSB부터 LSB 순서)

각 핀에 대해 LED 객체 생성 → leds 리스트에 저장

def cleanup(signal_received, frame):
    print("💡 모든 LED OFF (정리 완료)")
    for led in leds:
        led.off()
    sys.exit(0)
프로그램 종료 시 모든 LED를 꺼주는 함수

인터럽트 시 안전하게 종료되도록 처리


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
Ctrl+C(SIGINT)나 종료 요청(SIGTERM) 시 cleanup() 함수 호출

while True:
    for i in range(8):
무한 루프로 0부터 7까지 반복

총 8가지의 3비트 조합을 순차적으로 표시

        print(f"Count: {i:03b}")
현재 카운트 숫자를 3자리 이진수로 출력

예: i = 3 → "Count: 011"

        for j in range(3):
            if (i >> (2 - j)) & 1:
                leds[j].on()
            else:
                leds[j].off()
각 비트를 하나씩 검사해 해당 LED를 켜거나 끔

i >> (2 - j)로 각 비트를 오른쪽으로 이동

& 1로 해당 비트가 1인지 0인지 판별

결과적으로 이진수 비트에 따라 LED ON/OFF 결정

        sleep(1)
각 숫자 상태를 1초 동안 유지

```



## 🧾 결론 및 기대 효과

이 프로젝트는 Raspberry Pi의 GPIO를 활용하여  
**이진수(bitwise) 개념과 LED 제어를 시각적으로 익힐 수 있는 학습형 실습 예제**입니다.

- `gpiozero` 라이브러리를 사용함으로써 **간단한 코드로 핀 제어**가 가능하고,
- **비트 시프트와 마스킹 연산**을 통해 **논리적 사고력 향상**에도 도움을 줍니다.

특히 이 프로젝트는 다음과 같은 목적에 적합합니다:

- ✅ Python을 활용한 임베디드/하드웨어 제어 입문
- ✅ 2진수/비트 연산의 실습 및 시각화 학습
- ✅ GPIO 라이브러리(`gpiozero`)의 실전 활용법 체험
- ✅ 단순한 LED 깜빡임을 넘은 **논리 기반 제어 구조 익히기**
