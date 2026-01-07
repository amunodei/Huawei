from netmiko import ConnectHandler

with open("devices.txt") as CE6881:
    for IP in CE6881:
        IP = IP.strip()

        device = {
            "device_type": "huawei",
            "host": IP,
            "username": "huaweiatkins",
            "password": "Murambinda12#$",
        }

        print("=" * 80)
        print(f"Connecting to {IP}")

        myssh = ConnectHandler(**device)

        # 🔹 Disable paging immediately
        myssh.send_command("screen-length 0 temporary")

        # 🔹 Get VRP version safely
        version_output = myssh.send_command("display version | include VRP")
        print(version_output)

        # 🔹 Interface summary
        int_brief = myssh.send_command("display ip interface brief")
        print(int_brief)

        # 🔹 Decide routing command based on VRP output
        if "VRP" in version_output:
            print("Running routing-table command (standard)")
            routes = myssh.send_command_timing("display ip routing-table | include 10.1.24.")
            print(routes)

        else:
            print("Running routing-table all-routes")
            routes = myssh.send_command_timing(
                "display ip routing-table all-routes"
            )
            print(routes)

        myssh.disconnect()
