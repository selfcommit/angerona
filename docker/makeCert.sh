#!/bin/bash
if [ ! -f /opt/angerona/angerona.key ]
then
	openssl req -x509 -nodes -days 365 -config /opt/angerona/angerona-ossl.cnf -newkey rsa:2048 -keyout /opt/angerona/angerona.key -out /opt/angerona/angerona.crt
	kill -HUP 1
fi
sleep 1
