import subprocess
import os
from string import Template


class PTemplate(Template):
    delimiter = '%'


class NginX:
    def __init__(self, project):
        self._project_name = project
        self._server_name = self._project_name + '.test'
        self._project_dir = os.path.join(
            '/home/lun/Code',
            self._project_name
        )
        self._skeleton = 'skel/nginx.stub'
        self._available = '/etc/nginx/sites-available'
        self._enabled = '/etc/nginx/sites-enabled'

    def make_cfg(self):
        self.save_cfg()
        self.make_symlink()
        self.restart_service()

    def destroy_cfg(self):
        files = {
            'config': os.path.join(self._available, self._server_name),
            'symlink': os.path.join(self._enabled, self._server_name)
        }

        for path in files.values():
            os.remove(path)

        self.restart_service()

    def get_cfg(self):
        return PTemplate(open(self._skeleton).read()).substitute({
            'root': self._project_dir,
            'server_name': self._server_name,
            'project_name': self._project_name
        })

    def save_cfg(self):
        self.mkdirs(self._available)
        dst = os.path.join(self._available, self._server_name)
        with open(dst, 'w') as fd:
            fd.write(self.get_cfg())

    def make_symlink(self):
        self.mkdirs(self._enabled)
        src = os.path.join(self._available, self._server_name)
        dst = os.path.join(self._enabled, self._server_name)
        os.symlink(src, dst)

    def mkdirs(self, directory):
        os.makedirs(directory, mode=0o755, exist_ok=True)

    def restart_service(self):
        # TODO Do not restart if config test fails
        # and do a rollback in parent runtime
        retval = subprocess.run(['nginx', '-t'], stderr=subprocess.PIPE)
        if 'successful' in retval.stderr.decode('utf-8').split('\n')[-2]:
            subprocess.run(
                ['systemctl', 'restart', 'nginx'],
                check=True)
