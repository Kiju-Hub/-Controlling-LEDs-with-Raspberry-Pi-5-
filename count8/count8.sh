#!/bin/bash

# 사용할 GPIO 핀 번호 (가장 큰 비트부터)
PINS=(17 18 27)


# 종료 시 실행될 정리 함수
cleanup() {
    echo "💡 모든 LED OFF (정리 완료)"
    for PIN in "${PINS[@]}"; do
        pinctrl set $PIN dl
    done
    exit 0
}

# 종료 시 cleanup 함수 호출하도록 설정
trap cleanup SIGINT SIGTERM

# 초기화: 핀 출력 모드로 설정 + 모두 끄기
for PIN in "${PINS[@]}"; do
    pinctrl set $PIN op
    pinctrl set $PIN dl
done

# 무한 루프
while true; do
    # 0부터 7까지 반복 (3비트 이진수)
    for ((i = 0; i < 8; i++)); do
        echo "Count: $i"

        for j in {0..2}; do
            BIT=$(( (i >> (2 - j)) & 1 ))

            if [ "$BIT" -eq 1 ]; then
                pinctrl set ${PINS[j]} dh  # LED ON
            else
                pinctrl set ${PINS[j]} dl  # LED OFF
            fi
        done

        sleep 1
    done
done

