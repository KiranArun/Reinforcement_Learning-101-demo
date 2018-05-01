#!/bin/bash

apt update

apt install cmake
apt install ffmpeg

pip3 install gym
pip3 install gym[atari]

pip3 install 'opencv-contrib-python==3.3.0.9'