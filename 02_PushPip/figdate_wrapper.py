import venv
import shutil
import tempfile
import subprocess
import sys

env_dir = tempfile.mkdtemp()
venv.create(env_dir, with_pip=True)
if sys.platform == 'win32':
    install_command = env_dir + "\Scripts\pip.exe install pyfiglet"
    launch_command = env_dir + "\Scripts\python.exe -m figdate "
else:
    install_command = env_dir + "/bin/pip install pyfiglet"
    launch_command = env_dir + "/bin/python3 -m figdate "
if len(sys.argv) > 1:
    launch_command += ' '.join(sys.argv[1:])
subprocess.run(install_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run(launch_command)
shutil.rmtree(env_dir)