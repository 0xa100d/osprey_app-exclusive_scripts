#!/usr/local/bin/python3.8

# MIT License
#
# Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

version = 'sbit-v5'

motd_help = """
Welcome to OSPREY.app's {0}
-----------------------------------------------------
MIT License

Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[REQS] 	This is script is compiled to run on Ubuntu 16LTS and above with 
		python3 support having net-tools and OpenSSL 1.1.1l installed.

The purpose of this script is to find the encrpyted bit for a color in a hexadecimal 
format without the # as found in HTML and CSS.

To run this command, there are three options:

1. Simply type a hex color as the first parameter.
eg: ./osprey_app-{0} FFFFFF

2. Use hw keyword value to indicate that you would like to use the hardware address as 
typically found with ifconfig on Ubuntu with net-tools.
eg: ./osprey_app-{0} hw

3. Use any string with quotes if it has any white space
eg: ./osprey_app-{0} "Nathaniel Steven Henry Brown <nate@purefame.com>"

4. Use either ipv4 or ipv6 keywords to indicate that you would like to use the ip address 
associated to the machine to convert and then envrypt to a bit.
eg: ./osprey_app-{0} ipv6

Optionally you may pre-fix this first command with a digest format on 
how you would like to see the data of the sbit.

-sha2-256
-sha2-256-hex
-sha2-512
-sha2-512-hex
-sha3-256 (default)
-sha3-256-hex
-sha3-512
-sha3-512-hex
-log
-json

eg: ./osprey_app-{0} -sha3-256-hex 1c6a8cf8f033

In order to get a sum of the MOTD of this script, run this command:
eg: s=$( ./osprey_app-{0} | openssl dgst -sha256 ) && ./osprey_app-{0} "$s"
"""
if len(sys.argv) == 1:
	print(motd_help.format(version))
	exit(0)

if len(sys.argv) == 2:
	s = str(sys.argv[1])
	dgst_input = '-sha3-256'
else:
	s = str(sys.argv[2])
	dgst_input = str(sys.argv[1])

if len(s) == 0:
	print(motd_help.format(version))
	exit(0)


if s == 'hw':
	cmd = "ifconfig"
	ifconfig_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
	ifconfig = ifconfig_proc.stdout.read().decode('utf-8').strip()
	ifconfig_proc.terminate()
	# print(ifconfig)
	hw_matches = re.findall(r'.*ether\s([0-9a-f\:]+).*', ifconfig)
	if not hw_matches:
		hw_matches = re.findall(r'.*HWaddr\s([0-9a-f\:]+)', ifconfig)
		if hw_matches:
			hw_match = hw_matches[0]
		else: 
			print('Hardware ID Not found.')
			exit(0)
	else:
		hw_match = hw_matches[0]

	s_equation = str(int.from_bytes(hw_match.encode('utf-8'), 'big')).replace('0x', '')
elif s == 'ipv4':
	cmd = "ifconfig"
	ifconfig_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
	ifconfig = ifconfig_proc.stdout.read().decode('utf-8').strip()
	ifconfig_proc.terminate()
	# print(ifconfig)
	ip_matches = re.findall(r'.*inet\s([0-9\.]+).*', ifconfig)
	if not ip_matches:
		ip_matches = re.findall(r'.*inet addr:([0-9\.]+)', ifconfig)
		if ip_matches:
			ip_match = ip_matches[0]
		else: 
			print('IPv4 ID Not found.')
			exit(0)
	else:
		ip_match = ip_matches[0]

	s_equation = str(int.from_bytes(ip_match.replace('.', '-').encode('utf-8'), 'big')).replace('0x', '')
elif s == 'ipv6':
	cmd = "ifconfig"
	ifconfig_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
	ifconfig = ifconfig_proc.stdout.read().decode('utf-8').strip()
	ifconfig_proc.terminate()
	ip_matches = re.findall(r'.*inet6 addr:\s([^\s]+)', ifconfig)
	# print(ifconfig)
	if not ip_matches:
		ip_matches = re.findall(r'.*inet6\s([^\s]+).*', ifconfig)
		if ip_matches:
			ip_match = ip_matches[0]
		else: 
			print('IPv6 ID Not found.')
			exit(0)
	else:
		ip_match = ip_matches[0]

	s_equation = str(int.from_bytes(ip_match.encode('utf-8'), 'big')).replace('0x', '')
elif re.match(r'^[0-9\.]+$', s):
	s_equation = str(s)
elif re.match(r'^[a-fA-F0-9\-\:]+$', s):
	s_equation = str(int.from_bytes(s.encode('utf-8'), 'big')).replace('0x', '')
else:
	s_equation = s

cmd = '~/bin/osprey_app-divide_me-v9.py 1 "' + re.sub(r'"', r'\"', re.sub(r"\n", "  ", s_equation)) + '"'
# print(cmd)
dm = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
dm_log = dm.stdout.read().decode('utf-8').strip()
dm.terminate()

# eg = "1.639629710710792858755732690E-47 Hz (p.v8.0.0) [1 ÷ We did it! Woohoo ;)]"
# print(eg)
# 082fd134ceb4f6e8ff8d65a227e57e6d2ecaffe38a97aa88c4bc3ba3985d3
# print(dm_log)
# exit(1)
hz_matches = re.match(r"(((\d+)\.(\d+))([E]?[-+]?)(\d+))\sHz", dm_log)
# print(hz_matches[3])
# exit(1)

if not hz_matches:
	print("[ERROR] Hz not found")
	exit(1)

head = hz_matches[3] + '-' + hex(int(hz_matches[4])).replace('0x', '')
tail = hex(int(hz_matches[6])).replace('0x', '')
genr_plain = hz_matches[1]
# print(head)

coin = str(head) + '-' + hz_matches[5] + str(tail) + 'Hz'

# print(coin)

# exit(0)
# 54c4518b8a1f126d47d14d2E-2f

coin_value = int.from_bytes(coin.encode('utf-8'), 'big')

# print(coin_value)
# 21887118876010347795183703788327694437338207134076983283882472038

s_matches = re.match(r"((\d+\.\d+)([E]?[-+]?)(\d+))\sHz( \(p\.v\d+\.\d+\.\d+\) (\[.*\]))", dm_log)

# print(s_matches[6])
bit = s_matches[6].replace('1 ÷ ', '').replace('[', '').replace(']', '')

sbit_log = coin + ' ' + version + ' ' + bit

if dgst_input == '-log':
	print(sbit_log)
	exit(0)

dgst_hex = False
json_fmt = False

if dgst_input == '-sha3-256-hex':
	dgst_input = '-sha3-256'
	dgst_hex = True 
elif dgst_input == '-sha3-512':
	 dgst = '-sha3-512'
	 dgst_hex = False
elif dgst_input == '-sha3-512-hex':
	dgst_input = '-sha3-512'
	dgst_hex = True 
elif dgst_input == '-sha2-256':
	 dgst_input = '-sha256'
	 dgst_hex = False
elif dgst_input == '-sha2-256-hex':
	dgst_input = '-sha256'
	dgst_hex = True 
elif dgst_input == '-sha2-512':
	 dgst_input = '-sha512'
	 dgst_hex = False
elif dgst_input == '-sha2-512-hex':
	dgst_input = '-sha512'
	dgst_hex = True 
elif dgst_input == '-json':
	dgst_input = '-sha256'
	json_fmt = True 
else:
	dgst_input = '-sha3-256'
	dgst_hex = False 

cmd = "echo '" + str(sbit_log) + "' | openssl dgst " + dgst_input + " | awk '{print $NF}'"
sbit_sum_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, executable="/bin/bash")
sbit_sum = sbit_sum_proc.stdout.read().decode('utf-8').strip()
sbit_sum_proc.terminate()
sbit = int.from_bytes(sbit_sum.encode('utf-8'), 'big')

if json_fmt:
	json_data = {
		's': s,
		'log': sbit_log,
		'sbit': sbit,
		'sbit_hex': sbit_sum,
		'genr_hex_si': coin,
		'genr_hex': coin.replace('Hz', ''),
		'genr': genr_plain,
		'genr_si': genr_plain + ' Hz',
		'version': version,
	}
	json_string = json.dumps(json_data, default = str)
	print(json_string, end="")
	exit(0)

if dgst_hex == True:
	print(sbit_sum, end="")
	exit(0)

print(sbit, end="")
exit(0)