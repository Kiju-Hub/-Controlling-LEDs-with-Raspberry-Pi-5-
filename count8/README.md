# 🧠 count8.sh – 3비트 LED 바이너리 카운터 (Raspberry Pi 5)

This project demonstrates how to control 3 LEDs connected to GPIO pins on a Raspberry Pi 5 to display binary numbers from **0 to 7**. Each second, a number is incremented and converted to 3-bit binary, with each bit controlling one LED.

---
## 🔴 시연 동영상
> 

---  
 

## 📌 프로젝트 개요

- **목적**: Raspberry Pi 5의 GPIO 핀을 활용해 **LED를 이진수(3비트)로 표현**
- **핵심 기능**:
  - 0부터 7까지 숫자를 1초 간격으로 증가
  - 숫자를 3비트 이진수로 변환
  - 각 비트를 LED에 매핑하여 ON/OFF 제어

---

## ⚙️ 기술 스택 및 환경

| 항목             | 내용                       |
|------------------|----------------------------|
| Platform         | Raspberry Pi 5 (64-bit)    |
| OS               | Raspberry Pi OS (Debian 기반) |
| Language         | Bash Shell Script          |
| GPIO Control     | `pinctrl` CLI 유틸리티     |

> ※ `pinctrl`은 Raspberry Pi 5에서 GPIO 제어용으로 사용되는 툴입니다.

---

## 💡 회로 구성도

- **GPIO 17** → LED (최상위 비트)
- **GPIO 18** → LED (중간 비트)
- **GPIO 27** → LED (최하위 비트)

- LED 각각에는 **저항**을 직렬로 연결
- 공통 GND는 라즈베리파이의 **GND 핀**

📸 **[추후 업로드 예정 – `images/circuit.png`]**


---


## 🔍 코드 구조 상세 설명

### 🔹 1. 사용할 GPIO 핀 번호 설정

PINS=(17 18 27)

- 3개의 LED를 제어하기 위해 GPIO 핀 번호를 배열로 저장
- 각각 3비트 이진수의 위치를 담당
  - GPIO 17: 최상위 비트 (MSB)
  - GPIO 18: 중간 비트
  - GPIO 27: 최하위 비트 (LSB)

---

### 🔹 2. 초기화 – 핀 모드 설정 및 끄기

for PIN in "${PINS[@]}"; do  
    pinctrl set $PIN op  
    pinctrl set $PIN dl  
done

- 각 핀을 출력 모드로 설정 (op)
- 초기 상태는 OFF (dl)

---

### 🔹 3. 0부터 7까지 반복

for ((i = 0; i < 8; i++)); do  
    echo "Count: $i"  
    ...  
    sleep 1  
done

- 1초 간격으로 `i`를 증가시키며 0~7까지 반복
- 숫자를 이진수로 변환해 LED로 출력

---

### 🔹 4. 비트를 추출해 각 핀에 출력

for j in {0..2}; do  
    BIT=$(( (i >> (2 - j)) & 1 ))

    if [ "$BIT" -eq 1 ]; then  
        pinctrl set ${PINS[j]} dh  # LED ON  
    else  
        pinctrl set ${PINS[j]} dl  # LED OFF  
    fi  
done

- `>>`: 오른쪽 비트 쉬프트  
- `& 1`: 해당 자리의 비트만 추출 (0 또는 1)

| 예시 (i = 5) | 이진수 | GPIO 상태            |
|-------------|--------|-----------------------|
| `5`         | `101`  | 17: ON, 18: OFF, 27: ON |

- `dh`: digital high → LED ON  
- `dl`: digital low → LED OFF

---

### 🔹 5. 모든 LED 끄기 (종료 시)

for PIN in "${PINS[@]}"; do  
    pinctrl set $PIN dl  
done

- 스크립트 종료 시 LED를 모두 꺼줌
- 깔끔한 종료 처리

### 1. GPIO 핀 초기화
```bash
for PIN in "${PINS[@]}"; do
    pinctrl set $PIN op  # 출력 모드 설정
    pinctrl set $PIN dl  # 초기에는 OFF
done
