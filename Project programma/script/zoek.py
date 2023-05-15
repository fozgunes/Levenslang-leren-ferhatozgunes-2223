from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
from netmiko.exceptions import AuthenticationException
from pysnmp.hlapi import *
import re



ip_lijst = ['192.168.1.1', '192.168.1.2','192.168.1.3','192.168.1.4','192.168.1.5',] 

#lijst van toestellen
devices = []

with open("lijstvanswitches.csv", "w+") as f:
    f.write("IP Address,Hostname,Current_Version,Current_Image,Uptime,Device_Memory, Serial_Number,Device_Model\n")

with open("login_issues.csv", "w+") as f:
    f.write("IP Address,Status\n")


for ip in ip_list:
    cisco = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': 'xxx', #ssh username
        'password': 'xxx', #ssh password
        'secret': 'xxx', #ssh_enable_password
        'ssh_strict': False,
        'fast_cli': False,
    }

    #handling exceptions errors

    try:
        net_connect = ConnectHandler(**cisco)
    except NetMikoTimeoutException:
        with open("login_issues.csv", "a") as f:
            f.write(f"{ip},Toestel niet beschikbaar\n")
        continue
    except AuthenticationException:
        with open("login_issues.csv", "a") as f:
            f.write(f"{ip},Authenticatie mislukt\n")
        continue
    except SSHException:
        with open("login_issues.csv", "a") as f:
            f.write(f"{ip},SSH niet enabled\n")
        continue
    try:
        net_connect.enable()
      
    except ValueError:
        with open("login_log.csv", "a") as f:
            f.write(f"{ip},Can ssh enable pasword probleem zijn\n")
        continue
        

    #execute show version on router and save output to output object
    sh_ver_output = net_connect.send_command('show version')
    print(f"-----\n{sh_ver_output}\n")


def get_snmp_data(ip, community_string, oid):
    error_indication, error_status, error_index, var_binds = next(
        getCmd(SnmpEngine(),
               CommunityData(community_string),
               UdpTransportTarget((ip, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if error_indication:
        print(f"SNMP error: {error_indication}")
        return None
    elif error_status:
        print(f"SNMP error: {error_status}")
        return None
    else:
        for var_bind in var_binds:
            return var_bind.prettyPrint()


def discover_switches(network, community_string):
    for i in range(1, 255):
        ip = f"{network}.{i}"
        sys_descr_oid = "1.3.6.1.2.1.1.1.0"
        sys_name_oid = "1.3.6.1.2.1.1.5.0"
        cisco_image_oid = "1.3.6.1.4.1.9.9.109.1.1.1.1.2.1"

        sys_descr = get_snmp_data(ip, community_string, sys_descr_oid)
        sys_name = get_snmp_data(ip, community_string, sys_name_oid)
        cisco_image = get_snmp_data(ip, community_string, cisco_image_oid)

        if sys_descr and sys_name and cisco_image:
            print(f"Switch found at IP: {ip}")
            print(f"System Description: {sys_descr}")
            print(f"System Name: {sys_name}")
            print(f"Cisco Image: {cisco_image}")
            print("-" * 40)


if __name__ == "__main__":
    network = "192.168.1"  # Replace with your network address
    community_string = "public"  # Replace with your SNMP community string

    discover_switches(network, community_string)