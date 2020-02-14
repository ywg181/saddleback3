from opentest.core.process_step import ProcessStep


class TurnOffPduStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Turn Off PDU'):
        super(TurnOffPduStep, self).__init__(process_plan, name)

    def run(self):
        telnet_pdu = self.variables['TELNET_PDU']

        telnet_pdu.query('off .a1')

        return self.set_status()
