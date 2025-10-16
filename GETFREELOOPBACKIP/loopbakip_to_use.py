import paramiko
import re
from ipaddress import ip_network, ip_address

# Configuration
DEVICE_LIST_FILE = 'devices.txt'  # Each line: <hostname_or_ip> <username> <password>
SUBNET = '10.1.24.0/24'        # Change to your subnet

def read_devices(filename):
    devices = []
    with open(filename) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                devices.append({'host': parts[0], 'user': parts[1], 'pass': parts[2]})
    return devices

def ssh_command(host, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=username, password=password, timeout=10)
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        return output
    except Exception as e:
        print(f"Failed to connect to {host}: {e}")
        return ""
    finally:
        client.close()

def extract_ips(text):
    # Match IPv4 addresses (improved regex to avoid partial matches)
    return set(re.findall(r'^(\d{1,3}\.\d{1,3}\.\d{1,3})\.', text))

def get_used_ips(device):
        commands = [
            'screen-length 0 temporary',
            'display ip interface brief',
            'display ip routing-table'
        ]
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        config_ips = set()
        route_ips = set()
        try:
            client.connect(device['host'], username=device['user'], password=device['pass'], timeout=10)
            for command in commands:
                stdin, stdout, stderr = client.exec_command(command)
                output = stdout.read().decode()
                if command == 'display ip interface brief':
                    config_ips = {ip for ip in extract_ips(output) if ip.startswith('10.1.24.')}
                elif command == 'display ip routing-table':
                    route_ips = extract_ips(output)
        except Exception as e:
            print(f"Failed to connect to {device['host']}: {e}")
        finally:
            client.close()
        return config_ips.union(route_ips)
def main():
    devices = read_devices(DEVICE_LIST_FILE)
    subnet = ip_network(SUBNET)
    all_used_ips = set()
    for device in devices:
        print(f"Checking device: {device['host']}")
        used_ips = get_used_ips(device)
        # Filter only IPs in the subnet
        used_in_subnet = {ip for ip in used_ips if ip_address(ip) in subnet}
        all_used_ips.update(used_in_subnet)
        print(f"Used IPs on {device['host']}: {sorted(used_in_subnet)}")
    all_ips_in_subnet = {str(ip) for ip in subnet.hosts()}
    unused_ips = sorted(all_ips_in_subnet - all_used_ips)
    print("\nSummary:")
    print(f"Used IP addresses: {sorted(all_used_ips)}")
    print(f"Unused IP addresses: {sorted(unused_ips)}")

if __name__ == "__main__":
    main()