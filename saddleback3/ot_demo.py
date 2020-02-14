import sys

import common_ot
from opentest.utils.py3util import execfile

if __name__ == "__main__":
    # pylint: disable-msg=invalid-name
    extra_test_flags = sys.argv[1:]
    sys.argv = [
        sys.argv[0],
        './config/demo.cfg',
    ]
    sys.argv += extra_test_flags

    print(sys.version_info)
    server_executable = common_ot.prepare_server()
    execfile(server_executable)
