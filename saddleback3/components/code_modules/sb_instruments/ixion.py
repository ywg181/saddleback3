import os

from components.code_modules.sb_communication.sb_scp import SbScp


class Ixion:
    def __init__(self, telnet, ssh):
        self.telnet = telnet
        self.ssh = ssh

    def upload_file(self, file_path, remote_directory):
        # Create remote directory just in case it doesn't exist yet
        self.ssh.query(command='mkdir -p {}'.format(remote_directory), timeout=15)

        # Upload the file
        with SbScp(self.ssh.transport) as sb_scp:
            sb_scp.put(file_path, remote_directory)

        # TODO: Actually verify that the upload succeeded and return that file's name instead of cheating
        return os.path.join(remote_directory, os.path.basename(file_path))
