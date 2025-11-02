from netmiko import ConnectHandler
from datetime import datetime


devices = [
    {
    'device_type': 'cisco_ios',
    'host':   '192.168.91.115',
    'username': 'admin',
    'password': 'Eveng138343',
#     'port' : 8022,          # optional, defaults to 22
#     'secret': 'secret',     # optional, defaults to ''
}
, {
    'device_type': 'cisco_ios',
    'host':   '192.168.91.116',
    'username': 'admin',
    'password': 'Eveng138343',
#     'port' : 8022,          # optional, defaults to 22
#     'secret': 'secret',     # optional, defaults to ''
}
]

def exe_cmd():

    try:
        commands = ["show version", "show int brief | grep up"]
        # commands = ["show ip int brief"]
        # commands = ["hostname nxos"]
        # commands = ["router bgp 100"]
        for command in commands:
            # test_fsm= true
            output = net_connect.send_command(command)
            print(output)
            # output += net_connect.save_config()

            time_now = datetime.now()
            switch_ip = device.get('host').replace(".","-")
            current_date = time_now.strftime("%Y-%m-%d")
            output_file_name = f'output of {switch_ip} {current_date}.txt'
            
            with open(output_file_name, 'a') as output_file:
                 print(f"Output for {command} {output} ", file=output_file)

            # Use_genie
            # output = net_connect.send_command(command, use_genie==True)
            # print(f'\n {device.get('host')} version of output {command}{output}\n')

    except Exception as e:
        print(f'{e}')

def main():
    for device in devices:
        global net_connect
        net_connect =  ConnectHandler(**device)
        output1 =  net_connect.find_prompt()
        print(f'{output1}')
        exe_cmd()
        
if __name__ == "__main__":
    main()
