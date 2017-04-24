#!/usr/bin/python

############################################################################
# Description: python script to perform firwmare updates on ESXi 5.x servers
# Author: Eric Stokes (@esstokes1)
# Date: April 24, 2017
############################################################################

# function to install the firmware component
def installfirmware( node ):
  f = open(logfile,"a+")

  # get the attributes from node passed into function
  filename = node.getAttribute("name")
  component = node.getAttribute("component")
  ver = node.getAttribute("version")
  # print "\t filename : %s" % filename
  # print "\t component : %s" % component
  # print "\t version : %s" % ver

  # to keep things clean we download each component
  # into its own directory under the ddir variable
  firmware = filename[0:filename.find(".")]
  firmware_dir = ddir +"/"+ firmware
  fileoutput = firmware_dir +"/"+ filename
  if not os.path.isdir(firmware_dir):
    os.mkdir(firmware_dir)
    f.write("creating download directory : %s \n" % firmware_dir)

  # download the file
  fileurl = url +"/firmware/"+ filename
  cmd = "wget -q "+ fileurl +" -O "+ fileoutput
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  # unzip if needed
  if (filename.find("zip") > 0):
    cmd = "cd "+ firmware_dir +" ; unzip -o "+ fileoutput
    f.write("%s \n" % cmd)
    output = os.popen(cmd).read()
    f.write("%s \n" % output)

  # make exe file executable
  cmd = "chmod +x "+ firmware_dir +"/"+ firmware +".*exe"
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  # run the firmware update
  cmd =  "cd "+ firmware_dir +" ; ./"+ firmware +".*exe -s -f"
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  # remove the contents of ddir
  cmd = "rm -fr "+ ddir +"/*"
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  f.close
  return;


#### MAIN ####

# import needed modules
import string
import os
import sys
import datetime
from xml.dom.minidom import parse
import xml.dom.minidom

# make sure the repository was passed on the command line
if len(sys.argv) < 2:
  print 'you must URL to patch downloads'
  print 'example - /var/tmp/firmware.py http://www.esstokes1.com/vsphere6/patch'
  sys.exit('')

# set the log file
logfile = "/var/tmp/firmware.log"

# log start time
f= open(logfile,"a+")
f.write("*********************************\n")
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write("started firmware update - %s \n" % now)

# get the URL passed on the command-line and
# set the location for the firmware.xml file
url = sys.argv[1]
xmlLocation = url +"/xml/firmware.xml"
f.write("using URL : %s \n" % url)

# create download directory if it doesnt exist
ddir = "/var/tmp/download"
if not os.path.isdir(ddir):
  os.mkdir(ddir)
  f.write("creating download directory : %s \n" % ddir)

# get hardware platform
cmd = "/bin/localcli hardware platform get | grep 'Product Name:' | awk -F':' '{print $2}' | sed 's/^ //g'"
hardware = os.popen(cmd).read()

# MODIFY THIS SECTION BASED ON YOUR HARDWARE TYPE
if (hardware.find("ProLiant") > -1):
  f.write("HPE server \n")
  hdw = "HPE"

  if (hardware.find("Gen9") > -1):
    f.write("Gen9 \n")
    model = "G9"

  elif (hardware.find("Gen8") > -1):
    f.write("Gen8 \n")
    model = "G8"

  elif (hardware.find("G7") > -1):
    f.write("G7 \n")
    model = "G7"

  else:
    f.write("HPE firmware updates for Gen9, Gen8, and G7 only \n")
    f.close
    sys.exit(0)

else:
  f.write("updates for HPE only right now \n")
  f.close
  sys.exit(0)

# wget the xml firmware updates
cmd = "wget -q "+ xmlLocation +" -O /var/tmp/firmware.xml"
f.write("%s \n" % cmd)
os.popen(cmd)
f.close

# open xml document using minidom parser
DOMTree = xml.dom.minidom.parse("/var/tmp/firmware.xml")
firmware = DOMTree.documentElement
for hdwElement in firmware.childNodes:
  hdw_tag = hdwElement.localName

  # check if the element name is "all"
  if (hdw_tag == "all"):  
    for fileElement in hdwElement.getElementsByTagName('file'):
      installfirmware(fileElement)

  # check if the element name is the same as our hardware type
  if (hdw_tag == hdw):
    for modelElement in hdwElement.childNodes:
      model_tag = modelElement.localName

      # check if the model is either "all" or our hardware model
      if (model_tag == "all") or (model_tag == model):
        for fileElement in modelElement.getElementsByTagName('file'):
          installfirmware(fileElement)

# log end time
f= open(logfile,"a+")
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write("completed firmware update - %s \n" % now)
f.write("*********************************\n")
f.close
