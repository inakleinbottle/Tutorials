#! /usr/bin/python3


import os
import sys
import os.path as osp
from subprocess import Popen, PIPE
from threading import Thread

from venv import EnvBuilder


DEFAULT_ENV_DIR = osp.expanduser(osp.join('~', 'Documents', 'PyNotebook'))
    
CONVENIENCE_URL = 'git+https://github.com/inakleinbottle/mathconvenience.git'

def get_convenience(ex):
    from urllib.request import urlopen
    from tempfile import TemporaryDirectory
    from zipfile import ZipFile
    from io import BytesIO
    
    url = 'https://github.com/inakleinbottle/mathconvenience/archive/master.zip'
    Zip = ZipFile(BytesIO(urlopen(url).read()))
    with TemporaryDirectory() as tempdir:
        Zip.extractall(tempdir)
        pip_install(ex, osp.join(tempdir, 'mathconvenience-master'))
        

def reader(stream):
        while True:
            s = stream.readline()
            if not s:
                break
            
            sys.stderr.write(s.decode('utf-8'))
            sys.stderr.flush()
        stream.close()

def pip_install(ex, *package, flags=tuple()):
        cmd = [ex, '-m', 'pip', 'install', *flags, *package]
        sys.stderr.write('Downloading and installing %s.\n' %
                         ', '.join(package))
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout_reader = Thread(target=reader,
                               args=(p.stdout,))
        stderr_reader = Thread(target=reader,
                               args=(p.stderr,))
        stdout_reader.start()
        stderr_reader.start()
        p.wait()
        stdout_reader.join()
        stderr_reader.join()
        sys.stderr.write('Done.\n')


class NotebookEnvBuilder(EnvBuilder):

    def __init__(self, *args, **kwargs):
        prompt = kwargs.pop('prompt', 'pynb')
        super().__init__(*args, prompt=prompt, **kwargs)

    def post_setup(self, context):
        pip_install(context.env_exe, 'pip', flags=('--upgrade',))
        pip_install(context.env_exe, 'numpy', 'scipy', 'matplotlib','Jupyter')

        try:
            self.pip_install(context.env_exe, CONVENIENCE_URL)
        except:
            get_convenience(context.env_exe)
            

      

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
