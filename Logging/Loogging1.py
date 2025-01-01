import sys
import threading
from time import asctime

from netmiko import Netmiko
import datetime
#Import Logging
import logging
from netmiko.exceptions import NetmikoAuthenticationException


# Logging Levels #
################
#  CRITICAL 50
#  ERROR    40
#  WARNING  30
#  INFO     20
#  DEBUG    10
###############



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

#Define Logger
logger = logging.getLogger("SSH parser")

#Set the Minimum Log Level for logger
logger.setLevel(logging.DEBUG)

# creating File handler to store info
File_logging_info = logging.FileHandler("sh_ver_info_logs")
File_logging_debug = logging.FileHandler("sh_ver_debug_logs")
stem_handler = logging.StreamHandler(sys.stdout)

# Set Additional log level in Handlers if needed
File_logging_info.setLevel(logging.INFO)
File_logging_debug.setLevel(logging.DEBUG)
stem_handler.setLevel(logging.WARNING)

# Create Formatter and Associate with Handlers
formatter = logging.Formatter('%(asctime)s - %(name)s -%(levelname)s - %(message)s')
File_logging_debug.setFormatter(formatter)
File_logging_info.setFormatter(formatter)
stem_handler.setFormatter(formatter)

# Assigning logger to file handler
logger.addHandler(File_logging_info)
logger.addHandler(File_logging_debug)
logger.addHandler(stem_handler)

device_list = (nx_OS,nx_OS1)

logger.info(f"'#'* 5 connection establishing '#'* 5")


def cisco_run(device):
    try:

        net_Connect = Netmiko(**device)
        now = datetime.datetime.now()

        print(f"device connected successfully: {device['host']} ")
        logger.info(f"'#'* 5 device connected successfully: {device['host']}'#'* 5")

        print(f"connection successful: {device['host']} {now}")
        logger.info(f"'#'* 5 connection successful: {device['host']}'#'* 5")

        print(f"connection successful: {device['host']} {net_Connect.find_prompt()} {now}")

        show_run = net_Connect.send_command("show run")

        print(f'show run executed:{device['host']}')
        logger.info(f"'#'* 5 show run executed:{device['host']}'#'* 5")


        # now = datetime.datetime.now()   # creating timestamp
        # print(f'{show_run},{now}')
        # current_config_file = f"{now}_{device['host']}.txt"      # defing name of backup file
        # with open(current_config_file, "w") as file:            # creating file
        #     file.write(show_run)
        # print(f"saving the output to file :{current_config_file } {now}")

    except:
        print(sys.exc_info()[0])
        print("exception occured")
        logger.warning(f"'#'* 5 unsuccessful:{device['host']}'#'* 5")

backup_thread_list = list()

for device in device_list:
    backup_thread = threading.Thread(target=cisco_run,args=(device,))
    backup_thread.start()
    backup_thread_list.append(backup_thread)
for thread in backup_thread_list:
    thread.join()


print(f"******** Threading completed sucessfully *****")


###
# t1= threading.Thread(target=cisco_run, args=(nx_OS,))
# t2= threading.Thread(target=cisco_run, args=(nx_OS1,))
#
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# ####


# cisco_run(nx_OS)
# cisco_run(nx_OS1)
