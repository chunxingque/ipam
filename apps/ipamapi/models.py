from django.db import models

class Subnet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True, verbose_name='名称')
    subnet = models.CharField(max_length=100, db_index=True, verbose_name='子网')
    description = models.CharField(max_length=100, blank=True, verbose_name='描述')

    class Meta:
        managed = True
        ordering = ['id']
        db_table = 'subnet'
    
    def __str__(self):
        return self.subnet

class IpAddress(models.Model):
    subnet = models.ForeignKey(Subnet,on_delete=models.CASCADE,to_field='id',db_column="subnet_id",related_name='ip_address',verbose_name='IP子网')
    id = models.AutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(db_index=True, verbose_name='IP地址')
    description = models.CharField(max_length=128, blank=True,verbose_name='IP描述')

    class Meta:
        managed = True
        ordering = ['id']
        db_table = 'ip_address'


