import ipaddress

from django.forms import ModelForm,ModelChoiceField,Form,GenericIPAddressField,CharField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .models import IpAddress, Subnet

def subnet_validate(value):
    try:
        ipaddress.ip_network(value)
    except ValueError:
        raise ValidationError('%(value)s 格式不正确',params={'value':value})

class IpAddressForm(ModelForm):
    subnet =  ModelChoiceField(queryset=Subnet.objects.all(),empty_label=None,label="IP子网",initial="")

    class Meta:
        model = IpAddress
        fields = ("ip_address", "subnet","description")
    
class SubnetForm(ModelForm):
    subnet = CharField(label="子网",max_length=128,validators=[subnet_validate])
    
    class Meta:
        model = Subnet
        fields = ("name", "subnet", "description")