#!/bin/bash

apt update

apt install cmake >/dev/null
apt install ffmpeg >/dev/null

pip3 install gym >/dev/null
pip3 install gym[atari] >/dev/null

pip3 install 'opencv-contrib-python==3.3.0.9' >/dev/null