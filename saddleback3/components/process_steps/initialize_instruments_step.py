import time

from components.code_modules.sb_communication.sb_ssh import SbSsh
from components.code_modules.sb_communication.sb_telnet import SbTelnet
from components.code_modules.sb_instruments.ixion import Ixion
from components.code_modules.sb_instruments.pdu import Pdu
from opentest.core.process_step import ProcessStep


class InitializeInstrumentsStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Initialize Telnet'):
        super(InitializeInstrumentsStep, self).__init__(process_plan, name)

    def run(self):

        ixion = Ixion(
            telnet=SbTelnet(
                address='192.168.5.253',
                port=7001,
                read_terminal_character=r'\[root@mfg-saddleback ~\]#',
                write_terminal_character='\n',
                default_timeout=3),
            ssh=SbSsh(
                address='192.168.5.1'))

        pdu = Pdu(
            telnet=SbTelnet(
                address='192.168.5.253',
                port=7008,
                read_terminal_character=r'Switched CDU:',
                write_terminal_character='\n',
                default_timeout=3))

        # Open connection to the PDU first
        pdu.open()

        # Log in the PDU
        pdu.login()

        # Power Cycle Ixion
        pdu.power_cycle_ixion()

        # Use telnet to determine when something is done booting
        ixion.telnet.open()
        ixion.telnet.query('', read_terminal_character=r'\(none\) login:', read_timeout=300)
        ixion.telnet.query('root', read_terminal_character=r'\(none\):~#', read_timeout=300)
        # ixion.telnet.query('', read_terminal_character=r'\(none\):~#', read_timeout=300)

        # Open SSH connection to the (now fully booted) Ixion
        ixion.ssh.open()

        # Save these objects in OpenTest Variables for future use
        self.variables['IXION'] = ixion
        self.variables['PDU'] = pdu

        return self.set_status()
