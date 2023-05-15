from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

# Sample list of network devices
devices = [
    {
        'name': 'Router1',
        'ip': '192.168.1.1',
        'username': 'admin',
        'password': 'password',
        'device_type': 'cisco_ios',
    },
    {
        'name': 'Switch1',
        'ip': '192.168.1.2',
        'username': 'admin',
        'password': 'password',
        'device_type': 'cisco_ios',
    },
]

@app.route('/')
def index():
    return render_template('index.html', devices=devices)

@app.route('/configure', methods=['GET', 'POST'])
def configure():
    if request.method == 'POST':
        device_name = request.form['device']
        command = request.form['command']

        # Find the selected device in the devices list
        selected_device = next((device for device in devices if device['name'] == device_name), None)
        
        if selected_device:
            # Connect to the selected device using Netmiko
            net_connect = ConnectHandler(
                ip=selected_device['ip'],
                username=selected_device['username'],
                password=selected_device['password'],
                device_type=selected_device['device_type']
            )
            
            # Send the command and retrieve the output
            output = net_connect.send_command(command)
            
            # Close the connection
            net_connect.disconnect()
            
            return render_template('configure.html', device=selected_device, command=command, output=output)

    return render_template('configure.html', devices=devices)

if __name__ == '__main__':
    app.run(debug=True)