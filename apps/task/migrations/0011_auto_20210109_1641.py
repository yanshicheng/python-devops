# Generated by Django 2.2.2 on 2021-01-09 16:41

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_auto_20210107_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskRecycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(blank=True, max_length=50, null=True, verbose_name='脚本类型script/playbook')),
                ('src_user', models.CharField(blank=True, max_length=50, null=True, verbose_name='操作用户')),
                ('source_project', models.CharField(blank=True, max_length=50, null=True, verbose_name='原项目Path')),
                ('source_file', models.CharField(blank=True, max_length=50, null=True, verbose_name='原脚本/包名')),
                ('source_field', django_mysql.models.JSONField(blank=True, default=dict, null=True, verbose_name='原字段')),
                ('path', models.CharField(blank=True, max_length=1024, null=True, verbose_name='回收站中的路径')),
            ],
        ),
        migrations.AddField(
            model_name='ansibleplaybook',
            name='src_user',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='操作用户'),
        ),
        migrations.AddField(
            model_name='taskscript',
            name='src_user',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='操作用户'),
        ),
    ]