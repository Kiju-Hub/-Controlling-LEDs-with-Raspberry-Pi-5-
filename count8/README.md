# 🧠 count8.sh – 3비트 LED 바이너리 카운터 (Raspberry Pi 5)

## 📝 개요

`count8.sh`는 Raspberry Pi의 GPIO 핀을 사용하여 3개의 LED에 0부터 7까지의 이진 카운팅을 표시하는 Bash 스크립트입니다.  
각 비트는 하나의 GPIO 핀에 매핑되며, 1초 간격으로 3비트 이진수(000~111)를 LED로 출력합니다.


Count: 0 → LED 상태: OFF OFF OFF  
Count: 1 → LED 상태: OFF OFF ON  
Count: 2 → LED 상태: OFF ON OFF  
...  
Count: 7 → LED 상태: ON ON ON  
  

---
## 🔴 시연 동영상
> https://youtu.be/L8tmN0GluMQ  코드 수정 전 설명 영상입니다. (while true, clean up 함수 추가 전) 
> https://youtu.be/oteNfEjwBZo  코드 수정 후 설명 영상입니다. (while true, clean up 함수 추가 후) 

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

📸 **![image](https://github.com/user-attachments/assets/a3ee14e2-00fb-4a51-bd81-8fb8d52e6c55)**


---

## 🔧 코드 설명

### 🔹 1. 사용할 GPIO 핀 번호 설정

```bash

🔹 0. #!/bin/bash  

🔹 1. PINS=(17 18 27)
3개의 LED를 제어하기 위해 GPIO 핀 번호를 배열로 저장

각각 3비트 이진수의 위치를 담당

GPIO 17: 최상위 비트 (MSB)

GPIO 18: 중간 비트

GPIO 27: 최하위 비트 (LSB)

🔹 2. 초기화 – 핀 모드 설정 및 끄기
for PIN in "${PINS[@]}"; do  
    pinctrl set $PIN op  
    pinctrl set $PIN dl  
done
각 핀을 출력 모드(op) 로 설정

초기 상태는 OFF(dl) 처리하여 LED 꺼짐 상태 유지

🔹 3. 무한 루프 실행
while true; do
    ...
done

스크립트가 종료될 때까지 무한히 반복

true는 항상 참이므로 내부 로직이 계속 실행됨

내부에서는 0~7까지 반복하여 LED 점등 상태를 순차적으로 변경

🔹 4. 0부터 7까지 반복
for ((i = 0; i < 8; i++)); do  
    echo "Count: $i"  
    ...
    sleep 1  
done
i를 0부터 7까지 1씩 증가시키며 반복

현재 숫자 i를 이진수로 변환하여 LED에 출력

각 상태는 1초 간격으로 변경됨

🔹 5. 비트를 추출해 각 핀에 출력

for j in {0..2}; do  
    BIT=$(( (i >> (2 - j)) & 1 ))

    if [ "$BIT" -eq 1 ]; then  
        pinctrl set ${PINS[j]} dh  # LED ON  
    else  
        pinctrl set ${PINS[j]} dl  # LED OFF  
    fi  
done
>>: 비트 오른쪽 시프트 연산자 (해당 자리 비트를 앞으로 가져옴)

& 1: 맨 끝 비트만 추출하여 0 또는 1 값 획득

추출된 값이 1이면 LED ON (dh), 0이면 LED OFF (dl)

🔸 예시: i = 5 일 때
i 값	이진수	GPIO 17 (MSB)	GPIO 18	GPIO 27 (LSB)
5	101	[ON	- OFF - ON]
dh: digital high → LED ON

dl: digital low → LED OFF

🔹 6. 종료 처리 (Ctrl+C )
cleanup() {
    echo ""
    for PIN in "${PINS[@]}"; do
        pinctrl set $PIN dl
    done
    exit 0
}
trap cleanup SIGINT SIGTERM
스크립트가 종료되면 모든 LED를 OFF로 처리하고 안전하게 종료

trap 명령어로 SIGINT (Ctrl+C) 또는 SIGTERM 신호를 감지하여 cleanup 실행
```

---
## ✅ 결론

이 스크립트는 단순한 LED 제어를 넘어서, 다음과 같은 핵심 개념들을 실제로 구현하며 배울 수 있도록 구성되어 있습니다:

- **이진수 표현**: 0부터 7까지의 값을 3비트 이진수로 변환하고, 이를 물리적인 LED 상태(ON/OFF)로 시각화합니다. 이를 통해 추상적인 이진 연산 개념을 실제 동작으로 확인할 수 있습니다.

- **GPIO 핀 제어**: Raspberry Pi의 GPIO 핀을 제어하여 LED를 끄고 켜는 기본적인 회로 제어 방법을 실습할 수 있습니다. 실제 핀 설정(op), 출력 제어(dh/dl) 등의 명령어를 통해 물리적 하드웨어와의 인터랙션을 체험할 수 있습니다.

- **무한 루프와 인터럽트 처리**: `while true`로 LED 상태를 반복 출력하면서도, `trap`과 `cleanup`을 통해 안전한 종료 처리를 구현합니다. 이는 시스템 프로그래밍에서 중요한 **신호 처리(Signal Handling)**의 실제 예시입니다.

