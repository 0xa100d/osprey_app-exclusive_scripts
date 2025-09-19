#!/bin/bash
# ospreyapp-bash_aliases.sh

# LICENSE CREATIVE_COMMONS-ATTRIBUTION_SHARE_ALIKE
# https://creativecommons.org/licenses/by-sa/3.0/legalcode
# Copyright (c) 2020-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]
# Copyright (c) 2021-2022 Nathaniel Steven Henry Brown [0+nate@purefame.com]
# Copyright (c) God
# Copyright (c) Jesus Heaven Christ
# Copyright (c) Perfection

#
#
# Version: b.v1.0.0

### Goes in ~/.bash_aliases or ~/.bashrc or ~/.zshrc
# source ~/osprey_app-bash_aliases.sh

### Run this to get a secret key generated
# python3.8 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

ospreyapp_divide_me_moment() {
		moment=$( python3.8 -c 'import datetime; import uuid; print(str(uuid.uuid4()) + " " + str(datetime.datetime.now()));' );
		ospreyapp_divide_me=$( ~/bin/osprey_app-divide_me-v5.py 1 "$moment"  )
		md5_sum=$( echo "$ospreyapp_divide_me" | md5sum ) 
		sha3_256=$( echo "$ospreyapp_divide_me" | openssl dgst -sha3-256 ) 
		echo "$ospreyapp_divide_me"
		echo "MD5SUM: $md5_sum"
		echo "SHA3-256: $sha3_256"
}

alias ospreyapp_moment="ospreyapp_divide_me_moment"
#alias moment="ospreyapp_moment"

ospreyapp_debyte() {
		debyte=$( python3.8 -c "print(int.from_bytes('$1'.encode('utf-8'), 'big'));" );
		echo "$debyte"
}

ospreyapp_divide_me_moment() {
		moment=$( python3.8 -c 'import datetime; import uuid; print(str(uuid.uuid4()) + " " + str(datetime.datetime.now()));' );
		ospreyapp_divide_me=$( ~/bin/osprey_app-divide_me-v8.py 1 "$moment"  )
		sha3_256=$( echo "$ospreyapp_divide_me" | openssl dgst -sha3-256 | awk '{print $NF}' ) 
		sha3_512=$( echo "$sha3_256" | openssl dgst -sha3-512 | awk '{print $NF}' ) 
		sha3_256_debyte=$( ospreyapp_debyte $sha3_256 )		
		sha3_512_debyte=$( ospreyapp_debyte $sha3_512 )		
		
		echo "$ospreyapp_divide_me"
		echo "$sha3_256"
		echo "$sha3_256_debyte"
		echo "$sha3_512"
		echo "$sha3_512_debyte"
}


m() {
	ospreyapp_divide_me_moment
}

ospreyapp_divide_me_string() {
		ospreyapp_divide_me=$( ~/bin/osprey_app-divide_me-v8.py 1 "$1"  )
		sha3_256=$( echo "$ospreyapp_divide_me" | openssl dgst -sha3-256 | awk '{print $NF}' ) 
		sha3_512=$( echo "$sha3_256" | openssl dgst -sha3-512 | awk '{print $NF}' ) 
		sha3_256_debyte=$( ospreyapp_debyte $sha3_256 )		
		sha3_512_debyte=$( ospreyapp_debyte $sha3_512 )		
		echo "$ospreyapp_divide_me"
		echo "$sha3_256"
		echo "$sha3_256_debyte"
		echo "$sha3_512"
		echo "$sha3_512_debyte"
}

ospreyapp_encode() {
		encode=$( python3.8 -c "print('$1'.encode('utf-8'));" );
		echo "$encode"
}

ospreyapp_debit() {
		debit=$( python3.8 -c "import binascii; hd=hex($1); print(binascii.unhexlify(hd[2:]));" );
		echo "$debit"
}

alias ospreyapp_sbit="~/bin/osprey_app-sbit-v5.py"
alias sbit="ospreyapp_sbit"

# s test && bits
s() {
	s=$( ospreyapp_sbit -sha2-256-hex "$1" )
	ospreyapp_sbit -sha2-256-hex "$1"
}

# f qwety && s $f && bit $s
# f=$( echo f ) && s=$( sbit -log $f) && bit $s
bit() {
	sbit -sha2-512 "$1"
}

# f test && s $f && bits $s
# f test && s=$( sbit -json $f ) && bits $s
alias bits="~/bin/osprey_app-bits-v1.py"

# bits() {
# 	echo $( bits "$1")
# }

ospreyapp_qrid() {
		~/bin/osprey_app-qrid-v1.py "$1"
}

ospreyapp_sbit_qrid() {
		~/bin/osprey_app-sbit_qrid-v2.py "$1"
}

ospreyapp_sbit_json() {
		~/bin/osprey_app-sbit_json-v2.py start
}

terminal() {
	ssh localhost
}

# f test && sbit -log "$f"
# f test && sbit -json "$f" && bits
f() {
	f=$( openssl dgst -sha256 $1 | awk '{print $NF}' ) 
	echo $f
}

# f2 test && sbit -log "$f2"
f2() {
	f2=$( file $1 )
	echo $f2
}

e() {
	ee=$(~/bin/osprey_app-e-v2.py) && ~/bin/osprey_app-e-v2.py "$ee"
}

ospreyapp_by() {
	~/bin/osprey_app-by-v1.py
}

by() {
	ospreyapp_by
}

# Sources:
# https://unix.stackexchange.com/questions/148975/check-md5sum-from-pipe
# https://stackoverflow.com/questions/3601515/how-to-check-if-a-variable-is-set-in-bash