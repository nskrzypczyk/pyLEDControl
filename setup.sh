#!/bin/bash
# -*- coding: utf-8 -*-

shopt -s expand_aliases
source ~/.bashrc
sudo chmod 666 ./*
echo $(python --version)
PROJECT_NAME="pyLEDControl"

script_path="$(readlink -f "${BASH_SOURCE[0]}")"
script_dir="${script_path%/*}"
basedir=$(pwd)

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

echo "Installing python requirements"
pip install -r requirements.txt
cd ..

echo "Installing rgb matrix bindings"
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git || echo "Repo already exists. Continuing..."
cd rpi-rgb-led-matrix

echo "Building rgb matrix bindings"
sudo make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)
sudo chmod 666 ./*

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
" >>/etc/systemd/system/$PROJECT_NAME.service

sudo systemctl enable $PROJECT_NAME.service

echo "Building C-Libraries"
cd "$script_dir/pyLEDControl/c_libs"
make all

# Check the exit status of the 'make' command
if [ $? -eq 0 ]; then
    echo "The 'make all' command was successful."
else
    echo "The 'make all' command failed."
    # You can add error handling or exit the script here if needed.
fi

#echo "Preparing frontend dependencies"
#cd $basedir/plc-frontend
#npm i
#sudo npm i -g serve
