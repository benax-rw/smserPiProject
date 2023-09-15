#!/bin/bash

# Function to check if the process is running
check_process() {
  local process_name="$1"
  if pgrep -x "$process_name" > /dev/null; then
    return 0 # Process is running
  else
    return 1 # Process is not running
  fi
}

# Define the process name
process_name="python3 /home/pi/sim900/smser_out.py"

# Check if the process is already running
if check_process "$process_name"; then
  echo "Process is already running."
else
  # Start the process if it's not running
  echo "Starting the process..."
  python3 /home/pi/sim900/smser_out.py &
fi

