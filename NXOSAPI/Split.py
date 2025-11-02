
from netmiko import ConnectHandler
from datetime import datetime
import logging

NXOS1  =     {
    'device_type': 'cisco_ios',
    'host':   '192.168.91.115',
    'username': 'admin',
    'password': 'Eveng138343',
#     'port' : 8022,          # optional, defaults to 22
#     'secret': 'secret',     # optional, defaults to ''
}
NXOS2 = {
    'device_type': 'cisco_ios',
    'host':   '192.168.91.116',
    'username': 'admin',
    'password': 'Eveng138343',
#     'port' : 8022,          # optional, defaults to 22
#     'secret': 'secret',     # optional, defaults to ''
}

# # 
# logger = logging.getLogger(__name__)
# net_connect = ConnectHandler(**cisco_881)
# output = net_connect.send_command('show run')
# print(output)
# #     print(f"e")

def exec_cmd():
    try:
        # show ip int output
        commands = [
        "show ip interface brief",
        ]     

        for cmd in commands:
            output = net_connect.send_command(cmd)
            # print(f'Output for {cmd}:\n{output}\n', file=output_file)
            split_line = output.splitlines()
            print(f'{split_line}')
        
        #     # starting time
        #     start_time = datetime.now()

        # # Generate the output file name with the switch IP and current date
        #     switch_ip =  device.get("host").replace(".","-")
        #     current_date = datetime.now().strftime("%Y-%m-%d")
        #     output_file_name = f"output_{switch_ip}_{current_date}.txt"

        #     with open(output_file_name, "a") as output_file:
        #         print(f'Output for {cmd}:\n {output} \n', file=output_file)
            
            

    except Exception as e:
        print(f"SSHException for {device.get("host")}: {str(e)}")

for device in (NXOS1,NXOS2):
    net_connect = ConnectHandler(**device)
    exec_cmd()
