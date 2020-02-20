from collections import namedtuple

QueryOutput = namedtuple('QueryOutput', ['stdout', 'stderr', 'exit_code'])
QueryOutput.__new__.__defaults__ = (None, 0)
