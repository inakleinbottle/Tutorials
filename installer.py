#! /usr/bin/python3


import os
import sys
import os.path as osp
from subprocess import Popen, PIPE
from threading import Thread

from venv import EnvBuilder


DEFAULT_ENV_DIR = osp.expanduser(osp.join('~', 'PyNotebook'))
    
CONVENIENCE_URL = 'git+https://github.com/inakleinbottle/mathconvenience.git'


class NotebookEnvBuilder(EnvBuilder):
    '''


    '''
    def __init__(self, *args, **kwargs):
        prompt = kwargs.pop('prompt', 'pynb')
        super().__init__(*args, prompt=prompt, **kwargs)

    def reader(self, stream):
        while True:
            s = stream.readline()
            if not s:
                break
            
            sys.stderr.write(s.decode('utf-8'))
            sys.stderr.flush()
        stream.close()

    def pip_install(self, package, flags=tuple()):

        cmd = [context.env_exe, '-m', 'pip', 'install', *flags, package]
        sys.stderr.write('Downloading %s.\n' % package)
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout_reader = Thread(target=self.reader,
                               args=(p.stdout))
        stderr_reader = Thread(target=self.reader,
                               args=(p.stderr))
        stdout_reader.start()
        stderr_reader.start()
        p.wait()
        stdout_reader.join()
        stderr_reader.join()
        sys.stderr.write('Done.')


    def post_setup(self, context):
        self.pip_install('pip', flags=('--upgrade',))
        self.pip_install('numpy')
        self.pip_install('scipy')
        self.pip_install('matplotlib')
        self.pip_install(CONVENIENCE_URL)
        self.pip_install('Jupyter')

        os.mkdir('notebooks')

      

def main():
    path = 'test'

    builder = NotebookEnvBuilder(system_site_packages=False,
                                 clear=True,
                                 symlinks=False,
                                 upgrade=False,
                                 with_pip=True)
    builder.create(path)






if __name__ == '__main__':
    main()
