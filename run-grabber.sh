#!/usr/bin/env bash

GRABBER_DIR=$(dirname "$0")

while true
do
    "$GRABBER_DIR/sundtek-grab.py"
    sleep 1h
done
