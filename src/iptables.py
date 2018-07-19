#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 10:18:03 2018

@author: xiwhe
"""


from time import sleep
from datetime import datetime
import os
import calendar
from threading import Timer


TRH_P_M = 16*1000*1000*1000

#TRAFFICPERDAY = 512*1000*1000

class IPtableManager:

    _ports = list()
    _used_traffic = 0


    def __init__(self, supervise_ports):

        self._ports = supervise_ports
 
        mothrange = calendar.monthrange(datetime.today().year,datetime.today().month)[1]

        clear_all_rules = "iptables -F"
        if os.system(clear_all_rules):
            print("clear iptable failed")

#        with open("/tmp/ss_used", "rw+") as F:
#            self._used_traffic = f.read()
#            print("used: ", self._used_traffic,flush=True)

        traffic_limit = (TRH_P_M - self._used_traffic)/mothrange/self._ports.__len__()
        
        print("Data Transfer limit:", traffic_limit, flush=True)

        for port in self._ports:
            add_accept =  "iptables -A OUTPUT -p tcp -m quota --quota " + str(traffic_limit) + " -j ACCEPT --sport " + str(port)
            os.system(add_accept)
            add_drop = "iptables -A OUTPUT -p tcp -j DROP --sport " + str(port)
            os.system(add_drop)

        pass


    def _reset_TRH_limit(self):
        print "start clear limitations"
        clear_accept =  "iptables -Z"
        os.system(clear_accept)
        timer = Timer(60*60*24, self._reset_TRH_limit)
        timer.start()
        

    def start_supervising(self):
        self._reset_TRH_limit()


if __name__ == "__main__":
    manager = IPtableManager([50002])
    manager.start_supervising()
    pass
