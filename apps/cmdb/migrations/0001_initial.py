# Generated by Django 2.2.2 on 2021-01-01 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('device_status_id', models.IntegerField(choices=[(1, '上线'), (2, '在线'), (3, '离线'), (4, '下架')], default=1, verbose_name='设备状态')),
                ('cabinet_num', models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜号')),
                ('cabinet_order', models.CharField(blank=True, max_length=30, null=True, verbose_name='机柜中序号')),
                ('latest_date', models.DateTimeField(auto_now=True, verbose_name='最近同步日期')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '资产表',
                'verbose_name_plural': '资产表',
                'db_table': 'cmdb_asset',
            },
        ),
        migrations.CreateModel(
            name='DeviceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='设备种类')),
                ('pid', models.IntegerField(blank=True, null=True, verbose_name='是否为主菜单')),
            ],
            options={
                'verbose_name': '设备种类',
                'verbose_name_plural': '设备种类',
                'db_table': 'cmdb_device_category',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='IDC名称')),
                ('position', models.CharField(max_length=32, verbose_name='设备位置')),
            ],
            options={
                'verbose_name': '业务线',
                'verbose_name_plural': '机房表',
                'db_table': 'cmdb_idc',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='标签')),
            ],
            options={
                'verbose_name': '标签表',
                'verbose_name_plural': '标签表',
                'db_table': 'cmdb_tag',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='联系人姓名')),
                ('email', models.EmailField(max_length=254, verbose_name='联系人邮箱')),
                ('phone', models.CharField(max_length=32, verbose_name='联系人座机')),
                ('mobile', models.CharField(max_length=32, verbose_name='联系人手机号')),
            ],
            options={
                'verbose_name': '设备联系人表',
                'verbose_name_plural': '设备联系人表',
                'db_table': 'cmdb_user',
            },
        ),
        migrations.CreateModel(
            name='UserGrop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='联系人组')),
                ('remark', models.CharField(blank=True, max_length=128, null=True, verbose_name='联系人组备注')),
                ('users', models.ManyToManyField(to='cmdb.UserProfile')),
            ],
            options={
                'verbose_name': '联系人组',
                'verbose_name_plural': '联系人表',
                'db_table': 'cmdb_user_group',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=128, unique=True, verbose_name='主机名')),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理ip')),
                ('os_platform', models.CharField(blank=True, max_length=16, null=True, verbose_name='操作系统')),
                ('os_version', models.CharField(blank=True, max_length=16, null=True, verbose_name='操作系统版本')),
                ('sn', models.CharField(blank=True, db_index=True, max_length=64, null=True, verbose_name='SN号')),
                ('manufacturer', models.CharField(blank=True, max_length=128, null=True, verbose_name='制造商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('cpu_count', models.IntegerField(blank=True, null=True, verbose_name='CPU个数')),
                ('cpu_physical_count', models.IntegerField(blank=True, null=True, verbose_name='CPU物理个数')),
                ('cpu_model', models.CharField(blank=True, max_length=256, null=True, verbose_name='CPU型号')),
                ('latest_date', models.DateField(blank=True, null=True, verbose_name='更新时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('asset_obj', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='server', to='cmdb.Asset', verbose_name='所属资产')),
            ],
            options={
                'verbose_name': '服务器表',
                'verbose_name_plural': '服务器表',
                'db_table': 'cmdb_server',
            },
        ),
        migrations.CreateModel(
            name='NetworkDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(blank=True, max_length=64, null=True, verbose_name='名称')),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('vlan_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='VlanIp')),
                ('intranet_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='内网ip')),
                ('sn', models.CharField(max_length=64, unique=True, verbose_name='SN号')),
                ('manufacture', models.CharField(blank=True, max_length=128, null=True, verbose_name='制造商')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='型号')),
                ('port_num', models.SmallIntegerField(blank=True, null=True, verbose_name='端口个数')),
                ('device_detail', models.TextField(blank=True, null=True, verbose_name='设置详细配置')),
                ('latest_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('asset_obj', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cmdb.Asset', verbose_name='所属资产')),
            ],
            options={
                'verbose_name': '网络设备表',
                'verbose_name_plural': '网络设备表',
                'db_table': 'cmdb_network_device',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='网卡名称')),
                ('hwaddr', models.CharField(blank=True, max_length=64, null=True, verbose_name='网卡mac地址')),
                ('netmask', models.GenericIPAddressField(blank=True, null=True, verbose_name='子网掩码')),
                ('ipaddress', models.GenericIPAddressField(blank=True, null=True, verbose_name='ip地址')),
                ('broadcast', models.GenericIPAddressField(blank=True, null=True, verbose_name='广播地址')),
                ('up', models.BooleanField(default=False, verbose_name='网卡状态')),
                ('latest_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('server_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nic_list', to='cmdb.Server', verbose_name='所属服务器')),
            ],
            options={
                'verbose_name': '网卡表',
                'verbose_name_plural': '网卡表',
                'db_table': 'cmdb_network',
            },
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(max_length=32, verbose_name='插槽位')),
                ('manufacturer', models.CharField(blank=True, max_length=32, null=True, verbose_name='制造商')),
                ('model', models.CharField(max_length=128, verbose_name='型号')),
                ('capacity', models.FloatField(blank=True, null=True, verbose_name='容量')),
                ('sn', models.CharField(blank=True, max_length=64, null=True, verbose_name='内存SN号')),
                ('speed', models.CharField(blank=True, max_length=16, null=True, verbose_name='速度')),
                ('latest_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('server_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memory', to='cmdb.Server', verbose_name='所属服务器')),
            ],
            options={
                'verbose_name': '内存表',
                'verbose_name_plural': '内存表',
                'db_table': 'cmdb_memory',
            },
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot', models.CharField(blank=True, max_length=8, null=True, verbose_name='插槽位')),
                ('model', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘型号')),
                ('capacity', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁盘容量GB')),
                ('pd_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁盘类型')),
                ('latest_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('server_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disk', to='cmdb.Server', verbose_name='所属服务器')),
            ],
            options={
                'verbose_name': '硬盘表',
                'verbose_name_plural': '硬盘表',
                'db_table': 'cmdb_disk',
            },
        ),
        migrations.CreateModel(
            name='CloudServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance_id', models.CharField(blank=True, max_length=64, null=True, verbose_name='实例ID')),
                ('instance_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='实例名称')),
                ('instance_type', models.CharField(blank=True, max_length=64, null=True, verbose_name='实例类型')),
                ('manage_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='管理IP')),
                ('cpu', models.IntegerField(blank=True, null=True, verbose_name='CPU')),
                ('memory', models.IntegerField(blank=True, null=True, verbose_name='内存')),
                ('intranet_ip', models.CharField(blank=True, max_length=1024, null=True, verbose_name='内网IP')),
                ('public_ip', models.CharField(blank=True, max_length=1024, null=True, verbose_name='内网IP')),
                ('os_version', models.CharField(blank=True, max_length=64, null=True, verbose_name='系统版本')),
                ('security_groupids', models.CharField(blank=True, max_length=1024, null=True, verbose_name='安全组')),
                ('created_time', models.DateTimeField(blank=True, null=True, verbose_name='创建时间')),
                ('expired_time', models.DateTimeField(blank=True, null=True, verbose_name='到期时间')),
                ('latest_date', models.DateField(blank=True, null=True, verbose_name='更新时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='信息创建时间')),
                ('asset_obj', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cloudserver', to='cmdb.Asset', verbose_name='所属资产')),
            ],
            options={
                'verbose_name': '云服务器表',
                'verbose_name_plural': '云服务器表',
                'db_table': 'cmdb_cloud_server',
            },
        ),
        migrations.CreateModel(
            name='CloudDisk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disk_type', models.CharField(blank=True, max_length=128, null=True, verbose_name='磁盘类型')),
                ('disk_id', models.CharField(blank=True, max_length=32, null=True, verbose_name='磁盘ID')),
                ('capacity', models.IntegerField(blank=True, null=True, verbose_name='磁盘容量')),
                ('latest_date', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('server_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clouddisk', to='cmdb.CloudServer', verbose_name='所属云服务器')),
            ],
            options={
                'verbose_name': '云磁盘',
                'verbose_name_plural': '云磁盘',
                'db_table': 'cmdb_cloud_disk',
            },
        ),
        migrations.CreateModel(
            name='BusinessUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True, verbose_name='业务线')),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c', to='cmdb.UserGrop', verbose_name='业务联系人')),
            ],
            options={
                'verbose_name': '业务线',
                'verbose_name_plural': '业务线',
                'db_table': 'cmdb_businessUnit',
            },
        ),
        migrations.CreateModel(
            name='AssetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='更新标题')),
                ('content', models.TextField(null=True, verbose_name='变更内容')),
                ('creator', models.CharField(blank=True, max_length=32, null=True, verbose_name='变更人')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('asset_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ar', to='cmdb.Asset', verbose_name='所属资产')),
            ],
            options={
                'verbose_name': '资产更新记录',
                'verbose_name_plural': '资产更新记录',
                'db_table': 'cmdb_asset_record',
            },
        ),
        migrations.CreateModel(
            name='AssetErrorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='错误名称')),
                ('content', models.TextField(verbose_name='错误内容')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('asset_obj', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Asset', verbose_name='所属资产')),
            ],
            options={
                'verbose_name': '资产错误日志',
                'verbose_name_plural': '资产错误日志',
                'db_table': 'cmdb_asset_errorLog',
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='business_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset', to='cmdb.BusinessUnit', verbose_name='所属的业务线'),
        ),
        migrations.AddField(
            model_name='asset',
            name='device_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.DeviceCategory', verbose_name='资产类型'),
        ),
        migrations.AddField(
            model_name='asset',
            name='idc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.IDC', verbose_name='IDC机房'),
        ),
        migrations.AddField(
            model_name='asset',
            name='maintain_groups',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='m', to='cmdb.UserGrop', verbose_name='资产维护组'),
        ),
        migrations.AddField(
            model_name='asset',
            name='tag',
            field=models.ManyToManyField(blank=True, to='cmdb.Tag', verbose_name='资产标签'),
        ),
    ]
