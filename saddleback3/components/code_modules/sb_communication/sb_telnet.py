import logging
import re
import telnetlib
import time

from components.code_modules.sb_communication.i_communication \
    import ICommunication
from components.code_modules.sb_communication.i_communication import \
    ICommunicationError
from components.code_modules.sb_communication.i_communication import \
    ITimeoutError


LOGGER = logging.getLogger(__name__)


class SbTelnet(ICommunication):

    def __init__(self,
                 address,
                 port,
                 read_terminal_character='\n',
                 write_terminal_character='\n',
                 default_timeout=1):
        self.address = address
        self.port = port
        self.read_terminal_character = read_terminal_character
        self.write_terminal_character = write_terminal_character
        self.default_timeout = default_timeout

        self.session = None

    def open(self):
        try:
            self.session = telnetlib.Telnet(self.address, self.port, self.default_timeout)
            LOGGER.debug('Open Telnet Connection to %s:%s', self.address, self.port)
        except Exception as ex:
            raise ICommunicationError(ex)

    def close(self):
        try:
            if self.session:
                self.session.close()
                self.session = None
                #TODO: LOGGING
        except Exception as ex:
            raise ICommunicationError(ex)

    def read(self, timeout=None):
        timeout = timeout if timeout else self.default_timeout

        self.session.timeout = timeout
        read_str = self.session.read_eager().decode('utf-8', 'ignore')
        self.session.timeout = self.default_timeout
        #TODO: LOGGING
        return read_str

    def read_until(self, expected_regex, timeout=None, print_on_the_go=True):
        timeout = timeout if timeout else self.default_timeout

        start_time = time.time()
        read_str = ''
        try:
            while re.search(expected_regex, read_str) is None:
                newly_read_str = self.session.read_eager().decode('utf-8', 'ignore')  #TODO: Maybe use self.read() and have optional logging only
                if print_on_the_go:
                    print(newly_read_str, end='')  #TODO: Maybe use logging here instead of print?
                read_str += newly_read_str
                time.sleep(0.05)

                if time.time() >= start_time + timeout:
                    raise ITimeoutError('Timeout on read_until waiting for {}'.format(expected_regex))
        finally:
            #TODO: LOGGING
            pass

        return read_str

    def write(self, command, timeout=None):
        timeout = timeout if timeout else self.default_timeout

        self.session.timeout = timeout
        self.session.write((command + self.write_terminal_character).encode('utf-8', 'ignore'))
        self.session.timeout = self.default_timeout
        #TODO: LOGGING

    def query(self, command, read_timeout=None, write_timeout=None, print_on_the_go=True, read_terminal_character=None):
        # TODO: REMAKE THIS A BIT PRETTIER

        if not read_timeout:
            read_timeout = self.default_timeout

        if not write_timeout:
            write_timeout = self.default_timeout

        if not read_terminal_character:
            read_terminal_character = self.read_terminal_character

        start_time = time.time()

        self.write(command, write_timeout)
        read_str = self.read_until(expected_regex=read_terminal_character, timeout=read_timeout, print_on_the_go=print_on_the_go)
        read_str = read_str.rstrip()

        self._log_elapsed_time(command, time.time() - start_time)

        return read_str
