#!/usr/bin/env bash
# -*- coding: utf-8 -*-

git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)
