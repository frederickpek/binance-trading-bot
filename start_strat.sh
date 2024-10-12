#!/bin/bash

# Start the strategy and save the PID
nohup python main.py > /dev/null 2>&1 &
PID=$!

# Echo out the PID and confirmation message
echo "Strategy started with PID: $PID"

