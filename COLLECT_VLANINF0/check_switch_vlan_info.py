from netmiko import ConnectHandler
import time

with open( 'CE6881list.txt' ) as CE6881:
  for IP in CE6881 :
       device = {'device_type':'huawei',
                 'host': IP,
                'username':'huaweiatkins',
                 'password':'Murambinda12#$'}

       myssh=ConnectHandler(**device)
       print('8'*200)
       print(f'connecting to {IP} ')
       #print()
       #commands_to_run1 = ['disp sysname','dis lldp nei br']
       commands_to_run = ['display vlan']
       output0 = myssh.send_command("dis sysname ")
       output1 = myssh.send_command("dis vlan | i common ")
       
       output2 = (myssh.send_config_set(commands_to_run))
       time.sleep(0)
       print(output0)
       print(output2)
       print(output1)
       backupfilename = "CE6851-48S6Q-HI_VLANS-DATA.txt"
       backupfile = open(backupfilename, "a")
       backupfile.write("X"*200)
       backupfile.write("\n")
       backupfile.write(output0)
       backupfile.write("\n")
       backupfile.write(output1)
       backupfile.write("\n")
       backupfile.close()

       #backupfilename1 = 'CE6851-48S6Q-HI_VLANS_LLDP_NEIGHBORS.txt'
       #backupfile1 = open(backupfilename1, "a")
       #backupfile1.write(output1)
       #backupfile1.close()