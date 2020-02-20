import abc

import logging
import threading


class ITimeoutError(Exception):
    """ Query did not finish in time"""


class ICommunicationError(Exception):
    """ Unable to perform query"""


class ICommunication:
    __metaclass__ = abc.ABCMeta
    multi_log_lock = threading.Lock()

    @abc.abstractmethod
    def open(self):
        """The abstract method to open the connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self):
        """The abstract method to close the connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, timeout):
        """The abstract method to read."""
        raise NotImplementedError

    @abc.abstractmethod
    def read_until(self, expected_regex, timeout):
        """The abstract method to read."""
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, command, timeout):
        """The abstract method to write. Receives the command to be
        written."""
        raise NotImplementedError

    @abc.abstractmethod
    def query(self, command, timeout):
        """The abstract method for the query."""
        raise NotImplementedError

    @abc.abstractmethod
    def query_until(self, command, expected_string, timeout):
        """The abstract method for the query."""
        raise NotImplementedError

    @staticmethod
    def _log_elapsed_time(command, elapsed_time):
        logging.debug(
            'COMMAND > %s'
            '>>> TIME ELAPSED > %f',
            command, elapsed_time)

    def log_multi_line_output(self, raw_string, title, max_number_lines=None):
        if not raw_string:
            return

        logger = logging.getLogger(self.__class__.__module__)

        lines = raw_string.splitlines()

        number_lines = len(lines)
        if number_lines > 1:
            if logger.isEnabledFor(logging.DEBUG):
                with self.multi_log_lock:
                    logger.debug('>>> %s ===', title)

                    if max_number_lines is None or number_lines < max_number_lines:
                        for line in lines:
                            logger.debug(line.rstrip())
                    else:
                        # We can't have all the lines
                        # So we will take the max amount of line and have
                        # 50% of those lines be the beginning
                        # The other 50% will be the end of the output.
                        half_max_number_lines = max_number_lines/2
                        for index in range(half_max_number_lines):
                            line = lines[index]
                            logger.debug(line)

                        omitted_lines_count = number_lines - max_number_lines
                        logger.debug('\n\n\n...%i LINES OMITTED...\n\n\n', omitted_lines_count)
                        for index in range(number_lines - half_max_number_lines, number_lines):
                            line = lines[index]
                            logger.debug(line)

                    logger.debug('<<< %s ===', title)
        else:
            logger.debug('%s >>>  %s', title, raw_string.rstrip())
