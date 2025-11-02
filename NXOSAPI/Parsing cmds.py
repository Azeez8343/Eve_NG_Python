
from multiprocessing import Pool
from getpass import getpass
from netmiko import ConnectHandler
from datetime import datetime
from time import time

cmd = input("Enter config commands seperated by ',': ")
host = input("Enter the host IPs seperate with space: ")

hosts = host.split()
cmds = cmd.split(",")

starting_time = time()

def run_script(host_ip):
    try:
        ios_rtr = {
            "device_type": "cisco_ios",
            "ip": host_ip,
            "username": "admin",
            "password": "Eveng138343",
            }
    
        net_connect = ConnectHandler(**ios_rtr)
        
        print("Connected to host:", host_ip)

        output = net_connect.send_config_set(cmds)
        # print(output)
        # print('\n---- Elapsed time=', time()-starting_time)
        time_now = datetime.now()
        switch_ip = host_ip.replace(".","-")
        current_date = time_now.strftime("%Y-%m-%d")
        output_file_name = f'output of {switch_ip} {current_date}.txt'
                
        with open(output_file_name, 'a') as output_file:
            print(f"Output for {cmds} {output} ", file=output_file)
    except Exception as e:
        print(f'{e}')

if __name__ == "__main__":
    # Pool(5) means 5 process / devices will be run at a time, until youve gone through the device list
    for host_ip in hosts:
        run_script(host_ip)