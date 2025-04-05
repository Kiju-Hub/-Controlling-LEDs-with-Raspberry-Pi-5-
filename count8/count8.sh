#!/bin/bash

# 사용할 GPIO 핀 번호 (가장 큰 비트부터)
PINS=(17 18 27)

# 초기화: 핀 출력 모드로 설정 + 모두 끄기
for PIN in "${PINS[@]}"; do
    pinctrl set $PIN op
    pinctrl set $PIN dl
done

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

# 끝나고 모든 LED 끄기
for PIN in "${PINS[@]}"; do
    pinctrl set $PIN dl
done
