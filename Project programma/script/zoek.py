from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import SSHException
from netmiko.exceptions import AuthenticationException
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