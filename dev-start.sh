#!/usr/bin/env bash
# -*- coding: utf-8 -*-

cleanup () {
    echo "Cleaning up..."
    kill 0
}

trap cleanup EXIT INT TERM

script_dir="$(cd "$(dirname "$0")" && pwd -P)"
cd $script_dir/pyLEDControl
echo "DEV START: Starting backend"
./run.py &
echo "DEV START: Starting frontend"
serve -s $script_dir/plc-frontend/build -l 80
cd $script_dir/plc-frontend
sudo serve -s build -l 80 & 

wait
