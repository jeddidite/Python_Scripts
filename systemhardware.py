#!python
"""
Dependencies
apt update && apt upgrade -y && apt install -y scsitools pciutils smartmontools mdadm dmidecode ipmitool net-tools ethtool sysstat lm-sensors
yum update && yum upgrade -y && yum install -y scsitools pciutils smartmontools mdadm dmidecode ipmitool net-tools ethtool sysstat lm-sensors
sensors-detect -y
"""
import subprocess

# Host info output
def printhost():
    serial = subprocess.run(['sudo dmidecode -t3 | grep "Serial Number"'], capture_output=True, text=True, shell=True)
    serial = serial.stdout.split('Serial Number: ')[1].strip()
    product = subprocess.run(['sudo dmidecode -t1 | grep "Product"'], capture_output=True, text=True, shell=True)
    product = product.stdout.split('Product Name: ')[1].strip()
    man = subprocess.run(['sudo dmidecode -t1 | grep "Manufacturer"'], capture_output=True, text=True, shell=True)
    man = man.stdout.split('Manufacturer: ')[1].strip()
    asset = subprocess.run(['sudo dmidecode -t3 | grep "Asset"'], capture_output=True, text=True, shell=True)
    asset = asset.stdout.split('Asset Tag: ')[1].strip()
    hostname = subprocess.run(['hostname'], capture_output=True, text=True, shell=True)
    hostname = hostname.stdout.strip()
    hostnamectl = subprocess.run(['hostnamectl | tail -5'], capture_output=True, text=True, shell=True)
    hostnamectl = hostnamectl.stdout.split('Operating System: ')[0].strip().splitlines()
    date = subprocess.run(['date'], capture_output=True, text=True, shell=True)
    date = date.stdout.strip()
    uptime = subprocess.run(['uptime'], capture_output=True, text=True, shell=True)
    uptime = uptime.stdout.strip()
    who = subprocess.run(['who'], capture_output=True, text=True, shell=True)
    who = who.stdout.strip()
    print("Device Information:" + '\n' + "OS: " + hostnamectl[0] + "\n" + hostnamectl[1].strip() + "\n" + hostnamectl[4].strip())
    print("Serial Number: " + serial + "\n" + "Product: " + product)
    print("Asset Number:  " + asset + "\n" + "Hostname: " + hostname)
    print("Date:  " + date + "\n" + "Uptime: " + uptime)
    print("")


#CPU Output
def print_cpu():
    print("CPU Information:")
    rawdata = subprocess.run(['sudo', 'dmidecode', '-t4'], capture_output=True, text=True)
    if rawdata.returncode == 0:
        lines = rawdata.stdout.split('\n')
        Manufacturer = ''
        Family = ''   
        for line in lines:
            # At the start of a new Processor Information section, check and print if we have previous Manufacturer and Family
            if 'Processor Information' in line:
                if Manufacturer and Family:
                    print(f"{Manufacturer} {Family}")
                    Manufacturer = ''  # Reset for the next CPU
                    Family = ''
            elif 'Socket Designation:' in line:
                cpunum = line.split('Socket Designation:')[1].strip()
            elif 'Manufacturer:' in line:
                Manufacturer = line.split('Manufacturer: ')[1].strip()
            elif 'Family:' in line:
                Family = line.split('Family: ')[1].strip()
            elif 'Core Count:' in line:
                core = line.split('Core Count: ')[1].strip()
            elif 'Voltage:' in line:
                voltage = line.split('Voltage: ')[1].strip()
            elif 'Max Speed:' in line:
                max_speed = line.split('Max Speed: ')[1].strip()
            elif 'Current Speed:' in line:
                current_speed = line.split('Current Speed: ')[1].strip()
        print(f"Socket: {cpunum}")
        print(f"Model: {Manufacturer} {Family}")
        print(f"Max Speed: {max_speed} Current Speed: {current_speed}")
        print(f"Voltage: {voltage}")
        print(f"Cores: {core}")
    
def print_mem():
    # Get serial numbers and locators
    memserial_result = subprocess.run(['sudo', 'dmidecode', '-t17'], capture_output=True, text=True) #Running dmidecode
    if memserial_result.returncode == 0: # If the command worked
        rawdata = memserial_result.stdout.split('\n') # Bulk DIMM info
        dimm_counter = 0 # COunter to keep track of number of dimms starting at 0
        for line in rawdata:
            if 'Memory Device' in line: # Searching for "memory device"
                dimm_counter += 1  # Each instance of "Memory Device" means +1 DIMM installed
                print(f"\nDIMM {dimm_counter}:")
            elif 'Serial Number' in line and 'No Module Installed' not in line: # If "Serial Number exists"
                serial_number = line.split('Serial Number: ')[1].strip() #Split each dimm serial number 
                print(f"Serial Number: {serial_number}") #Print each Serial number on a new line, each serial is conencted to the counter
            elif 'Part Number' in line:
                part_number = line.split('Part Number: ')[1].strip()
                print(f"Part Number: {part_number}")
            elif 'Manufacturer' in line:
                man_number = line.split('Manufacturer: ')[1].strip()
                print(f"Manufacturer: {man_number}")
            elif 'Size' in line:
                size_number = line.split('Size: ')[1].strip()
                print(f"Memory Size: {size_number}")
            elif 'Memory Speed' in line:
                speed_number = line.split('Memory Speed: ')[1].strip()
                print(f"Memory Speed: {speed_number}")
            elif 'Locator' in line:
               locator = line.split('Locator: ')[1].strip()
               print(f"{locator}")
        print("\n")
printhost()
print_cpu()
print_mem()

"""
console 
/usr/bin/ipmitool lan print | grep IP | grep -v "IP Header" | grep -v "Backup Gateway" 
/usr/bin/ipmitool lan print | grep "MAC Address"

Set Network Variables
interface = ip -o link show | awk -F': ' '{print $2}' | grep -v "lo" | head -1

network 
ifconfig interface | grep inet | grep -v inet6
ifconfig interface | grep "RX errors"
ifconfig interface | grep "TX errors"
ethtool interface | grep "Speed"
ip link | grep -v lo | grep -v loopback | head -2 | grep ether

logs
/bin/dmesg | grep "Failed"
/bin/dmesg | grep "failed"
/usr/bin/ipmitool sel list

sensors
sensors | grep "Core"
sensors | grep "temp" | grep -v "coretemp"

OR
/usr/bin/ipmitool sdr list

VIDEO
sudo lshw -C video | head -4

Audio
lspci | grep -i audio

drive    
lsblk | grep -v loop
sudo parted -l | tail -13
sudo lshw -class disk -class storage | grep "serial"
sudo smartctl -a -t short /dev/nvme0n1 | grep "test result"

memory            
dmidecode -t19 | grep "Range Size"
battery
dmidecode -t22 | grep "Name"
dmidecode -t22 | grep "Capacity"
dmidecode -t22 | grep "Voltage"
dmidecode -t22 | grep "Manufacturer"
dmidecode -t22 | grep "Chemistry"

"""
