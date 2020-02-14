from components.process_steps.close_telnet_step import CloseTelnetStep
from components.process_steps.initialize_telnet_step import InitializeTelnetStep
from components.process_steps.populate_reporter_variables_default_step import \
    PopulateReporterVariablesDefaultStep
from components.process_steps.record_fru_info_step import RecordFruInfoStep
from components.process_steps.turn_off_pdu_step import TurnOffPduStep
from opentest.core.process_plan import ProcessPlan


class MainProcessPlan(ProcessPlan):

    def create_process_plan(self):
        my_plan = [
            PopulateReporterVariablesDefaultStep(self),
            InitializeTelnetStep(self),
            RecordFruInfoStep(self),
            TurnOffPduStep(self),
            CloseTelnetStep(self),
        ]

        return my_plan
