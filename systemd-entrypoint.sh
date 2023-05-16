#!/usr/bin/env bash
# -*- coding: utf-8 -*-
script_dir="$(cd "$(dirname "$0")" && pwd -P)"
cd $script_dir/pyLEDControl
echo "ENTRYPOINT: Starting backend"
sudo ./run.py &
echo "ENTRYPOINT: Starting frontend"
# sudo serve -s $script_dir/plc-frontend/build -l 80
cd $script_dir/plc-frontend
sudo serve -s build -l 80
