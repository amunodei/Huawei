from netmiko import ConnectHandler
import time

with open( 'devices.txt' ) as network_devices:
  for IP in network_devices :
       device = {'device_type':'huawei',
                 'host': IP,
                'username':'huaweiatkins',
                 'password':'Murambinda12#$'}

       myssh=ConnectHandler(**device)
       print('X'*100)
       print(f'connecting to {IP} ')
       backupfilename = "Looback_ips_inuse_" + time.strftime("%Y%m%d_%H%M%S") + ".txt"
       backupfile = open(backupfilename, "a")
       myssh.send_command("screen-length 0 temporary")
       device_name = myssh.send_command("disp sysname")
       print(device_name)
       version_output = myssh.send_command("display version | include VRP")[1:4]
       print(version_output)
       output1 = myssh.send_command("disp ip int br")
       backupfile.write("X"*200)
       backupfile.write("\n")
       backupfile.write(output1)
       print(output1)
       if version_output == "026" :
        output3 = myssh.send_command_timing("display ip routing-table | i 10.1.24.")
        print(output3)
        backupfile.write("X"*200)
        backupfile.write("\n")
        backupfile.write(output3)
       elif version_output == "nfo" :
        output4 = myssh.send_command_timing("display ip routing-table all-routes | i 10.1.24")
        print(output4)
        backupfile.write("X"*200)
        backupfile.write("\n")
        backupfile.write(output4)
       else:
        print("No matching VRP version found.") 


        #backupfile.write("\n")
        #backupfile.write(output3)
        #backupfile.write("\n")
        #backupfile.write(output4)
        backupfile.close()