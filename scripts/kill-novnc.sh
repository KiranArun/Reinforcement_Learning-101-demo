#!/usr/bin/env bash

kill $(ps ax | grep websockify | grep -v grep | awk '{ print $1 }') >/dev/null
pkill ngrok
pkill vncserver
pkill Xvnc
pkill Xvfb
pkill x11vnc
ps aux | egrep "ngrok|vnc|Xvfb"
