Patch Requirements
==================================================================================
- These scripts have been tested on ESXi 5.x HPE DL380 servers.

- As of 04/24/2017, the firmware.py script is provided for HPE servers only. As
  other vendors are needed then the firmware.py script will be updated.

- All firmware files should be placed in a directory named "firmware" at the same
  level as this README file.

- All software files should be placed in a directory named "software" at the same
  level as this README file.

- When downloading firmware files from vendor sites make sure you are downloading
  for your current ESXi version if using the patch.sh script (see chapter 4 below).


Firmware XML file
==================================================================================
Before setting up the firmware.xml you must determine the hardware model of your
servers.  This can be using the following command from the ESXi command prompt:

/bin/localcli hardware platform get | grep 'Product Name:'

Once you have determined the model then you will need to modify the firmware.py
script at line 107 along with creating the same elements under the <HPE> tag in the
firmware.xml.  The attributes of the element (name, component, version) must be
present.


Software XML file
==================================================================================
Before setting up the software.xml you must determine the hardware model of your
servers.  This can be using the following command from the ESXi command prompt:

/bin/localcli hardware platform get | grep 'Product Name:'

Once you have determined the model then you will need to modify the software.py
script at line 102 along with creating the same elements under the <HPE> tag in the
software.xml.  The attributes of the element (name, component, version) must be
present.

The software.xml file also provides the ability to executes commands by leveraging
the <cmd> element.  Commands are executed prior to software/updates within the
tag being installed.  


Patching Instructions
==================================================================================
The files included here must be placed on a web server which is accessible via HTTP
by the ESXi servers.  See 3rd and 4th items in chapter 1 above for firmware and 
software file locations.

This bundle includes a shell script named patch.sh in the "scripts" directory at
the same level as this README file. To patch an ESXi server follow these steps:

- SSH to ESXi server or login to the console via the DCUI
- change directory to /var/tmp
- wget/scp the patch.sh script
- execute the patch.sh script with the HTTP URL to the patch repository - see example

     /bin/sh /var/tmp/patch.sh http://www.esstokes1.com/vsphere6/patch/

- ESXi server will reboot when patching is complete


It is also possible to perform firmware and software updates manually by following
these steps:

- SSH to ESXi server or login to the console via the DCUI
- change directory to /var/tmp
- wget/scp the firmware.py and software.py scripts
- execute the firmware.py and software.py script with the HTTP URL to the patch 
  repository - see example

     /bin/python /var/tmp/firmware.py http://www.esstokes1.com/vsphere6/patch/
     /bin/python /var/tmp/software.py http://www.esstokes1.com/vsphere6/patch/

- ESXi server will need to be manually rebooted when patching is complete


Disclaimer
==================================================================================
The scripts/programs/workflows provided by Eric Stokes may be freely distributed,
provided that no charge above the cost of distribution is levied.  These items are
provided as is without any guarantees or warranty.  Although the author has 
attempted to find and correct any bugs, the author is not responsible for any
damages or losses of any kind caused by use or misuse.  The author is under no
obligation to provide support, service, corrections, or upgrades to these items.


==================================================================================
