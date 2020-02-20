from opentest.core.process_objects import Spec
from opentest.core.process_step import ProcessStep


class RecordGsysVersionStep(ProcessStep):
    def __init__(self,
                 process_plan,
                 name='Record Gsys Version'):
        super(RecordGsysVersionStep, self).__init__(process_plan, name)

    def run(self):
        ixion = self.variables['IXION']
        gsys_version = ixion.ssh.query('gsys --version').stdout

        gsys_version_label = gsys_version.split('Build label: ')[1].split('\nBuild tool')[0]

        self.add_data(
            'Gsys Version',
            gsys_version_label,
            Spec('==', '6.12-1'))

        return self.set_status()
