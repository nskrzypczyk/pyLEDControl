#!/usr/bin/env bash
# -*- coding: utf-8 -*-
script_dir="$(cd "$(dirname "$0")" && pwd -P)"
cd $script_dir/pyLEDControl
sudo ./run.py