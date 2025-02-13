#make executable on with this command: chmod +x run.bash
#idk if it is the same for windows
#!/bin/bash
# run.bash

# Start the UDP server
python3 udpServer.py &
SERVER_PID=$!
echo "Started UDP server with PID: $SERVER_PID"

# wait 
sleep 2

# Start the player screen
python3 playerScreen.py

# terminate the UDP server
kill $SERVER_PID
echo "UDP server terminated."
