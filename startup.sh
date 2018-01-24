#!/bin/bash

sudo su -c "useradd user1 -s /bin/bash"
echo user1:Password123 | sudo chpasswd
sudo usermod -aG sudo user1
