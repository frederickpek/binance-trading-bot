#!/bin/bash

# Fetch the PID from the running process
PID=$(ps -ef | grep 'main.py' | grep -v grep | awk '{print $2}')

# If the PID exists, kill the process
if [ -n "$PID" ]; then
    kill -9 $PID
    echo "Strategy with PID: $PID has been stopped."
else
    echo "No strategy process found."
fi

