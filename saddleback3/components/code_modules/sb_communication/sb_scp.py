import logging
import os

import scp
from scp import SCPClient

LOGGER = logging.getLogger(__name__)


class SbScp(SCPClient):
    def put(self, files, remote_path=b'.', recursive=False, preserve_times=False):
        # Log that we are putting 1+ file
        LOGGER.debug('UPLOADING FILE(S) %s >>> %s', str(files), str(remote_path))
        # Call the put as normal
        super(SbScp, self).put(
            files=files,
            remote_path=remote_path,
            recursive=recursive,
            preserve_times=preserve_times)

    def _send_recursive(self, files):
        # Normal SCP for list of files
        if len(files) != 1 or not os.path.isdir(files[0]):
            return super(SbScp, self)._send_recursive(files)

        # Custom logic for a list containing a single directory
        base = files[0]
        last_dir = scp.asbytes(base)
        for root, _, fls in os.walk(base):
            # We don't want to create a directory for the root dir
            if root != last_dir:
                self._chdir(last_dir, scp.asbytes(root))

            self._send_files([os.path.join(root, f) for f in fls])
            last_dir = scp.asbytes(root)

        # back out of the directory
        while self._pushed > 0:
            self._send_popd()
