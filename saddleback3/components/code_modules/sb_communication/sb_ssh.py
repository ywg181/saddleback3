import logging
import re
import time
from threading import Semaphore

import paramiko

from components.code_modules.sb_communication.i_communication import ICommunication, ICommunicationError, ITimeoutError
from components.code_modules.sb_communication.query_output import QueryOutput

LOGGER = logging.getLogger(__name__)


class SbSsh(ICommunication):

    NUMBER_OF_BYTES_TO_READ = 16384

    def __init__(self,
                 address,
                 port=22,
                 username='root',
                 password='',
                 private_key_file=None,
                 terminal_character='\n',
                 default_timeout=20.0,
                 max_ssh_sessions=10):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.private_key_file = private_key_file
        self.terminal_character = terminal_character
        self.default_timeout = default_timeout
        self.max_ssh_sessions = max_ssh_sessions

        self.session = None
        self.ssh_semaphore = Semaphore(max_ssh_sessions)

    def open(self):
        try:
            self.session = paramiko.SSHClient()
            self.session.load_system_host_keys()
            self.session.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.session.connect(
                hostname=self.address,
                port=self.port,
                username=self.username,
                password=self.password,
                key_filename=self.private_key_file,
                timeout=self.default_timeout)
            LOGGER.debug('Opened SSH connection to %s:%s', self.address, self.port)
        except Exception as ex:  #TODO: Make this less broad, such as NoValidConnectionsError + SSHException + socket.error like in fugu
            raise ICommunicationError(ex)

    def close(self):
        try:
            if self.session:
                self.session.close()
                self.session = None
                LOGGER.debug('Closed SSH connection to %s:%s', self.address, self.port)
        except Exception as ex:  #TODO: Make this less broad, such as NoValidConnectionsError + SSHException + socket.error like in fugu
            raise ICommunicationError(ex)

    @property
    def transport(self):
        return self.session.get_transport()

    def _readline(self, read_function):
        line = b''
        new_char = b''
        while new_char.decode('utf-8', 'ignore') != self.terminal_character:
            line += new_char
            new_char = read_function(1)

        return line.decode('utf-8', 'ignore')

    def _read_buffer(self, channel):
        stdout = ''
        new_stdout = None
        while channel.recv_ready() or (channel.closed and new_stdout != ''):
            new_stdout = channel.recv(self.NUMBER_OF_BYTES_TO_READ).decode('utf-8', 'ignore')
            stdout += new_stdout

        stderr = ''
        new_stderr = None
        while channel.recv_stderr_ready() or (channel.closed and new_stderr != ''):
            new_stderr = channel.recv_stderr(self.NUMBER_OF_BYTES_TO_READ).decode('utf-8', 'ignore')
            stderr += new_stderr

        return stdout, stderr

    def read(self, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        with self.ssh_semaphore:
            with self.transport.open_session(timeout=timeout) as channel:
                channel.settimeout(timeout)
                read_buffer, _ = self._read_buffer(channel)

        self.log_multi_line_output(read_buffer, 'Read')
        return read_buffer

    def read_until(self, expected_regex, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        start_time = time.time()
        read_buffer = ''
        new_buffer = read_buffer
        re_func = re.compile(expected_regex)

        try:
            while re_func(new_buffer) is None:
                new_buffer = self.read(timeout=timeout)
                read_buffer += new_buffer
                # We do timeout ourselves
                current_time = time.time() - start_time
                if current_time > timeout:
                    raise ITimeoutError('Timeout on read_until waiting for {}'.format(expected_regex))
        finally:
            self.log_multi_line_output(read_buffer, 'Read Until {}'.format(expected_regex))

        return read_buffer

    def write(self, command, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        with self.ssh_semaphore:
            with self.transport.open_session(timeout=timeout) as channel:
                # channel.settimeout(timeout)  # TODO: This might be necessary, but apparently not
                channel.send((command + self.terminal_character).encode('utf-8', 'ignore'))
        LOGGER.debug('SSH WRITE >>> %s', command)

    def query(self, command, timeout=None, kill_on_timeout=True, max_number_of_lines=None):
        if timeout is None:
            timeout = self.default_timeout
        command = 'echo $$; {}{}'.format(command, self.terminal_character)
        with self.ssh_semaphore:
            with self.transport.open_session(timeout=timeout) as channel:

                channel.settimeout(timeout)
                channel.exec_command(command.encode('utf-8', 'ignore'))
                LOGGER.debug('SSH QUERY >>> %s', command)
                pid = self._readline(channel.recv)

                stdout = ''
                stderr = ''
                start_time = time.time()
                try:
                    # TODO: We do the timeout ourselves. This is kinda nasty, review later
                    while not channel.exit_status_ready():
                        new_stdout, new_stderr = self._read_buffer(channel)
                        stdout += new_stdout
                        stderr += new_stderr

                        # We do timeout ourselves
                        current_time = time.time() - start_time
                        if current_time > timeout:
                            if kill_on_timeout and pid is not None:
                                self.session.exec_command(('kill -9 {}'.format(pid)).encode('utf-8', 'ignore'), timeout=20)
                            raise ITimeoutError('Timeout on command {}'.format(command))
                    time.sleep(0.01)
                finally:
                    # Empty the buffer
                    # We make sure that we had 2 blank read before exiting
                    # In very fast queries, data racing may occur

                    blank_reads = 0
                    while blank_reads < 1:
                        new_stdout, new_stderr = self._read_buffer(channel)
                        stdout += new_stdout
                        stderr += new_stderr
                        if new_stdout != '' or new_stderr != '':
                            blank_reads = 0
                        else:
                            blank_reads += 1

                        time.sleep(0.1)

                self._log_elapsed_time(command, time.time() - start_time)
                self.log_multi_line_output(stdout, 'Query stdout', max_number_of_lines)
                self.log_multi_line_output(stderr, 'Query stderr', max_number_of_lines)

        exit_code = channel.exit_status
        result = QueryOutput(stdout=stdout, stderr=stderr, exit_code=exit_code)
        return result

    def query_until(self, command, expected_string, timeout=None, write_timeout=None):
        self.write(command=command, timeout=write_timeout)
        return self.read_until(expected_regex=expected_string, timeout=timeout)
