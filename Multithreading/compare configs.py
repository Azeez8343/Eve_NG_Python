import sys

from netmiko import Netmiko
import datetime
import difflib
import webbrowser
from netmiko.exceptions import NetmikoAuthenticationException

try:
    nx_OS = {               'device_type':'cisco_ios',
                            'host':'192.168.91.5',
                            'username':'admin',
                            'password':'Eveng1383438'}

    net_Connect = Netmiko(**nx_OS)

    # net_Connect = Netmiko( device_type= 'cisco_ios',
    #                         host =   '192.168.91.5',
    #                         username = 'admin',
    #                         password= 'Eveng138343',
    # )
    print(net_Connect.find_prompt())
    print ("connection successful")

    show_run = net_Connect.send_command("show run")
    # with open(backup)
    # print (show_run)
    now = datetime.datetime.now().replace(microsecond=0)    # creating timestamp
    current_config_file = f"{now}_{nx_OS['host']}.txt"      # defing name of backup file
    with open(current_config_file, "w") as file:            # creating file
        file.write(show_run)

    ref_file = open("backup.txt")
    ref_read = ref_file.readlines()
    ref_file.close()

    current_file = open(current_config_file)
    currnet_read = current_file.readlines()
    current_file.close()

    conf_compare = difflib.HtmlDiff().make_file(fromlines=ref_read,
                                                tolines=currnet_read,
                                                fromdesc="backup ref",
                                                todesc=f"current{current_config_file}")
    with open("diff.html","w") as newfile:
        newfile.write(conf_compare)

    webbrowser.open_new_tab("diff.html")
except NetmikoAuthenticationException:
    print ('authentication failed')

except:
    print(sys.exc_info()[0])
    print("exception occured")