############################################################
# NOT REAL, DELETE AFTER
############################################################

import os

from opentest.core.process_objects import Measurement
from opentest.core.process_step import ProcessStep


class IxionScpTestStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Ixion SCP Test'):
        super(IxionScpTestStep, self).__init__(process_plan, name)

    def run(self):

        ixion = self.variables['IXION']

        file_path = './hello_world.txt'

        # Python doesn't support the . in paths, so expand it just in case
        full_file_path = os.path.expanduser(file_path)

        uploaded_file_path = ixion.upload_file(full_file_path, '/tmp')

        self.add_measurement(Measurement(
            'Uploaded File Path',
            uploaded_file_path
        ))

        return self.set_status()
