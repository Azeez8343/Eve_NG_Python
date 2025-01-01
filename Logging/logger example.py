#! /usr/local/Python_envs/Python3/bin/python3
import paramiko
import time
import re
import sys

# Logging Levels #
################
#  CRITICAL 50
#  ERROR    40
#  WARNING  30
#  INFO     20
#  DEBUG    10
###############

#Import Logging
import logging

#Define Logger
logger = logging.getLogger("SSH_Parser")

#Set the Minimum Log Level for logger
logger.setLevel(logging.DEBUG)

#Create Handlers(Filehandler with filename| StramHandler with stdout)
file_handler_info = logging.FileHandler('show_ver_info.log')
file_handler_debug = logging.FileHandler('show_ver_debug.log')
stream_handler = logging.StreamHandler(sys.stdout)

#Set Additional log level in Handlers if needed
file_handler_info.setLevel(logging.INFO)
file_handler_debug.setLevel(logging.DEBUG)
stream_handler.setLevel(logging.WARNING)

#Create Formatter and Associate with Handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler_info.setFormatter(formatter)
file_handler_debug.setFormatter(formatter)
stream_handler.setFormatter(formatter)

#Add Handlers to logger
logger.addHandler(file_handler_info)
logger.addHandler(file_handler_debug)
logger.addHandler(stream_handler)

version_pattern = re.compile(r'Cisco .+ Software, Version (\S+)')
model_pattern = re.compile(r'cisco (\S+).+bytes of memory\.')
serial_no_pattern = re.compile(r'Processor board ID (\S+)')
uptime_pattern = re.compile(r'(.+) uptime is (.*)')

lab_csr = {
	'host': 'csr1.test.lab',
	'username': 'admin',
	'password': 'admin'
}
devnet_csr = {
	'host': 'ios-xe-mgmt-latest.cisco.com',
	'username': 'developer',
	'password': 'C1sco12345'
}
#Set the logger for required instances with loging level and Messages
logger.info(f"{'#'*15} INITIALIZING THE SCRIPT {'#'*15}")
def cisco_parse_version(host,username,password):
	#Set the logger for required instances with loging level and Messages
	logger.info(f"Connecting to the Device :{host}")
	#Set the logger for required instances with loging level and Messages
	logger.info(f"Username is :{username}")
	try:
		print(f"\n{'#' * 55}\nConnecting to the Device {host}\n{'#' * 55} ")
		SESSION = paramiko.SSHClient()
		SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		SESSION.connect(host, port=22,
						username=username,
						password=password,
						look_for_keys=False,
						allow_agent=False)
		logger.info("Connected Successfully")
		DEVICE_ACCESS = SESSION.invoke_shell()
		logger.info("Executing the command 'show version'")
		DEVICE_ACCESS.send(b'term length 0\n')
		DEVICE_ACCESS.send(b'show run\n')
		time.sleep(1)
		output = (DEVICE_ACCESS.recv(65000).decode('ascii'))

		logger.info(f"Received Output")
		logger.debug(f"Output Data: {output}")

		version_match = version_pattern.search(output)
		version_result = ('IOS Version'.ljust(18)+': '+version_match.group(1))
		print(version_result)
		logger.info(version_result)

		model_match = model_pattern.search(output)
		model_result = ('Model '.ljust(18)+': '+model_match.group(1))
		print(model_result)
		logger.info(model_result)

		serial_no_match = serial_no_pattern.search(output)
		serial_no_result = ('Serial Number '.ljust(18)+': '+serial_no_match.group(1))
		print(serial_no_result)
		logger.info(serial_no_result)

		uptime_match = uptime_pattern.search(output)
		host_name_result = ('Host Name '.ljust(18)+': '+uptime_match.group(1))
		print(host_name_result)
		logger.info(host_name_result)

		up_time_result = ('Device Uptime '.ljust(18)+': '+uptime_match.group(2))
		print(up_time_result)
		logger.info(up_time_result)

		print(f"\n{'#' * 55}\nFinished Executing Script\n{'#' * 55} ")
		SESSION.close()
		logger.info(f"Successfully Completed the Script execution\n")
	except paramiko.ssh_exception.AuthenticationException:
		logger.warning("Authentication failed")
		# logger.exception("Authentication failed")
		print("Authentication Failed")
	except AttributeError:
		logger.error("Parsing error: Check the Command\n")
		print("Parsing Error, Please check the command")
	except:
		logger.critical("Unable to connect\n")
		print("Can not connect to Device")
cisco_parse_version(**devnet_csr)