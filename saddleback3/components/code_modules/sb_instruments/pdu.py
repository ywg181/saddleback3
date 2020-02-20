import time


class Pdu:
    def __init__(self, telnet):
        self.telnet = telnet

    def open(self):
        self.telnet.open()

    def login(self, username='admn', password='admn'):
        self.telnet.query('', read_terminal_character=r'Username:')
        self.telnet.query(username, read_terminal_character=r'Password:')
        self.telnet.query(password)

    def power_cycle_ixion(self):
        self.telnet.query('off .a1')
        time.sleep(2)
        self.telnet.query('on .a1')
