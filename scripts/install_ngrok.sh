#!/bin/bash

if ! [ -e /content/ngrok ]
then
    wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip > /dev/null 2>&1
    unzip -o ngrok-stable-linux-amd64.zip > /dev/null 2>&1
fi