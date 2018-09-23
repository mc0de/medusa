import subprocess


class MySQL:
    """ Command line wrapper for MySQL. """

    def __init__(self, config):
        self._env = subprocess.os.environ.copy()
        self._env['MYSQL_PWD'] = config['MYSQL']['PWD']
        self._user = config['MYSQL']['USER']

    # Returns subprocess.CompletedProcess()
    # h = human readable, because returned cp.stdout is binary
    def execute(self, command, h=False):
        cp = subprocess.run(
            ['mysql', '-u', self._user, '-e', command],
            env=self._env,
            stdout=subprocess.PIPE,
            check=True,
        )

        return cp.stdout.decode('utf-8') if h else cp

    def create_db(self, database):
        return self.execute("CREATE DATABASE {};".format(database))

    def drop_db(self, database):
        return self.execute("DROP DATABASE {};".format(database))
