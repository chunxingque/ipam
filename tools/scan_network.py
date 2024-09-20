#!/usr/bin/env python3

import os
import sys
import django
import argparse

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.abspath(os.path.join(DIR_PATH,".."))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipam.settings')
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)
django.setup()
from apps.ipamapi.subnet import scan_subnet_ip
from apps.ipamapi.models import IpAddress,Subnet


exec_name = os.path.basename(__file__)
example_text = f'''use of example:
python {exec_name} 192.168.15.125/24
'''

parser = argparse.ArgumentParser(description='扫描网络存活ip，并存入数据库',epilog=example_text,formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('subnet', help='子网地址')
args = parser.parse_args()

subnet = args.subnet

def scan_network(subnet: str):
    """扫描网络存活ip，并存入数据库

    Args:
        subnet (str): 子网地址
    """
    subnet_obj = Subnet.objects.filter(subnet=subnet).first()
    if not subnet_obj:
        print("请先添加子网")
    else:    
        ips = scan_subnet_ip(subnet)
        for ip in ips:
            ip_obj = IpAddress.objects.filter(ip_address=ip).first()
            if not ip_obj:
                print("添加IP到数据库: {}".format(ip))
                IpAddress.objects.create(ip_address=ip, subnet=subnet_obj)
    
        print("扫描完成")

if __name__ == '__main__':
    scan_network(subnet)