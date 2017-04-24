#!/usr/bin/python

############################################################################
# Description: python script to perform firwmare updates on ESXi 5.x servers
# Author: Eric Stokes (@esstokes1)
# Date: April 24, 2017
############################################################################

# function to execute command
def runCmdFromXml( node ):
  f = open(logfile,"a+")

  cmd = node.childNodes[0].data
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  f.close()
  return;

# function to install the software component
def installupdate( node ):
  f = open(logfile,"a+")
  
  filename = node.getAttribute("name")
  component = node.getAttribute("component")
  ver = node.getAttribute("version")
  # print "\t filename : %s" % filename
  # print "\t component : %s" % component
  # print "\t version : %s" % ver

  # download update file
  fileoutput = ddir +"/"+ filename
  fileurl = url +"/software/"+ filename
  cmd = "wget -q "+ fileurl +" -O "+ fileoutput
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  # install the update 
  # files with zip extension use -d flag
  # files with vib extension use -v flag
  flag = "-d"
  if (filename.find("vib") > -1):
    flag = "-v"
  cmd = "/bin/localcli software vib install "+ flag +" "+ fileoutput +" --force"
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  # remove the contents of ddir
  cmd = "rm -fr "+ ddir +"/*"
  f.write("%s \n" % cmd)
  output = os.popen(cmd).read()
  f.write("%s \n" % output)

  f.close()
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
  print 'example - /var/tmp/software.py http://www.estokes1.com/vsphere6/patch'
  sys.exit('')

# set the log file
logfile = "/store/instlog/software.log"

# log start time
f = open(logfile,"a+")
f.write("*********************************\n")
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write("started software update - %s \n" % now)

# get the URL passed on the command-line and
# set the location for the software.xml file
url = sys.argv[1]
xmlLocation = url +"/xml/software.xml"
f.write("using URL : %s \n" % url)

# create download directory if it doesnt exist
ddir = "/var/tmp/download"
if not os.path.isdir(ddir):
  os.mkdir(ddir)
  f.write("creating download directory : %s \n" % ddir)

# get hardware platform
cmd = "/bin/localcli hardware platform get | grep 'Product Name:' | awk -F':' '{print $2}' | sed 's/^ //g'"
hardware = os.popen(cmd).read()

# MODIFY THIS SECTION BASED ON YOUR HARDWARE
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
    f.write("HPE updates for Gen9, Gen8, and G7 only \n")
    f.close()
    sys.exit(0)

else:
  f.write("updates for HPE only right now \n")
  f.close()
  sys.exit(0)

# wget the xml for software updates
cmd = "wget "+ xmlLocation +" -O /var/tmp/software.xml"
f.write("%s \n" % cmd)
os.popen(cmd)
f.close()

# open xml document using minidom parser
DOMTree = xml.dom.minidom.parse("/var/tmp/software.xml")
software = DOMTree.documentElement

# check each child directly under the root node
for hdwElement in software.childNodes:
  hdw_tag = hdwElement.localName

  # check if the element name is "all" 
  if (hdw_tag == "all"):
  
    # execute all commands given in the xml file
    for cmdElement in hdwElement.getElementsByTagName('cmd'):
      runCmdFromXml(cmdElement)

    # install all files given in the xml file
    for fileElement in hdwElement.getElementsByTagName('file'):
      installupdate(fileElement)

  # check if the element name is the same as our hardware type
  if (hdw_tag == hdw):
    for modelElement in hdwElement.childNodes:
      model_tag = modelElement.localName

      # check if the model is either "all" or our hardware model
      if (model_tag == "all") or (model_tag == model):

        # execute all commands given in the xml file
        for cmdElement in modelElement.getElementsByTagName('cmd'):
          runCmdFromXml(cmdElement)

        # install all files given in the xml file
        for fileElement in modelElement.getElementsByTagName('file'):
          installupdate(fileElement)

# log end time
f = open(logfile,"a+")
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
f.write("completed software update - %s \n" % now)
f.write("*********************************\n")
f.close()
