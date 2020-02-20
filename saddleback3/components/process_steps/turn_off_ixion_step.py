from opentest.core.process_step import ProcessStep


class TurnOffIxionStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Turn Off Ixion'):
        super(TurnOffIxionStep, self).__init__(process_plan, name)

    def run(self):
        pdu = self.variables['PDU']

        # Power off the Ixion
        pdu.telnet.query('off .a1')

        return self.set_status()
