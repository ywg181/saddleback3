from components.code_modules.sb_communication.sb_ssh import SbSsh
from opentest.core.process_objects import Measurement, Spec
from opentest.core.process_objects import ProcessStatus
from opentest.core.process_step import ProcessStep


class RecordFruInfoStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Record FRU Info'):
        super(RecordFruInfoStep, self).__init__(process_plan, name)

    def run(self):

        ixion = self.variables['IXION']

        fru_info_str = ixion.ssh.query('gsys -k fru info', timeout=10).stdout

        # value = 'hello world this should fail'
        # expected_value = 'Hello World'
        #
        # self.add_data(
        #     name='Sentence we read',
        #     value=value,
        #     spec=Spec('==', expected_value))

        self.add_measurement(Measurement(
            'FRU Info',
            fru_info_str))

        return self.set_status()
