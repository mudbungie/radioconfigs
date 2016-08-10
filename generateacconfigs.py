#!/usb/bin/local/python3

import os

# Get rid of weird trailing characters, and remove numbers
def ssidstrip(ssid):
    return ''.join([c for c in ssid.rstrip('N').\
        rstrip('NYK') if not c.isdigit()])

# Get the universal configuration options, compile into list
universaldirectives = []
with open('/root/radioconfigurator/universalconfig.conf', 'r') as universalconfig:
    for line in universalconfig.readlines():
        universaldirectives.append(line.split('=')[0])

# Get the channels for each AP
ssids = {}
with open('/root/csvs/current_aps.csv', 'r') as apfile:
    for line in apfile:
        line = line.split(',')
        ssid = ssidstrip(line[3])
        #ssids.add(ssidlisting)
        channel = line[6]
        try:
            ssids[ssid].add(channel)
        except KeyError:
            ssids[ssid] = set()
            ssids[ssid].add(channel)


# Look at each file, get all the configuration options that aren't in the universal.
with open('/root/radioconfigurator/specifics.conf', 'w') as output:
    for tower in os.listdir('/root/radioconfigurator/configs'):
        towername = tower.replace('.cfg', '')
        output.write('BEGIN ' + towername + '\n')
        with open('/root/radioconfigurator/configs/' + tower, 'r') as towerconfig:
            for line in towerconfig.readlines():
                line = line.rstrip()
                directive = line.split('=')[0]
                if directive == 'wireless.1.ssid':
                    output.write(line + '\n')

                    # Compile and write the channels line.
                    channels = ssids[ssidstrip(line.split('=')[1])]
                    channels = ','.join(channels)
                    channels = 'wireless.1.scan_list.channels=' + channels
                    output.write(channels + '\n')
                    #print(channels)

                elif directive == 'wireless.1.scan_list.channels':
                    # This is handled when we run into the SSID.
                    pass

                elif directive not in universaldirectives:
                    #print(line)
                    output.write(line + '\n')
        output.write('END ' + towername + '\n')

for tower in os.listdir('/root/radioconfigurator/configs'):
    towername = tower.replace('.cfg', '')
    with open('/root/radioconfigurator/newconfigs/' + tower, 'w') as output:
        with open('/root/radioconfigurator/specifics.conf') as specifics:
            start = False
            for line in specifics.readlines():
                if line == 'END ' + towername + '\n':
                    start = False
                if start:
                    output.write(line)
                if line == 'BEGIN ' + towername + '\n':
                    start = True
        with open('/root/radioconfigurator/universalconfig.conf') as universal:
           for line in universal.readlines():
            output.write(line)
