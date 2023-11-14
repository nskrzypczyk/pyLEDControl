<div align="center">
    <img src="img/logo.svg" alt="Logo" />
  <p align="center">
    A ready-to-use platform for the deployment of 64x64 RGB-LED matrices.
  </p>
</div>
<br />

# pyLEDControl

Experimental project which is about connecting, configuring and managing LED-RGB-Matrices.
I needed a clock for my office room, so here I am.

## Prerequisites

- Raspi running **Raspbian** and ...
  - **Python3** (<=3.9.2), used for backend & matrix control
  - **Nodejs**, used for building the React frontend
  - **gcc**, used for building the official and custom C-bindings involved in this project
  - **make**

## First time setup
### Development Setup (Tested only on Linux systems)
For the first-time setup, please install the software-[prerequisites](#prerequisites).
After that please run the `setup_local_dev.sh` script which installs python dependencies, the rgb bindings as well as all custom C-libraries and npm modules.
After that, continue with [the setup of the settings.py](#setting-up-the-constants-settingspy)

### Deployment system (Raspi)
For setting up your Raspi deployment system, please run the `setup.sh` script, which is similar to the script used to set up the development machine. 
The main difference is that it creates a new `systemd` entry which ensures that pyLEDControl will be launched after booting up the system.
After that, continue with [the setup of the settings.py](#setting-up-the-constants-settingspy)

### Setting up the constants (settings.py) 
After the platform dependent first time installation of the environment, it is essential to copy the `settings.py.example`-file as a new file called `settings.py`. 
Open the newly created file and replace all `<REPLACE_ME>` placeholders the the respective values, e.g. regarding your location and Spotify metadata.
Depending on your system (development or deployment Raspi system), it is necessary to adjust the value `MODE` to either `ExecutionMode.REAL` or `ExecutionMode.EMULATION`.
Please proceed with [text](https://)

### Building the frontend and push it to your deployment system
pyLEDControl includes a React-based frontend which is used to e.g. change the current effect and brightness. Moreover it is capable of change effect related options as long as they are defined in the `.py`-counterpart. 
To build the frontend run `npm run build`. After this, copy the `build` directory to the same place on your Raspi system. This can be done e.g. via sftp or a remote VS Code connection to your Raspi.

## Participate

Feel free to participate in this project! Check out the corresponding [GitHub board](https://github.com/users/nskrzypczyk/projects/1) in which current problems as well as the project's progress are documented. If you find issues, whether it be code, setup et cetera, do not hesitate to create a new board entry :) 

## TODO

- [X] Creating base project / repo
  - [X] Set up `logging`
  - [X] ~~Learn how to TDD in Python (just btw)~~
- [X] Setting up test system using [RGBMatrixEmulator](https://github.com/ty-porter/RGBMatrixEmulator)
- [X] Create the controller
- [X] Set up flask server
- [X] Create the API
  - [X] Extend the API => Allow options for each effect individually
- [X] Create a Web-Frontend using React or Angular (or anything else...?)
- [X] Get a real Matrix
- [X] Wire everything up using a Raspi 3
- [X] Build a case out of a cardboard box?
- [X] Build spotify integration + effect
- [X] Shuffle Mode
- [X] DEMO (Simple [Rainbow] Waves for testing purposes)
- [ ] Document achievements
- [ ] Profit
