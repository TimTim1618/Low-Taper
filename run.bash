#!/bin/bash

echo "Select a network to connect to:"
echo "1. Localhost (127.0.0.1:7501)"
echo "2. Enter custom network"
read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    ip="127.0.0.1"
    port=7501
elif [ "$choice" = "2" ]; then
    read -p "Enter IP address: " ip
    read -p "Enter Port number: " port
else
    echo "Invalid choice, defaulting to localhost."
    ip="127.0.0.1"
    port=7501
fi

echo "Selected Network: $ip:$port"
python3 playerScreen.py "$ip" "$port"
