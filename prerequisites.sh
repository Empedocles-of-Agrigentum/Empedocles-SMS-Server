#!/usr/bin/env bash
# This is prerequisites installation script for CentOS 6.5 x64

# Install Python
yum -y install python

# Install PySerial library for serial port handling
wget https://pypi.python.org/packages/source/p/pyserial/pyserial-2.7.tar.gz#md5=794506184df83ef2290de0d18803dd11
tar -xzf pyserial-2.7.tar.gz
cd pyserial-2.7
python setup.py install

# Install smspdu library for transcoding SMS-messages to PDU and vice versa
wget https://pypi.python.org/packages/source/s/smspdu/smspdu-1.0.tar.gz#md5=d350d9923c9a943c8e8af6825a41f529
tar -xzf smspdu-1.0.tar.gz
cd smspdu-1.0
python setup.py install

# Install Twisted
yum -y install python-twisted

# Create folder and files for logging
mkdir /var/log/sms_server
touch /var/log/sms_server/log
touch /var/log/sms_server/err
