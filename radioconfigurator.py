#!/usr/local/bin/python3

# Produces updated configuration files for radios.
# Sources of data include: 
#   /root/csvs/current_aps.csv
#       This is updated by /root/ubfreqs/doaps, via a cronjob
# 

import re

towers = [3Creeks, Awbrey, Chamber, Cinder, Cline, Crescent, Culver, EventCenter, FallRiver, Finley, Grey, Harrison, Hawkins, Hinkle, Hodgsen, Laidlaw, Lisa, Long, MATT, MWT, NorthMadras, Powell, Smolich, SpringRiver, SugarPine, Susans, Wick]

#the different things are 
#iptables.2.cmd # This is an iptables command that contains netconf.1.ip
#netconf.1.ip # management ip?
#netconf.3.ip # not management ip
#route.1.gateway
#wireless.1.scan_list.channels
#wireless.1.ssid
#wpasupplicant.profile.1.network.1.ssid

iptables.2.cmd = '-A FIREWALL -i eth0 --protocol 6 --dst ' + ApIp + '/32 -j DROP'

class apConfig:
    def __init__(self, mgmntip, notmgmntip, ssid):
        
    @property
    def mgmntip(self): # netconf.1.ip
        return self._mgmntip
    @mgmntip.setter
    def mgmntip(self, ip):
        self._mgmntip = ip
    @property
        def notmgmntip(self): # netconf.3.ip
        return self._notmgmntip
    @notgmtmnip.setter
    def notnmmntip(self, ip):
        self._notmgmntip = ip

    @property
    def gateway(self): # route.1.gateway
        return re.sub(r'\.\d{1,3}$', '1', self.mgmntip)

    @property
    def channels(self): # wireless.1.scan_list.channels
        return self._channels
    @channels.setter
    def channels(self, channels):
        self._channels = channels

    @property # wireless.1.ssid
    def ssid(self):
        return self._ssid
    @ssid.setter
    def ssid(self, ssid):
        self._ssid = ssid
    @property 
    def wpasupssid(self): # wpasupplicant.profile.1.network.ssid
        return self._ssid

    @property
    def iptablescmd(self): # iptables.2.cmd
        return '-A FIREWALL -i eth0 --protocol 6 --dst ' + self.mgmntip + '/32 -j DROP'

3Creeks = apConfig
3Creeks.

def makeConfigs():
    with open()
towers = {
'3Creeks':apConfig()
}


