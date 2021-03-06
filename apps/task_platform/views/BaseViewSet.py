import tarfile
import zipfile

from ..models import TaskHistory, ScriptProject, AnsibleProject, AnsibleParameter
from base.views import BaseModelViewSet
from common.get_config_value import get_value
from common.random_str import random_str
from common.file import File
from apps.rbac.auth.jwt_auth import analysis_token
from my_celery.run import app

from django.conf import settings
from celery.result import AsyncResult


class Base(BaseModelViewSet):

    def async_ssh_cmd(self, abs_file, data):
        list = []
        ramdom_str = random_str()
        ansible = get_value("ansible", "abs_ansible_command")
        remote_file_path = f'/tmp/{File.get_file_name(abs_file)}-{ramdom_str}'
        copy_file_cmd = f'{ansible} {data["middle_host"][0]} -m copy -a "src={abs_file} dest={remote_file_path} mode=0777"'
        if File.if_file_endswith(abs_file, '.sh'):
            list.append(
                f'''ansible {",".join(data["target_host"])} -m script -a "{remote_file_path} {data["task_args"]}" && rm -rf {remote_file_path} ''')
        else:
            if not data["task_args"]:
                list.append(f'"ansible-playbook {remote_file_path} -v && rm -rf {remote_file_path}"')
            else:
                list.append(
                    f'''ansible-playbook {remote_file_path} -v -e {data["task_args"]} && rm -rf {remote_file_path}''')
        list.append(remote_file_path)
        return list

    def async_script_cmd(self, abs_file, data):
        ramdom_str = random_str()
        ansible = get_value("ansible", "abs_ansible_command")
        remote_file_path = f'/tmp/{File.get_file_name(abs_file)}-{ramdom_str}'
        copy_file_cmd = f'{ansible} {data["middle_host"][0]} -m copy -a "src={abs_file} dest={remote_file_path} mode=0777"'
        if File.if_file_endswith(abs_file, '.sh'):
            remote_cmd = f'''{ansible} {data["middle_host"][0]} -m shell -a 'ansible {",".join(data["target_host"])} -m script -a "{remote_file_path} {data["task_args"]}" && rm -rf {remote_file_path}' '''
        else:
            if not data["task_args"]:
                remote_cmd = f'{ansible} {data["middle_host"][0]} -m shell -a "ansible-playbook {remote_file_path} -v && rm -rf {remote_file_path}"'
            else:
                remote_cmd = f'''{ansible} {data["middle_host"][0]} -m shell -a 'ansible-playbook {remote_file_path} -v -e {data["task_args"]} && rm -rf {remote_file_path}' '''
        return f'{copy_file_cmd}&&{remote_cmd}'

    def ssh_cmd(self, abs_file_path, data):
        list = []
        ramdom_str = random_str()
        file_name = abs_file_path.split('/')[-1]
        remote_file_path = f'/tmp/{file_name}-{ramdom_str}'
        ''' 调用 celery paramiko'''
        if File.if_file_endswith(file_name, '.sh'):
            command = f'bash {remote_file_path}  {data["task_args"]} && rm -rf {remote_file_path}'
        else:
            command = f'python {remote_file_path} {data["task_args"]} && rm -rf {remote_file_path}'
        list.append(command)
        list.append(remote_file_path)
        return list

    def ansible_cmd(self, abs_file_path, data):
        ansible = get_value("ansible", "abs_ansible_command")
        ansible_playbook = get_value("ansible", "abs_playbook_command")
        if File.if_file_endswith(abs_file_path, '.sh'):
            return f"{ansible} {','.join(data['task_host_list'])} -m script -a '{abs_file_path} {data['task_args']}'"
        elif File.if_file_endswith(abs_file_path, '.py'):
            ramdom_str = random_str()
            file_name = abs_file_path.split('/')[-1]
            remote_file_path = f'/tmp/{file_name}-{ramdom_str}'
            copy_file_cmd = f'ansible {",".join(data["task_host_list"])} -m copy -a "src={abs_file_path} dest={remote_file_path} mode=766" '
            exec_cmd = f'ansible {",".join(data["task_host_list"])} -m shell -a "chdir=/tmp/ .{remote_file_path} {data["task_args"]} && rm -f {remote_file_path}"  '
            return f'{copy_file_cmd} && {exec_cmd}'
        elif File.if_file_endswith(abs_file_path, '.yaml') or File.if_file_endswith(abs_file_path, '.yml'):
            if data['hosts_file']:
                if File.if_file_exists(get_value('ansible', 'ansible_host_path')):
                    hosts_file_path = get_value('ansible', 'ansible_host_path')
                else:
                    hosts_file_path = File.get_join_path(get_value('ansible', 'ansible_host_path'), data['hosts_file'])
            else:
                hosts_file_path = data['hosts_file']
            if File.if_file_exists(abs_file_path):
                if not hosts_file_path and not data['task_args']:
                    return f'{ansible_playbook} {abs_file_path} -v  '
                elif not hosts_file_path:
                    return f'{ansible_playbook} {abs_file_path} -v -e {data["task_args"]}'
                elif not data['task_args']:
                    return f'{ansible_playbook} {abs_file_path} -v -i {hosts_file_path}'
                else:
                    return f'{ansible_playbook} {abs_file_path} -v -i {hosts_file_path} -e {data["task_args"]}'

    def playbook_cmd(self, abs_file, data):
        res = {'status': True, 'data': '', 'script_file': ''}
        try:
            playbook_command = get_value("ansible", "abs_playbook_command")
            if data['host_file']:
                if File.if_file_exists(get_value('ansible', 'ansible_host_path')):
                    hosts_file_path = get_value('ansible', 'ansible_host_path')
                else:
                    hosts_file_path = File.get_join_path(get_value('ansible', 'ansible_host_path'), data['host_file'])
            else:
                hosts_file_path = data['host_file']
            if data['parameter_id']:
                par_obj = AnsibleParameter.objects.filter(id=data['parameter_id']).first()
            else:
                par_obj = None
            if not hosts_file_path and not par_obj:
                return f'{playbook_command} {abs_file} -v  '
            elif not hosts_file_path:
                return f'{playbook_command} {abs_file}  -v -e {par_obj.param}'
            elif not par_obj:
                return f'{playbook_command} {abs_file} -v -i {hosts_file_path}'
            else:
                return f'{playbook_command} {abs_file} -v -i {hosts_file_path} -e {par_obj.param}'
        except Exception as e:
            res['status'] = False
            res['data'] = str(e)
            return res

    def __abs_file(self, type, project, file):
        if type == 'playbook':
            return File.get_join_path(settings.TASK_PLAYBOOK_DIR, project, file)
        elif type == 'script':
            # if source:
            return File.get_join_path(settings.TASK_SCRIPT_DIR, project, file)

    def record_log(self, request, task_name, abs_file, result_id, task_host_list, task_type, run_type):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        run_type_id = 0 if run_type == 'ansible' else 1
        result_status = AsyncResult(id=result_id, app=app)
        log_dic = {
            'src_user': self.get_user(request),
            'src_ip': ip,
            'task_name': task_name,
            'task_id': result_id,
            'script_file': abs_file,
            'task_status': result_status,
            'task_type': task_type,
            'task_host': task_host_list,
            'run_type': run_type_id
        }
        print(log_dic)
        history_obj = TaskHistory.objects.create(**log_dic)
        history_obj.save()
        print('ok')

    def script_save(self, data):
        res_dict = {'status': True, 'data': ''}
        script_file = data['sctiptFile']
        project_obj = ScriptProject.objects.filter(id=data['project']).first()
        abs_file_path = File.get_join_path(settings.TASK_SCRIPT_DIR, project_obj.path, script_file.name)
        try:
            if script_file.name.endswith('.sh') or script_file.name.endswith('.py'):
                if File.if_dir_exists(abs_file_path):
                    res_dict['status'] = False
                    res_dict['data'] = '脚本文件已经存在请检查后在上传!。'
                    return res_dict
            else:
                res_dict['status'] = False
                res_dict['data'] = '上传文件格式错误, 只支持.sh/.py结尾脚本。'
                return res_dict
            with open(abs_file_path, 'wb') as f:
                for chunk in script_file.chunks():
                    f.write(chunk)
                f.flush()
            res_dict['data'] = script_file.name
        except Exception as e:
            if File.if_file_exists(abs_file_path):
                File.rm_dir(abs_file_path)
            res_dict['status'] = False
            res_dict['data'] = str(e)
        return res_dict

    def playbook_save(self, data):
        try:
            script_file = data['sctiptFile']
            project_obj = AnsibleProject.objects.filter(id=data['project']).first()
            if script_file.name.endswith('.yaml'):
                abs_file_path = File.get_join_path(settings.TASK_PLAYBOOK_DIR, project_obj.path, script_file.name)
                if File.if_dir_exists(abs_file_path):
                    return f'{project_obj.name} 项目中已经存在此剧本请检查后重试!', False

            elif script_file.name.endswith('.tar.gz'):
                abs_file_path = File.get_join_path(settings.TASK_PLAYBOOK_DIR, project_obj.path, script_file.name)
                if File.if_dir_exists(abs_file_path.split('.tar.gz')[0]):
                    return f'{project_obj.name} 项目中已经存在此角色包请检查后重试!', False

            elif script_file.name.endswith('.zip'):
                abs_file_path = File.get_join_path(settings.TASK_PLAYBOOK_DIR, project_obj.path, script_file.name)
                if File.if_dir_exists(abs_file_path.split('.zip')[0]):
                    return f'{project_obj.name} 项目中已经存在此角色包请检查后重试!', False
            else:
                return 'PlayBook 文件上传暂只支持，.yaml/.zip/.tar.gz结尾文件。', False

            # # 保存压缩包或者文件
            with open(abs_file_path, 'wb') as f:
                for chunk in script_file.chunks():
                    f.write(chunk)
                f.flush()
            if abs_file_path.endswith('.tar.gz'):
                return self.__un_tar(abs_file_path)
            if abs_file_path.endswith('.zip'):
                return self.__un_zip(abs_file_path)
            # 文件直接返回file名
            return script_file.name, False
        except Exception as e:
            return str(e), False

    def __un_tar(self, abs_package):
        try:
            # untar zip file"""
            base_dir = abs_package.split('.tar.gz')[0]
            dir_name = File.get_file_name(abs_package).split('.tar.gz')[0]
            tar = tarfile.open(abs_package)
            names = tar.getnames()
            File.create_dirs(base_dir)
            # 因为解压后是很多文件，预先建立同名目录
            for name in names:
                tar.extract(name, base_dir)
            tar.close()
            File.rm_dir(abs_package)
            if File.if_file_exists(File.get_join_path(base_dir, 'deploy.yml')):
                return f'/{dir_name}/deploy.yml', True
            elif File.if_file_exists(File.get_join_path(base_dir, dir_name, 'deploy.yml')):

                return f'/{dir_name}/{dir_name}/deploy.yml', True
            else:
                File.rm_dirs(base_dir)
                return '剧本包格式上传不正确，入口文件格式： 包名/deploy.yml', False
        except Exception:
            File.rm_dir(abs_package)
            return '请检查文件是否损坏，无法解压。', False

    def __un_zip(self, abs_package):
        try:
            # untar zip file"""
            base_dir = abs_package.split('.zip')[0]
            dir_name = File.get_file_name(abs_package).split('.zip')[0]
            zip_file = zipfile.ZipFile(abs_package)
            File.rm_dir(base_dir)
            # 因为解压后是很多文件，预先建立同名目录
            for names in zip_file.namelist():
                zip_file.extract(names, base_dir)
            zip_file.close()
            File.rm_dir(abs_package)
            if File.if_file_exists(File.get_join_path(base_dir, 'deploy.yml')):
                return f'/{dir_name}/deploy.yml', True
            elif File.if_file_exists(File.get_join_path(base_dir, dir_name, 'deploy.yml')):
                return f'/{dir_name}/{dir_name}/deploy.yml', True
            else:
                File.rm_dirs(base_dir)
                return '剧本包格式上传不正确，入口文件格式： 包名/deploy.yml', False
        except Exception:
            File.rm_dir(abs_package)
            return '请检查文件是否损坏，无法解压。', False

    def get_user(self, request):
        if analysis_token(request)['user_info']['username']:
            return analysis_token(request)['user_info']['username']
        else:
            return None
