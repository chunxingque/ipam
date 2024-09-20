import ipaddress
import subprocess


def ip_is_alive(ip):
    """判断ip是否存活

    Args:
        ip (_type_): _description_

    Returns:
        _type_: _description_
    """
    ping_response = subprocess.run(["ping", "-c", "1",ip], stdout=subprocess.PIPE)
    if ping_response.returncode == 0:
        return True
    else:
        return False

def scan_subnet_ip(subnet: str):
    """判断子网的ip是否存活

    Args:
        subnet (_type_): _description_

    Returns:
        _type_: _description_
    """
    ip_alive = []
    try:
        net =  ipaddress.ip_network(subnet,strict=False)
        for ip in net.hosts():
            ip_status = ip_is_alive(str(ip))
            if ip_status:
                ip_alive.append(str(ip))
        return ip_alive
    except ValueError:
        print("Invalid subnet")
        return []

if __name__ == '__main__':
    print(scan_subnet_ip("192.168.15.0/24"))
