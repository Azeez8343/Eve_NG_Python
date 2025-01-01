import sys
import threading
import time
from math import trunc

from netmiko import Netmiko
import datetime
import schedule
from netmiko.exceptions import NetmikoAuthenticationException


# net_Connect = Netmiko( device_type= 'cisco_ios',
#                         host =   '192.168.91.5',
#                         username = 'admin',
#                         password= 'Eveng138343',
# )


nx_OS = {               'device_type':'cisco_ios',
                                'host':'192.168.91.5',
                                'username':'admin',
                                'password':'Eveng138343'}

nx_OS1 = {               'device_type':'cisco_ios',
                                'host':'192.168.91.4',
                                'username':'admin',
                                'password':'Eveng138343'}

device_list = (nx_OS,nx_OS1)

def cisco_interface_parser(device):
    try:

        net_Connect = Netmiko(**device)
        now = datetime.datetime.now()
        print(f"device connected successfully: {device['host']} ")
        print(f"connection successful: {device['host']} {now}")
        print(f"connection successful: {device['host']} {net_Connect.find_prompt()} {now}")
        show_interface = net_Connect.send_command("show interface status")
        print(show_interface)


    except:
        print(sys.exc_info()[0])
        print("exception occured")

# def bkp_thread():
#     backup_thread_list = list()
#
#     for device in device_list:
#         backup_thread = threading.Thread(target=cisco_run,args=(device,))
#         backup_thread.start()
#         backup_thread_list.append(backup_thread)
#     for thread in backup_thread_list:
#         thread.join()


    print(f"******** Interface data printed successfully *****")

cisco_interface_parser(nx_OS1)




