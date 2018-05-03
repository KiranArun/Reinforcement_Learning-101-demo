#!/bin/bash

echo 'Updating...'
apt update > /dev/null

echo 'Installing cmake...'
apt install cmake > /dev/null
echo 'Installing ffmpeg...'
apt install ffmpeg > /dev/null

echo 'Installing gym...'
pip3 -q install gym
pip3 -q install gym[atari]

echo 'Installing opencv...'
pip3 -q install 'opencv-contrib-python==3.3.0.9'