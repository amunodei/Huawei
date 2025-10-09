from netmiko import ConnectHandler

with open( 'CE6881List.txt' ) as CE6881:
  for IP in CE6881 :
       device = {'device_type':'huawei',
                 'host': IP,
                'username':'huaweiatkins',
                 'password':'Murambinda12#$'}

       myssh=ConnectHandler(**device)
       print('8'*200)
       print(f'connecting to {IP} ')

       commands_to_run = ['disp sysname','display int br ']
       
       output1 = myssh.send_command('disp sysname')
       output2 = (myssh.send_config_set(commands_to_run))
       backupfilename = output1 + '-Backup.txt'
       backupfile = open(backupfilename, "w")
       backupfile.write(output1)
       backupfile.close()