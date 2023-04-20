#!/usr/bin/env bash
# -*- coding: utf-8 -*-

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
    echo "Not running as root"
    exit
fi

PROJECT_NAME="pyLEDControl"
APP_NAME="run.py"

echo "Installing python requirements"
pip install -r requirements.txt
basedir=$(pwd)
cd ..

echo "Installing rgb matrix bindings"
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix

echo "Building rgb matrix bindings"
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)

echo "Creating autostart entry"
if [ -e "/etc/systemd/system/$PROJECT_NAME.service" ]; then
  rm -f /etc/systemd/system/$PROJECT_NAME.service
fi
echo "
[Unit]
Description=My Python Script
After=multi-user.target

[Service]
ExecStart= sh $basedir/systemd-entrypoint.sh

[Install]
WantedBy=multi-user.target
" >> /etc/systemd/system/$PROJECT_NAME.service

sudo systemctl enable $PROJECT_NAME.service

