#!/usb/bin/local/python3

import os

path = os.path.dirname(os.path.abspath(__file__))

# Get rid of weird trailing characters, and remove numbers
def ssidstrip(ssid):
    return ssid.rstrip().rstrip('N').rstrip('NYK').rstrip('0123456789')

# Get the universal configuration options, compile into list
universaldirectives = []
with open(path + '/universalconfig.conf') as universalconfig:
    for line in universalconfig.readlines():
        universaldirectives.append(line.split('=')[0])

# Get the channels for each AP
ssids = {}
with open('/root/csvs/current_aps.csv') as apfile:
    for line in apfile:
        line = line.split(',')
        ssid = ssidstrip(line[3])
        # This is a hack, but we have weird equipment.
        if ssid == 'GBS' or ssid == 'GREYCBB':
            ssid = 'GB'
        if ssid == 'CPOWELL':
            ssid = 'PB'
        #ssids.add(ssidlisting)
        channel = line[6]
        try:
            ssids[ssid].add(channel)
        except KeyError:
            ssids[ssid] = set()
            ssids[ssid].add(channel)
        #print(ssid, len(ssids[ssid]))

towers = [tower.replace('.cfg', '') for tower in os.listdir(path + '/configs')]
oldpath = path + '/configs/'
newpath = path + '/newconfigs/'

for tower in towers:
    print('Generating configuration for ' + tower)
    m510 = open(newpath + 'M5/' + tower + '10.cfg', 'w')
    m520 = open(newpath + 'M5/' + tower + '20.cfg', 'w')
    ac10 = open(newpath + 'AC/' + tower + '10.cfg', 'w')
    ac20 = open(newpath + 'AC/' + tower + '20.cfg', 'w')

    m510.write('radio.1.chanbw=10\n')
    m520.write('radio.1.chanbw=20\n')
    with open('/root/radioconfigurator/specifics.conf') as specificsFile:
        specifics = {}
        start = False
        for line in specificsFile.readlines():
            if line == 'END ' + tower + '\n':
                start = False
            if start:
                directive = line.split('=')[0]
                specifics[directive] = line.split('=')[1]
                if not directive == 'wireless.1.scan_list.channels':
                    m510.write(line)
                    m520.write(line)
                    ac10.write(line)
                    ac20.write(line)
            if line == 'BEGIN ' + tower + '\n':
                start = True
        # Get the channels for this AP.
    try:
        ssid = ssidstrip(specifics['wireless.1.ssid'])
    except KeyError:
        print(tower)
        raise
    channels = ','.join(ssids[ssid])
    print(channels)
    m510.write('wireless.1.scan_list.channels=' + channels + '\n')
    m520.write('wireless.1.scan_list.channels=' + channels + '\n')
    # Copy the the configuration from each of the files into each of the new configs.
    with open(oldpath + tower + '.cfg') as baseConfig:
        for line in baseConfig.readlines():
            line = line.rstrip()
            directive = line.split('=')[0]
            if directive in specifics:
                pass
            elif directive == 'radio.1.chanbw':
                pass
            else:
                m510.write(line + '\n')
                m520.write(line + '\n')
    m510.close()
    m520.close()
    # Now for the AC configurations.
    ac10.write('radio.1.chanbw=10\n')
    ac10.write('radio.1.ieee_mode=11acvht20\n')
    ac20.write('radio.1.chanbw=20\n')
    ac20.write('radio.1.ieee_mode=auto\n')
    with open('/root/radioconfigurator/universalacconfig.conf') as ACConfig:
       for line in ACConfig.readlines():
        line = line.rstrip()
        directive = line.split('=')[0]
        if directive == 'radio.1.chanbw':
            pass
        elif directive in specifics:
            pass
        elif directive == 'radio.1.ieee_mode':
            pass
        else:
            ac10.write(line + '\n')
            ac20.write(line + '\n')

    ac10.close()
    ac20.close()
