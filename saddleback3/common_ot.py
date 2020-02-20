import os
import sys


def prepare_server():
    project_root = os.path.dirname(__file__)
    sys.path.append(project_root)
    os.chdir(project_root)

    opentest_path = os.path.join(project_root, 'opentest')
    sys.path.append(opentest_path)

    server_executable = os.path.join('.', 'opentest', 'core', 'server.py')

    return server_executable
