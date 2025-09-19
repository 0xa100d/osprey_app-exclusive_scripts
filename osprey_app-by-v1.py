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
import uuid

sources = """
Sources:
https://stackoverflow.com/questions/3877623/can-you-have-variables-within-triple-quotes-if-so-how
"""

version = 'by-v1'

if len(sys.argv) > 1:
	motd_help = """
Welcome to OSPREY.app's {0}
-----------------------------------------------------
LICENSE CREATIVE_COMMONS-ATTRIBUTION_SHARE_ALIKE
https://creativecommons.org/licenses/by-sa/3.0/legalcode
Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]


[REQS] 	This is script is compiled to run on Ubuntu 16LTS and above with 
		python3.

The purpose of this script is to produce a bit based on the data on the machine
relative to an ipv6 and a moment calculated by uuid4 by way of a Qubit ~1 not ~0.

To run this command, run the command:
eg: ./osprey_app-{0}
"""
	print(motd_help.format(version))
	exit(0)

# by="Brown, Nathaniel Steven Henry" && sbit=$(/osprey_app-scripts/osprey_app-sbit-v6.py -sha2-256-hex "$by") && dm=$(/osprey_app-scripts/osprey_app-divide_me-v10.py $sbit "$by" | openssl dgst -sha3-256 | awk '{print $NF}') && echo $dm

cmd = "/osprey_app-scripts/osprey_app-sbit-v6.py -log-raw ipv6"
# print(cmd)
ipv6_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
ipv6 = ipv6_proc.stdout.read().decode('utf-8').strip()
ipv6_proc.terminate()

ipv6_uuid = str(uuid.uuid4())
cmd = "echo '" + ipv6 + " " + ipv6_uuid + "' | openssl dgst -sha256 | awk '{print $NF}'"
# print(cmd)
ipv6_sha2_256_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
ipv6_sha2_256 = ipv6_sha2_256_proc.stdout.read().decode('utf-8').strip()
ipv6_sha2_256_proc.terminate()

cmd = "/osprey_app-scripts/osprey_app-divide_me-v10.py '" + ipv6_sha2_256 + "' '" + ipv6 + "' | openssl dgst -sha3-256 | awk '{print $NF}'"
# print(cmd)
divide_me_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
divide_me = divide_me_proc.stdout.read().decode('utf-8').strip()
divide_me_proc.terminate()

divide_me_int = int.from_bytes(divide_me.encode('utf-8'), 'big')
print(divide_me_int, end="")
exit(0)
