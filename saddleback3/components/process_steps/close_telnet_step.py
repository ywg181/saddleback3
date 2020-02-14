from opentest.core.process_step import ProcessStep


class CloseTelnetStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Close Telnet'):
        super(CloseTelnetStep, self).__init__(process_plan, name)

    def run(self):
        telnet_ixion = self.variables['TELNET_IXION']
        telnet_pdu = self.variables['TELNET_PDU']

        telnet_ixion.close()
        telnet_pdu.close()

        self.variables['TELNET_IXION'] = None
        self.variables['TELNET_PDU'] = None

        return self.set_status()
