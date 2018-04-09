from django.db import models

# Create your models here.

class Server(models.Model):
    asset = models.OneToOneField('Asset')
    hostname = models.CharField(max_length=128, unique=True, verbose_name='服务器名称')
    hostuser = models.CharField(max_length=32, blank=True,null=True, verbose_name='服务器账号')
    hostpass = models.CharField(max_length=64, blank=True,null=True, verbose_name='服务器密码')
    SN = models.CharField(max_length=64, blank=True,null=True,db_index=True, verbose_name='SN号')
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField(max_length=64, null=True, blank=True, verbose_name='型号')
    manage_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name='管理IP')
    os_platform = models.CharField(max_length=16, null=True, blank=True,verbose_name='系统')
    os_vsersion = models.CharField(max_length=32, null=True, blank=True, verbose_name='系统版本')
    create_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name_plural = '服务器信息表'

    def __str__(self):
        return self.hostname


class CPU(models.Model):
    cpu_count = models.IntegerField(null=True, blank=True, verbose_name='CPU个数')
    cpu_physical_count = models.IntegerField(null=True, blank=True, verbose_name='CPU物理个数')
    cpu_model = models.CharField(max_length=128, null=True, blank=True, verbose_name='CPU型号')
    server_obj = models.ForeignKey('Server', related_name='cpu')

    def __str__(self):
        return self.cpu_model
    class Meta:
        verbose_name_plural='CPU信息'


class Memory(models.Model):
    #MemTotal = models.CharField(max_length=64,blank=True,null=True, verbose_name='内存容量')
    slot = models.CharField(max_length=32,blank=True,null=True, verbose_name='插槽位')
    manufacturer = models.CharField(max_length=32, null=True, blank=True, verbose_name='制造商')
    model = models.CharField(max_length=64,blank=True,null=True, verbose_name='型号')
    capacity = models.FloatField(null=True, blank=True, verbose_name='容量')
    sn = models.CharField(max_length=64, null=True, blank=True, verbose_name='SN号')
    speed = models.CharField(max_length=16, null=True, blank=True, verbose_name='速度')
    server_obj = models.ForeignKey('Server', related_name='memory')

    class Meta:
        verbose_name_plural = '内存信息'

    def __str__(self):
        return self.capacity

class Disk(models.Model):
    slot = models.CharField(max_length=32, null=True, blank=True, verbose_name='插槽')
    capacity = models.CharField(max_length=64,null=True,blank=True,verbose_name='容量')
    diskname = models.CharField(max_length=32,null=True,blank=True,verbose_name='分区')
    model = models.CharField(max_length=32, null=True, blank=True, verbose_name='型号')
    pd_type = models.CharField(max_length=32, null=True, blank=True, verbose_name='类型')
    server_obj = models.ForeignKey('Server', related_name='disk')

    class Meta:
        verbose_name_plural = '硬盘信息'

    def __str__(self):
        return self.capacity
        #return self.capacity


class Nic(models.Model):
    name = models.CharField(max_length=128, verbose_name='网卡名称')
    hwaddr = models.CharField(max_length=64, verbose_name='网卡的max地址')
    ipaddrs = models.CharField(max_length=256, verbose_name='IP地址')
    netmask = models.CharField(max_length=64, verbose_name='掩码')
    up = models.BooleanField(default=False)
    server_obj = models.ForeignKey('Server', related_name='NIC')

    class Meta:
        verbose_name_plural = '网卡信息'

    def __str__(self):
        return self.ipaddrs


class BusinessUnit(models.Model):
    name = models.CharField(max_length=64,verbose_name='业务线')
    cantact = models.ForeignKey('UserGroup', verbose_name='业务联系人', related_name='c')
    manage = models.ForeignKey('UserGroup', verbose_name='系统管理员', related_name='m')

    class Meta:
        verbose_name_plural = '业务线表'

    def __str__(self):
        return self.name


class IDC(models.Model):
    name = models.CharField(max_length=32, verbose_name='机房名称')
    floor = models.IntegerField('楼层', default=1)
    contact = models.CharField(max_length=32, verbose_name='联系人')
    call = models.PositiveIntegerField(verbose_name='电话')

    class Meta:
        verbose_name_plural = '机房'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签', max_length=32, unique=True)

    class Meta:
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='用户组名称')
    users = models.ManyToManyField('UserProfile',verbose_name='用户')

    class Meta:
        verbose_name_plural = '用户组'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    name = models.CharField(max_length=32, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=32, verbose_name='座机')
    mobile = models.CharField(max_length=32, verbose_name='手机')
    wiexin = models.CharField(max_length=64, null=True, blank=True, verbose_name='微信')

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.name


class AdminInfo(models.Model):
    user_info = models.OneToOneField("UserProfile")
    username = models.CharField(max_length=64, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')

    class Meta:
        verbose_name_plural = 'cmdb系统管理员'

    def __str__(self):
        return self.user_info.name



class NetWorkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    management_ip = models.CharField(max_length=64, blank=True, null=True, verbose_name='管理IP')
    vlan_ip = models.CharField(max_length=64, blank=True, null=True, verbose_name='VLANIP')
    intranet_ip = models.CharField(max_length=128, blank=True, null=True, verbose_name='内网IP')
    sn = models.CharField(max_length=64, unique=True, verbose_name='SN号')
    manufacture = models.CharField(max_length=128, unique=True, verbose_name='制造商')
    model = models.CharField(max_length=128, unique=True, verbose_name='型号')
    port_num = models.SmallIntegerField(null=True, blank=True, verbose_name='端口个数')
    device_detail = models.CharField(max_length=255, unique=True, verbose_name='详细配置')

    class Meta:
        verbose_name_plural = '网络设备信息'

    def __str__(self):
        return self.model


class Asset(models.Model):
    device_type_choices = (
        (1, '服务器'),
        (2, '交换机'),
        (3, '防火墙'),
    )
    device_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )
    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)

    cabinet_num = models.CharField(max_length=30, null=True, blank=True, verbose_name='机柜号')
    cabinet_order = models.CharField(max_length=30, null=True, blank=True, verbose_name='机柜内部序号')

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name='属于的业务线', null=True, blank=True)

    tag = models.ManyToManyField('Tag')

    latest_date = models.DateField(null=True, verbose_name='修改时间')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '资产表'

    def __str__(self):
        return "%s%s:%s:%s"%(self.idc.name,self.cabinet_num,self.cabinet_order, self.business_unit.name)


class AssetRecord(models.Model):
    asset_obj = models.ForeignKey('Asset', related_name='ar')
    content = models.TextField(null=True, blank=True, verbose_name='变更内容')
    creator = models.ForeignKey('UserProfile', null=True, blank=True, verbose_name='变更人')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '资产变更信息表'

    def __str__(self):
        return "%s-%s-%s" % (self.asset_obj.idc.name, self.asset_obj.cabinet_num, self.asset_obj.cabinet_order)


class Error_Log(models.Model):
    asset_obj = models.ForeignKey('Asset', null=True, blank=True)
    title = models.CharField(max_length=16, verbose_name='错误标题')
    content = models.TextField(verbose_name='错误信息')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '错误信息表'

    def __str__(self):
        return "%s-%s" % (self.title, self.create_at)
