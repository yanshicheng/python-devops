# Generated by Django 2.2.2 on 2021-01-06 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20210105_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskhistory',
            name='run_time',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='脚本运行时长'),
        ),
    ]
