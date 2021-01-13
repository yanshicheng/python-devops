# Generated by Django 2.2.2 on 2021-01-05 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskhistory',
            name='script_cmd',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='执行命令'),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='script_file',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='执行脚本'),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='src_ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='来源IP'),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='src_user',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='操作用户'),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='task_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='脚本返回状态'),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='task_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='任务名称'),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='task_result',
            field=models.TextField(blank=True, null=True, verbose_name='返回结果'),
        ),
        migrations.AlterField(
            model_name='taskhistory',
            name='task_status',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='任务状态'),
        ),
    ]
