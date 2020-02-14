from opentest.core.process_objects import Measurement
from opentest.core.process_objects import ProcessStatus
from opentest.core.process_step import ProcessStep


class RecordFruInfoStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Record FRU Info'):
        super(RecordFruInfoStep, self).__init__(process_plan, name)

    def run(self):

        telnet_ixion = self.variables['TELNET_IXION']

        fru_info_str = telnet_ixion.query('gsys -k fru info', read_timeout=10)

        measurement_status = ProcessStatus.PASSED
        if '85213281' not in fru_info_str:
            measurement_status = ProcessStatus.FAILED

        self.add_measurement(Measurement(
            'FRU Info',
            fru_info_str,
            status=measurement_status))

        return self.set_status()
