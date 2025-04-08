# 🔁 domino4.sh – 도미노 LED 점등 효과 (Raspberry Pi 5)

이 프로젝트는 Raspberry Pi 5의 GPIO 핀에 연결된 4개의 LED를 활용하여  
LED가 순차적으로 켜지고 꺼지는 **도미노 효과**를 구현합니다.  
각 LED는 1초 간격으로 하나씩 켜지고, 나머지 LED는 꺼지는 방식으로 반복됩니다.

---

## 🔴 시연 동영상  
> (https://youtube.com/shorts/bE27yohYqBE?feature=share)

---

## 📌 프로젝트 개요

- **목적**: Raspberry Pi 5의 GPIO 핀을 활용한 **LED 순차 점등 애니메이션**
- **핵심 기능**:
  - 4개의 LED 중 하나만 1초 동안 켜짐
  - 나머지 LED는 항상 꺼짐
  - 반복적으로 도미노처럼 LED가 좌→우 순서로 점등

---

## ⚙️ 기술 스택 및 환경

| 항목             | 내용                            |
|------------------|---------------------------------|
| Platform         | Raspberry Pi 5 (64-bit)         |
| OS               | Raspberry Pi OS (Debian 기반)   |
| Language         | Bash Shell Script               |
| GPIO Control     | `pinctrl` CLI 유틸리티          |

---

## 💡 회로 구성도


- **GPIO 17** → LED 1
- **GPIO 18** → LED 2  
- **GPIO 27** → LED 3  
- **GPIO 22** → LED 4  

- 각 LED는 **330Ω 저항**과 함께 직렬 연결
- 공통 GND는 라즈베리파이의 **GND 핀**에 연결

📸 **[]**

---

## 🔍 코드 구조 상세 설명

# domino4.sh - 도미노 형태의 LED 순차 점등 스크립트

Raspberry Pi의 GPIO 핀 4개를 제어하여 LED가 도미노처럼 **순차적으로 하나씩 점등**되도록 하는 Bash 스크립트입니다.  
각 LED는 1초 간격으로 ON 상태가 되며, 나머지 LED는 OFF 상태를 유지합니다.

---

## 🔧 코드 설명

### 🔹 1. 사용할 GPIO 핀 번호 설정

```bash

PINS=(17 18 27 22)
제어할 LED 수만큼 GPIO 핀 번호를 배열에 저장

배열 순서대로 LED가 순차 점등됨

예: GPIO 17 → GPIO 18 → GPIO 27 → GPIO 22

🔹 2. 종료 처리 함수 정의

cleanup() {
    for PIN in "${PINS[@]}"; do
        pinctrl set $PIN dl
    done
    echo "💡 모든 LED OFF (정리 완료)"
    exit 0
}
trap cleanup SIGINT SIGTERM
Ctrl+C 또는 종료 신호 발생 시 모든 핀을 OFF로 전환

trap 명령어로 SIGINT/SIGTERM을 감지해 cleanup 함수 호출

🔹 3. 초기화 – 핀을 출력 모드로 설정

for PIN in "${PINS[@]}"; do
    pinctrl set $PIN op
    pinctrl set $PIN dl
done
모든 핀을 출력 모드(op)로 설정하고 초기 상태는 OFF(dl)로 유지

🔹 4. 도미노 형태로 LED 점등 (메인 루프)

while true; do
    for PIN in "${PINS[@]}"; do
        for OTHER in "${PINS[@]}"; do
            if [ "$PIN" -eq "$OTHER" ]; then
                pinctrl set $OTHER dh
            else
                pinctrl set $OTHER dl
            fi
        done
        sleep 1
    done
done
무한 루프(while true)로 LED 순차 점등 반복

for PIN in ... : 점등할 LED 선택

for OTHER in ... : 모든 핀 순회하며 현재 점등할 핀(PIN)만 ON, 나머지는 OFF

각 상태 유지 시간: sleep 1 → 1초 간격

🔸 예시 동작 시퀀스
시간	점등된 GPIO 핀	LED 상태
1초	17	O X X X
2초	18	X O X X
3초	27	X X O X
4초	22	X X X O
5초~	17 (반복)	O X X X

```
## 🧾 결론 및 기대 효과

이 프로젝트는 **GPIO 순차 제어**, **반복 루프 제어**, **인터럽트 처리** 등  
기초 임베디드 개념을 실습하기에 적합합니다.

또한 `trap` 명령어와 `cleanup` 함수를 통해,  
스크립트 종료 시 **하드웨어 정리(clean shutdown)** 방법을 경험할 수 있습니다.
