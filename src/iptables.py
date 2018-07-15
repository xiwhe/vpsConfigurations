#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 10:18:03 2018

@author: xiwhe
"""


import iptc
from time import sleep
from datetime import datetime
import os
import calendar


TRH_P_M = 16*1000*1000*1000

#TRAFFICPERDAY = 512*1000*1000

class IPtableManager:

    _ports = list()
    _cnt_setted = False
    _used_traffic = 0

    def __init__(self, supervise_ports):

        self._ports = supervise_ports

        mothrange = calendar.monthrange(datetime.today().year,datetime.today().month)[1]

        clear_all_rules = "iptables -F"
        if os.system(clear_all_rules):
            print("clear iptable failed")

#        with open("/tmp/ss_used", "rw+") as F:
#            self._used_traffic = f.read()

        traffic_limit = (TRH_P_M - self._used_traffic)/mothrange/self._ports.__len__()
        
        print "Data Transfer limit:", traffic_limit

        for port in self._ports:
            add_accept =  "iptables -A OUTPUT -p tcp -m quota --quota " + str(traffic_limit) + " -j ACCEPT --sport " + str(port)
            os.system(add_accept)
            add_drop = "iptables -A OUTPUT -p tcp -j DROP --sport " + str(port)
            os.system(add_drop)

        pass

    def start_supervising(self):
        while True:
            if datetime.today().hour is 23 and self.cnt_setted is False:
                print "start clear limitations"
                table = iptc.Table(iptc.Table.FILTER)
                chain = iptc.Chain(table, 'OUTPUT')
                chain.zero_counters()
                self.cnt_setted = True
            elif datetime.today().hour is 22 and self.cnt_setted is True:
                print "cleared limitations"
                self.cnt_setted = False
            else:
                print "wait for clear limitations"
            sleep(60*50)


def test():
    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        print "======================="
        print "Chain ", chain.name
        for rule in chain.rules:
            print "Rule", "proto:", rule.protocol, "src:", rule.src, "dst:", \
                  rule.dst, "in:", rule.in_interface, "out:", rule.out_interface,
            print "Matches:",
            for match in rule.matches:
                print match.name,
            print "Target:",
            print rule.target.name
    print "======================="

    table = iptc.Table(iptc.Table.FILTER)
    chain0 = iptc.Chain(table, 'OUTPUT')
    for rule in chain0.rules:
        for match in rule.matches:
            (packets, bytes) = rule.get_counters()
            print packets, bytes, match.name, match.sport


if __name__ == "__main__":
    manager = IPtableManager([50011,50022])
    manager.start_supervising()
    pass