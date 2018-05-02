#!/bin/bash

echo 'Updating...'
apt update

echo 'Installing cmake...'
apt install -qq cmake
echo 'Installing ffmpeg...'
apt install -qq ffmpeg

echo 'Installing gym...'
pip3 -q install gym
pip3 -q install gym[atari]

echo 'Installing opencv...'
pip3 -q install 'opencv-contrib-python==3.3.0.9'