from opentest.core.process_step import ProcessStep


class DisconnectPduStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Disconnect PDU'):
        super(DisconnectPduStep, self).__init__(process_plan, name)

    def run(self):
        pdu = self.variables['PDU']

        # Close connections of PDU
        pdu.telnet.close()

        # Remove that OpenTest Variable since the Ixion is off
        self.variables['PDU'] = None

        return self.set_status()
