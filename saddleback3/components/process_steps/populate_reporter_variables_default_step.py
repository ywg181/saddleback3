"""Hardcodes some Reporter Values to enable Reporting for the plan

MEANT TO BE USED FOR THE DEMO PLAN, AS A NORMAL PROJECT WILL NEED TO >NOT< HARDCODE THESE VALUES

"""
import time

from opentest.core.process_step import ProcessStep


class PopulateReporterVariablesDefaultStep(ProcessStep):
    def __init__(self, process_plan, name='Populate Reporter Variables'):
        super(PopulateReporterVariablesDefaultStep, self).__init__(process_plan, name)

    def run(self):
        self.set_reporter_variable('manufacturer', 'Default Manufacturer')
        self.set_reporter_variable('site', 'Default Site')
        self.set_reporter_variable('platform_name', 'Default Product Family')
        self.set_reporter_variable('business_group', 'Default Business Group')
        self.set_reporter_variable('assembly_part_type', 'Default Part Type')
        self.set_reporter_variable('assembly_mpn', 'Default MPN')
        self.set_reporter_variable('test_step', 'Default Test Step')
        self.set_reporter_variable('work_order', 'Default Work Order')
        self.set_reporter_variable('work_flow', 'Default Work Flow')
        self.set_reporter_variable('router', 'Default Router')
        self.set_reporter_variable('build_id', 'Default Build ID')
        self.set_reporter_variable('build_type', 'Default Build Type')
        self.set_reporter_variable('rma_number', 'Default RMA Number')
        self.set_reporter_variable('log_file_path', 'Default Log File Path')
        self.set_reporter_variable('process_group', 'Default Process Group')
        self.set_reporter_variable('product_name', 'RZB')
        self.set_reporter_variable('operator_name', 'Operator')
        self.set_reporter_variable('otc_tester_name', 'DefaultTester')
        self.set_reporter_variable('otc_tester_secret', 'DefaultSecret')
        self.set_reporter_variable('test_log_file', 'OpenTestDebugLog')

        self.set_reporter_variable('software_version', '0.0.1')
        self.set_reporter_variable('assembly_gpn', 'TODO-PN')

        app_config = self.get_global_variable('app_config')
        app_config.set('Global', 'operatorName', 'Operator')

        # Does not count Daylight Saving Time
        utc_offset = -time.timezone / 3600
        self.set_reporter_variable('utcoffset', utc_offset)

        if True:
            print('hey')
            print('hey')
            print('hey')

        return self.set_status()
