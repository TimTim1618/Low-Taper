# Low-Taper
Software Engineering Laser Tag Project

to give permission use chmod +x run.bash

How to run code on oracle / bash
#---------------------------------------------------
How to install python3 - sudo apt update  ->  sudo apt install python3
How to install pip - sudo apt install python3-pip
How to install Tk - sudo apt update  ->  sudo apt install python3-tk
How to install psycopg2 - pip install psycopg2
How to install pillow - pip install pillow
How to install pygame - pip intall pygame

use command ./run.bash
          Press 1 and connect to local host. Then enter player and equipment id
udp server - python3 udpServer.py
          Press 1 and connect to the local host. It should now be listening for any inputs
#----------------------------------------------------------
Game commands
      F3 - Switch to play action screen
      F1 - Switch back to player screen
      F12 - Clear players 

#---------------------------------------------------
For running the Virtual machine:

###
Need to chage Host playerScreen.py to 127.0.0.1 instead of 192.168.0.42
###

Change the listening address to accept connections from external hosts:
Use command:
          sudo nano /etc/postgresql/13/main/postgresql.conf
Find the listen_addresses line and uncommment it and set it equal to '*'
          listen_addresss = '*'
Change pg_hba.conf file to allow connections from any IP address:
Use command:
          sudo nano /etc/postgresql/15/main/pg_hba.conf
Add a line at the bottom of the file like this:
          host    all             all             0.0.0.0/0            md5
Save these changes and restart PostgreSQL:
          sudo systemctl restart postgresql

Disable and firewalls preventing connections:
Install any updates:
          sudo apt update
Install ufw:
          sudo apt install ufw -y
Allow access to port 5432:
          sudo ufw allow 5432/tcp
You can check if ufw installed and the status by:         
          sudo ufw status
If you want to ensure that this all is working and your computer can connect to your virtual machine
Go to your command propmpt on your computer and enter in:
          telnet 10.0.2.15 5432
If your computer doesn't connect and show a blank screen, then something isn't working properly
If you do not have Telnet activated:
          Open control panel
          Go to Programs -> Turn windows features on or off
          Scroll down to check the box for Telnet Client
          CLick OK to install
          

I changed the network for my virtual machine in Oracle to a Bridged Adapter, and then chose the name as the Wifi that I was on. Then I got the IP address from entering the command "ip a" in the virtual machine and made sure it was the same as inthe playerScreen file in vscode. Then when I ran the code it would add the players in the screen to the database


Landon Ramsey
     GitHub - moblando
     Trello    -  landonramsey2
Marco Trujillo
      GitHub -  Marcot-10
      Trello    -  marcot96
Jay Guo
      GitHub  - jayguoo
      Trello     - jayguo10
Timothy Clelland
      GitHub  - TimTim1618
      Trello     - timothyclelland1
Tyler Pham
       GitHub - tyler1o9
       Trello    - Tylerpham24
