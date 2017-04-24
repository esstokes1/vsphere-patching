#!/bin/sh

############################################################################
# Description: wrapper script to firmware / software updates
# Author: Eric Stokes (@esstokes1)
# Date: April 24, 2017
############################################################################

# make sure the directory exists before starting
mkdir -p /var/tmp/

# setup logging script
logfile=/var/tmp/patch.log
exec > $logfile 2>&1

# get URL from command line
URL=$1
echo "using URL ${URL}"

echo "downloading firmware.py script"
wget -q ${URL}/scripts/firmware.py -O /var/tmp/firmware.py

echo "running firmware script"
/bin/python /var/tmp/firmware.py ${URL} 

echo "downloading software.py script"
wget -q ${URL}/scripts/software.py -O /var/tmp/software.py

echo "running software script"
/bin/python /var/tmp/software.py ${URL} 

echo "rebooting"
reboot
