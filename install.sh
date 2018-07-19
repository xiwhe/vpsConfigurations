#!/bin/bash

cp src/iptables.py /usr/bin/
cp systemd/ACL.service /lib/systemd/system/
cp systemd/shadowsock.service /lib/systemd/system/

systemctl enable /lib/systemd/system/ACL.service
systemctl enable /lib/systemd/system/shadowsock.service
