# Generated by Django 2.2.2 on 2021-01-19 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_platform', '0007_auto_20210116_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCrontab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='定时任务名称')),
                ('task_id', models.CharField(max_length=128, verbose_name='定时任务任务ID')),
                ('run_type', models.CharField(max_length=128, verbose_name='执行方式')),
                ('task_lib', models.CharField(max_length=128, verbose_name='任务类型')),
                ('project', models.CharField(max_length=128, verbose_name='项目名称')),
                ('task_hosts', models.TextField(verbose_name='主机列表')),
                ('task_file', models.CharField(max_length=128, verbose_name='执行脚本')),
                ('hosts_file', models.CharField(max_length=128, verbose_name='hosts文件')),
                ('task_args', models.CharField(max_length=128, verbose_name='参数')),
                ('remarks', models.TextField(verbose_name='定时任务备注')),
            ],
            options={
                'verbose_name': '定时任务',
                'verbose_name_plural': '定时任务',
                'db_table': 'task_platform_crontab',
            },
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='task_type',
            field=models.IntegerField(blank=True, choices=[(0, '脚本任务'), (1, '剧本任务'), (2, '定时任务'), (3, '中间调度')], null=True, verbose_name='执行的任务类型'),
        ),
    ]
