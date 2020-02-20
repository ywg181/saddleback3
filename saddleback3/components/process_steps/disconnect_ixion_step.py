

from opentest.core.process_step import ProcessStep


class DisconnectIxionStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Disconnect Ixion'):
        super(DisconnectIxionStep, self).__init__(process_plan, name)

    def run(self):
        ixion = self.variables['IXION']

        # Close connections of Ixion
        ixion.telnet.close()
        ixion.ssh.close()

        # Remove that OpenTest Variable since the Ixion is off
        self.variables['IXION'] = None

        return self.set_status()
