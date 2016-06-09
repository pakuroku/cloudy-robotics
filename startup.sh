#execute this bash script by typing "sudo bash startup.sh" to execute all python programs at once
cd elderlyrobot/robot/uart/
sudo python uart-socket.py &
sudo python degrees.py &
sudo python voltage.py &
cd ~
