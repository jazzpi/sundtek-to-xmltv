#!/usr/bin/env bash

GRABBER_DIR=$(dirname "$0")

while true
do
    "$GRABBER_DIR/sundtek-grab.py"
    # Uncomment the following line to upload the XML data file.
    #"$GRABBER_DIR/upload-epg-file.sh"
    sleep 1h
done
