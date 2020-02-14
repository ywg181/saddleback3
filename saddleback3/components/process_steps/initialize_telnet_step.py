from components.code_modules.sb_communication.sb_telnet import SbTelnet
from opentest.core.process_step import ProcessStep


class InitializeTelnetStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Initialize Telnet'):
        super(InitializeTelnetStep, self).__init__(process_plan, name)

    def run(self):

        telnet_ixion = SbTelnet(address='192.168.5.253',
                                port=7001,
                                read_terminal_character=r'\[root@mfg-saddleback ~\]#',
                                write_terminal_character='\n',
                                default_timeout=3)

        telnet_pdu = SbTelnet(address='192.168.5.253',
                              port=7008,
                              read_terminal_character=r'Switched CDU:',
                              write_terminal_character='\n',
                              default_timeout=3)

        # Open connection to the PDU first
        telnet_pdu.open()

        # Log in the PDU
        telnet_pdu.query('', read_terminal_character=r'Username:')
        telnet_pdu.query('admn', read_terminal_character=r'Password:')
        telnet_pdu.query('admn')

        # Power Cycle Ixion
        # telnet_pdu.query('off .a1')
        telnet_pdu.query('on .a1')

        # Open connection to the (now turned on) Ixion
        telnet_ixion.open()

        # Wait until it's done booting
        telnet_ixion.query('', read_timeout=300)

        # Save these Telnet objects for future steps to use!
        self.variables['TELNET_IXION'] = telnet_ixion
        self.variables['TELNET_PDU'] = telnet_pdu

        return self.set_status()
