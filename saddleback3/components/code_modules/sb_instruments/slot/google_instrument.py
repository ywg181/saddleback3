class UnitInformation:
    """This class contains properties used by most products."""

    def __init__(self):
        """Initialize the class."""
        self.mfg_name = ""
        self.mfg_timestamp = ""
        self.mfg_time = ""
        self.part_number = ""
        self.serial_number = ""
        self.asset_tab = ""


class GoogleInstrument:
    """This class contains properties common to all Google devices."""

    def __init__(self):
        """Initialize the class"""
        self.fru_search_string = '^.device+name="{}".*$'.format(
            self.__class__.__name__.lower())
        self.validity = False
        self.device_name = None
        self.prd_info = UnitInformation()
        self.brd_info = UnitInformation()
        self.cycle_count = 0
        self.calibration_date = None

        self.devpath = ''
        self.location = None
        self.assembly_mpm = ''

    @property
    def product_type(self):
        """A string property inducating the product type"""
        return self.__class__.__name__
