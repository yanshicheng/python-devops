# 定时任务
import uuid

from .BaseViewSet import Base
from .crontab_def import add_ansible_crontab, add_ssh_crontab
from ..models import TaskCrontab, ScriptFile, AnsiblePlaybook
from ..serializers import TaskCrontabSerializer
from base.response import json_ok_response, json_error_response
from common.file import File

from django.conf import settings

# 实例化
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore())  # 指定存储
scheduler.start()


class TaskCrontabViewSet(Base):
    queryset = TaskCrontab.objects.all().order_by('id')
    serializer_class = TaskCrontabSerializer
    ordering_fields = ('id', 'name',)
    search_fields = ('name',)
    filter_fields = ('id', 'name')

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            if data['task_lib'] == 'script':
                script_obj = ScriptFile.objects.filter(id=data['script_id']).first()
                abs_file = File.get_join_path(settings.TASK_SCRIPT_DIR, script_obj.project.path, script_obj.file_name)
            else:
                script_obj = AnsiblePlaybook.objects.filter(id=data['script_id']).first()
                if script_obj.file_name.endswith('yaml'):
                    abs_file = File.get_join_path(settings.TASK_SCRIPT_DIR, script_obj.project.path,
                                                  script_obj.file_name)
                else:
                    abs_file = f'{File.get_join_path(settings.TASK_SCRIPT_DIR, script_obj.project.path)}{script_obj.file_name}'
            if not File.if_file_exists(abs_file):
                return json_error_response(message='所选文件找不到请检查后重试。')

            if data['run_type'] == 'ansible':
                cmd = self.ansible_cmd(abs_file, data=data)
            else:
                cmd = self.ssh_cmd(abs_file, data)

            # 创建定时任务
            task_id = uuid.uuid4().hex
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            # 创建定时任务扩展表
            TaskCrontab.objects.create(**{
                "name": data['name'],
                "task_id": task_id,
                "run_type": data['run_type'],
                "task_lib": data['task_lib'],
                "project": script_obj.project.name,
                "task_file": script_obj.file_name,
                "task_args": data["task_args"],
                "task_hosts": data["task_host_list"],
                "hosts_file": data["hosts_file"],
                "remarks": data['task_remarks'],
            })

            # 注册定时任务
            history_data = {
                'src_user': self.get_user(request),
                'src_ip': ip,
                'task_type': 2,
                'task_host': data["task_host_list"],
                'task_name': data['name'],
                'crontab_id': task_id,

            }
            print(history_data)
            if data['run_type'] == 'ansible':
                scheduler.add_job(
                    add_ansible_crontab,
                    'cron',
                    args=[cmd, history_data],
                    id=task_id,
                    **data['execution_way'],
                )
            else:
                scheduler.add_job(
                    add_ssh_crontab,
                    'cron',
                    args=[cmd[0], history_data, abs_file, cmd[1]],
                    id=task_id,
                    **data['execution_way'],
                )
            # 注册任务
            register_events(scheduler)
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=str(e))

    def update(self, request, *args, **kwargs):
        try:
            task_status = request.data.get('task_status')
            instance = self.get_object()
            if task_status:
                instance.task_status = True
                scheduler.resume_job(instance.task_id)
                instance.save()
                return json_ok_response(data=f'{instance.name} 任务开启成功')
            else:
                scheduler.pause_job(instance.task_id)
                instance.task_status = False
                instance.save()
                return json_ok_response(data=f'{instance.name} 任务停止成功')
        except Exception as e:
            return json_error_response(message=str(e), )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            scheduler.remove_job(instance.task_id)
            instance.delete()
            return json_ok_response()
        except Exception as e:
            return json_error_response(message=f'ERROR: {str(e)}')
