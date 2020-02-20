from components.process_steps.disconnect_ixion_step import DisconnectIxionStep
from components.process_steps.disconnect_pdu_step import DisconnectPduStep
from components.process_steps.initialize_instruments_step import InitializeInstrumentsStep
from components.process_steps.ixion_scp_test_step import IxionScpTestStep
from components.process_steps.populate_reporter_variables_default_step import \
    PopulateReporterVariablesDefaultStep
from components.process_steps.record_fru_info_step import RecordFruInfoStep
from components.process_steps.record_gsys_version_step import RecordGsysVersionStep
from components.process_steps.turn_off_ixion_step import TurnOffIxionStep
from opentest.core.process_plan import ProcessPlan


class MainProcessPlan(ProcessPlan):

    def create_process_plan(self):
        my_plan = [
            # Setup
            PopulateReporterVariablesDefaultStep(self),
            InitializeInstrumentsStep(self),

            # Main
            RecordFruInfoStep(self),
            RecordGsysVersionStep(self),
            IxionScpTestStep(self),

            # Cleanup
            DisconnectIxionStep(self),
            TurnOffIxionStep(self),
            DisconnectPduStep(self),

        ]

        return my_plan
