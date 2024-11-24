#!/bin/bash

ctlScript="/opt/aws/aws-otel-collector/bin/aws-otel-collector-ctl"
status=$(sudo $ctlScript -a status | python3 -c "import sys, json; print(json.load(sys.stdin)['status'])")

if [ "$status" == "running" ]; then
    echo "AWSOTelCollector is running."
else
    echo "AWSOTelCollector is not running. Starting the collector agent"
    sudo $ctlScript -a start
fi