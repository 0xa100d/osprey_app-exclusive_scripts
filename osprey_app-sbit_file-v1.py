#!/usr/bin/python3.8

# LICENSE CREATIVE_COMMONS-ATTRIBUTION_SHARE_ALIKE
# https://creativecommons.org/licenses/by-sa/3.0/legalcode
# Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]

import sys
from sys import exit
import os.path
import json
import pyqrcode as qrcode
import io
import subprocess
import re

sources = """
Sources:
"""

version = 'sbit_file-v1'

if len(sys.argv) == 1:
	motd_help = """
Welcome to OSPREY.app's {0}
-----------------------------------------------------
LICENSE CREATIVE_COMMONS-ATTRIBUTION_SHARE_ALIKE
https://creativecommons.org/licenses/by-sa/3.0/legalcode
Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]

[REQS] 	
This is script is compiled to run on Ubuntu 16LTS and above with 
python3 support having net-tools and OpenSSL 1.1.1l installed.

[USAGE]
The purpose of this script is to generate the sha1 file and a subsequent
sbit file for whatever source file your choice may prevail.

To run this command, use start as the first parameter.
./osprey_app-{0} /path/to/file
"""
	print(motd_help.format(version))
	exit(0)

if len(sys.argv) <= 1:
        print('[ERROR] Missing file.')
        exit(1)
else:
        filepath = sys.argv[1]

if not os.path.isfile(filepath):
	print("[ERROR] Path is not a file: " + filepath)
	exit(1)

sbit_cmd = "/divideme.app.osprey.app/osprey_app-sbit-v4.py"

cmd = "sha1=$( openssl dgst -sha1 " + filepath + " | awk '{ print $NF }' > " + filepath + ".sha1 )"

try:
	sha1_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
	sha1 = sha1_proc.stdout.read().decode('utf-8').strip()
	sha1_proc.terminate()
except Exception as e:
	print('[ERROR] Unable to produce sha1. Error:' + str(e))
	exit(1)

if os.path.isfile(filepath + '.sha1'):
	print("** Successfully created file: " + filepath + '.sha1')

cmd = "sha1=$( cat " + filepath + ".sha1 ) && " + sbit_cmd + " $sha1 > " + filepath + ".sbit"

try:
	sbit_file_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
	sbit_file = sbit_file_proc.stdout.read().decode('utf-8').strip()
	sbit_file_proc.terminate()
except Exception as e:
	print('[ERROR] Unable to produce sbit. Error:' + str(e))
	exit(1)

if os.path.isfile(filepath + '.sbit'):
	print("** Successfully created file: " + filepath + '.sbit')

cmd = "sha1=$( cat " + filepath + ".sha1 ) && " + sbit_cmd + " -json $sha1 > " + filepath + ".sbit.json"

try:
	sbit_file_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
	sbit_file = sbit_file_proc.stdout.read().decode('utf-8').strip()
	sbit_file_proc.terminate()
except Exception as e:
	print('[ERROR] Unable to produce sbit.json. Error:' + str(e))
	exit(1)

if os.path.isfile(filepath + '.sbit.json'):
	print("** Successfully created file: " + filepath + '.sbit.json')

exit(0)