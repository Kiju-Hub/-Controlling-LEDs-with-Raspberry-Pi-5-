# 🔁 domino4.sh – 도미노 LED 점등 효과 (Raspberry Pi 5)

이 프로젝트는 Raspberry Pi 5의 GPIO 핀에 연결된 4개의 LED를 활용하여  
LED가 순차적으로 켜지고 꺼지는 **도미노 효과**를 구현합니다.  
각 LED는 1초 간격으로 하나씩 켜지고, 나머지 LED는 꺼지는 방식으로 반복됩니다.

---

## 🔴 시연 동영상  
> 추후 업로드 예정

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

📸 **[추후 업로드 예정 – `images/circuit_domino.png`]**

---

## 🔍 코드 구조 상세 설명

### 🔹 1. 사용할 GPIO 핀 번호 설정

```bash
PINS=(17 18 27)
3개의 LED를 제어하기 위해 GPIO 핀 번호를 배열로 저장

각각 3비트 이진수의 위치를 담당

GPIO 17: 최상위 비트

GPIO 18: 중간 비트

GPIO 27: 최하위 비트

🔹 2. 초기화 – 핀 모드 설정 및 끄기
bash
복사
편집
for PIN in "${PINS[@]}"; do
    pinctrl set $PIN op
    pinctrl set $PIN dl
done
각 핀을 출력 모드(op)로 설정

초기 상태는 모두 OFF (dl)

🔹 3. 0부터 7까지 반복
bash
복사
편집
for ((i = 0; i < 8; i++)); do
    echo "Count: $i"
    ...
    sleep 1
done
i를 0부터 7까지 1초 간격으로 증가

숫자를 3비트 이진수로 변환 후 LED로 표현

🔹 4. 비트를 추출해 각 핀에 출력
bash
복사
편집
for j in {0..2}; do
    BIT=$(( (i >> (2 - j)) & 1 ))

    if [ "$BIT" -eq 1 ]; then  
        pinctrl set ${PINS[j]} dh  # LED ON  
    else  
        pinctrl set ${PINS[j]} dl  # LED OFF  
    fi  
done
>>: 오른쪽 비트 쉬프트 → 2-j만큼 밀어서 원하는 비트를 앞으로

& 1: 마지막 비트가 1인지 0인지 판별

해당 결과에 따라 dh(ON) 또는 dl(OFF) 설정

예시 (i = 5)	이진수	GPIO 상태
5	101	17: ON, 18: OFF, 27: ON
dh: digital high → LED ON

dl: digital low → LED OFF

🔹 5. 모든 LED 끄기 (종료 시)
bash
복사
편집
for PIN in "${PINS[@]}"; do
    pinctrl set $PIN dl
done
스크립트 종료 시 모든 LED OFF

깨끗한 종료 처리로 회로 보호


## 🧾 결론 및 기대 효과

이 프로젝트는 **GPIO 순차 제어**, **반복 루프 제어**, **인터럽트 처리** 등  
기초 임베디드 개념을 실습하기에 적합합니다.

또한 `trap` 명령어와 `cleanup` 함수를 통해,  
스크립트 종료 시 **하드웨어 정리(clean shutdown)** 방법을 경험할 수 있습니다.
