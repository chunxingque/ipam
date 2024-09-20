import ipaddress

from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import SubnetForm,IpAddressForm
from . import models



@require_GET
@login_required(login_url="/login/")
def subnet_list(request):
    search_subnet = request.GET.get('subnet', "")
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    if search_subnet:
        subnets_obj = models.Subnet.objects.filter(subnet__icontains=search_subnet)
    else:
        subnets_obj = models.Subnet.objects.all()
    paginator = Paginator(subnets_obj, per_page=int(page_size))
    subnets = paginator.get_page(page)
    
    form = SubnetForm()
    return render(request, 'subnet/subnet.html', {'form': form, 'subnets': subnets,'search_subnet': search_subnet})

@login_required(login_url="/login/")
def add_subnet(request):
    custom_errors = {
        "subnet": []
    }
    if request.method == 'POST':
        form = SubnetForm(request.POST)
        if form.is_valid():
            subnet = models.Subnet.objects.filter(subnet=form.cleaned_data['subnet']).first()
            if subnet:
                custom_errors["subnet"].append(f"{subnet.subnet} 子网已经存在")
                return render(request, 'subnet/subnet_add.html', {'form': form,'custom_errors': custom_errors})
            else:
                form.save()
                return HttpResponseRedirect('/subnet/')
        else:
            return render(request, 'subnet/subnet_add.html', {'form': form,'custom_errors': custom_errors})
    else:
        form = SubnetForm(initial={"name": "","subnet": "","description": ""})
        return render(request, 'subnet/subnet_add.html', {'form': form,'custom_errors': custom_errors})
        
@login_required(login_url="/login/")        
def subnet_edit(request,pk):
    # 编辑解锁
    edit_result = False
    subnet = models.Subnet.objects.get(pk=pk)
    if request.method == 'POST':
        form = SubnetForm(request.POST, instance=subnet)
        if form.is_valid():
            form.save()
            edit_result = True
            
        return render(request, 'subnet/subnet_edit.html', {'form': form,"id": pk,'edit_result': edit_result})
    
    form = SubnetForm(instance=subnet)
    return render(request, 'subnet/subnet_edit.html', {'form': form,"id": pk,'edit_result': edit_result})

@login_required(login_url="/login/")
@require_GET
def subnet_del(request,pk):
    subnet = models.Subnet.objects.get(pk=pk)
    subnet.delete()
    return HttpResponseRedirect('/subnet/')

@login_required(login_url="/login/")
@require_GET
def ip_address_list(request):
    search_ip = request.GET.get('ip', "")
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 10)
    if search_ip:
       ip_addresses_obj = models.IpAddress.objects.filter(ip_address__icontains=search_ip)
    else:
        ip_addresses_obj = models.IpAddress.objects.all()
    paginator = Paginator(ip_addresses_obj, per_page=int(page_size))
    ip_addresses = paginator.get_page(page)
    
    return render(request, 'ip_address/ip_address.html', {'ips': ip_addresses,'search_ip': search_ip})

@login_required(login_url="/login/")
def ip_address_add(request):
    custom_errors = {
        "ip_address": []
    }
    
    if request.method == 'POST':    
        form = IpAddressForm(request.POST)
        if form.is_valid():
            ip_address = models.IpAddress.objects.filter(ip_address=form.cleaned_data['ip_address']).first()
            if ip_address:
                custom_errors["ip_address"].append(f"{ip_address.ip_address} 地址已经存在")
                return render(request, 'ip_address/ip_address_add.html', {'form': form,'custom_errors': custom_errors})
            else:
                form.save()
                return HttpResponseRedirect('/ip/')
        else:
            return render(request, 'ip_address/ip_address_add.html', {'form': form,'custom_errors': custom_errors})
    else:
        form = IpAddressForm(initial={"ip_address": "","description": ""})
        return render(request, 'ip_address/ip_address_add.html', {'form': form,'custom_errors': custom_errors})
    
@login_required(login_url="/login/")
def ip_address_edit(request,pk):
    ip_address = models.IpAddress.objects.get(pk=pk)
    if request.method == 'POST':
        form = IpAddressForm(request.POST, instance=ip_address)
        if form.is_valid():
            form.save()
    else:    
        form = IpAddressForm(instance=ip_address)
    
    return render(request, 'ip_address/ip_address_edit.html', {'form': form,"id": pk})

@login_required(login_url="/login/")
@require_GET
def ip_show(request,pk):
    subnet = models.Subnet.objects.get(pk=pk)
    subnet_param = {
        'id': subnet.id,
        'name': subnet.name,
        'subnet': subnet.subnet,
        'description': subnet.description
    }
    ips = models.IpAddress.objects.filter(subnet_id=pk)
    ips_used_param = {}
    ips_used = []
    for ip in ips:
        ips_used.append(ip.ip_address)
        ips_used_param[ip.ip_address] = {
            'id': ip.id,
            'used': True,
            'ip_address': ip.ip_address,
            'subnet': subnet.subnet,
            'description': ip.description,
        }
    
    net = ipaddress.ip_network(subnet.subnet, strict=False)
    ips_param = []
    for ip in net.hosts():
        if str(ip) in ips_used:
            ips_param.append(ips_used_param[str(ip)])
        else:
            ips_param.append({"used": False, "ip_address": str(ip)})
            
    return render(request, 'subnet/ip_show.html',context={'subnet': subnet_param, 'ips_param': ips_param})

@login_required(login_url="/login/")
@require_GET
def ip_address_del(request,pk):
    ip = models.IpAddress.objects.get(pk=pk)
    if ip:
        ip.delete()
        return HttpResponseRedirect('/ip/')
    else:
        return HttpResponseRedirect('/ip/')