from netmiko import ConnectHandler
import time

with open( 'devices1.txt' ) as CE6881:
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
       commands_to_run = ('display ip routing-table all-routes')
       output0 = myssh.send_command("dis sysname ")
       output1 = myssh.send_command("disp ip int br ")
       
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