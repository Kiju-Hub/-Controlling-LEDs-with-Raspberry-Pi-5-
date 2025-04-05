#!/bin/bash

PINS=(17 18 27 22)


# 종료 시 모든 핀 끄기
cleanup() {
    for PIN in "${PINS[@]}"; do
        pinctrl set $PIN dl
    done
    echo "💡 모든 LED OFF (정리 완료)"
    exit 0
}

# SIGINT (Ctrl+C) 또는 SIGTERM 시 cleanup 호출
trap cleanup SIGINT SIGTERM


# 핀을 출력 모드로 설정
for PIN in "${PINS[@]}"; do
    pinctrl set $PIN op
    pinctrl set $PIN dl  # 처음엔 꺼두기
done

# 도미노 LED 무한 루프
while true; do
    for PIN in "${PINS[@]}"; do
        for OTHER in "${PINS[@]}"; do
            if [ "$PIN" -eq "$OTHER" ]; then
                pinctrl set $OTHER dh  # 해당 LED 켜기
            else
                pinctrl set $OTHER dl  # 나머지는 끄기
            fi
        done
        sleep 1
    done
done
