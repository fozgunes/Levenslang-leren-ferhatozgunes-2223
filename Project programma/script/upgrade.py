from netmiko import ConnectHandler
import time

# Device details
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.1.1',
    'username': 'admin',
    'password': 'password',
    'secret': 'enable_password',
}

# Firmware file details
firmware_file = {
    'path': '/path/to/firmware.bin',
    'protocol': 'tftp',
    'server_ip': '192.168.1.100',
}

def upgrade_firmware(device, firmware_file):
    # Connect to the device using Netmiko
    net_connect = ConnectHandler(**device)

    # Enter privileged EXEC mode
    net_connect.enable()

    # Disable logging to the console
    net_connect.send_command('no logging console')

    # Enter global configuration mode
    net_connect.config_mode()

    # Disable the boot system configuration
    net_connect.send_command('no boot system')

    # Configure the boot image from the firmware file
    config_commands = [f'boot system {firmware_file["protocol"]}://{firmware_file["server_ip"]}/{firmware_file["path"]}']
    net_connect.send_config_set(config_commands)

    # Save the configuration
    net_connect.send_command_expect('write memory')

    # Exit configuration mode
    net_connect.exit_config_mode()

    # Reboot the switch
    net_connect.send_command_timing('reload', delay_factor=2)
    time.sleep(5)
    net_connect.send_command_timing('y')

    # Close the connection
    net_connect.disconnect()

if __name__ == '__main__':
    upgrade_firmware(device, firmware_file)