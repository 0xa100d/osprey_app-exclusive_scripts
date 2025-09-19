#!/usr/bin/python3.8

# LICENSE CREATIVE_COMMONS-ATTRIBUTION_SHARE_ALIKE
# https://creativecommons.org/licenses/by-sa/3.0/legalcode
# Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]

import re
import subprocess
import sys
from sys import exit
# import datetime.datetime
import time
import json

sources = """
Sources:
https://stackoverflow.com/questions/3877623/can-you-have-variables-within-triple-quotes-if-so-how
"""

version = 'bits-v1'

if len(sys.argv) == 1:
	motd_help = """
Welcome to OSPREY.app's {0}
-----------------------------------------------------
LICENSE CREATIVE_COMMONS-ATTRIBUTION_SHARE_ALIKE
https://creativecommons.org/licenses/by-sa/3.0/legalcode
Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]

[REQS] 	This is script is compiled to run on Ubuntu 16LTS and above with 
		python3.

The purpose of this script is to produce multiple bits per sbit.

To run this command, run the command:
eg: ./osprey_app-{0} "$s"
"""
	print(motd_help.format(version))
	exit(0)

bits_of_what = str(sys.argv[1])

cmd = '/divideme.app.osprey.app/osprey_app-sbit-v5.py -sha256 "' + bits_of_what + '"'
sbit_sha2_256_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
sbit_sha2_256 = sbit_sha2_256_proc.stdout.read().decode('utf-8').strip()
sbit_sha2_256_proc.terminate()

cmd = '/divideme.app.osprey.app/osprey_app-sbit-v5.py -sha512 "' + bits_of_what + '"'
sbit_sha2_512_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
sbit_sha2_512 = sbit_sha2_512_proc.stdout.read().decode('utf-8').strip()
sbit_sha2_512_proc.terminate()


print(sbit_sha2_256 + ";" + sbit_sha2_512, end="")
exit(0)
