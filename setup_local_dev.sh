#!/usr/bin/env bash
# -*- coding: utf-8 -*-

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
make build-python PYTHON=$(command -v python3)
make install-python PYTHON=$(command -v python3)

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

echo "Preparing frontend dependencies"
cd $basedir/plc-frontend
npm i
sudo npm i -g serve
