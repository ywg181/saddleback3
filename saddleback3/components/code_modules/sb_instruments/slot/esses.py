import logging
from components.code_modules.sb_instruments.slot.google_instrument import GoogleInstrument


class Essex(GoogleInstrument):
    """This class is used to control the Essex."""
    def __init__(self:
        """Initializes the class.

        Args:
          address: The Essex address if it has ethernet otherwise None
        """
        GoogleInstrument.__init__(self)

    @property
    def communication(self):
        if self._proxy is None:
            logging.debug('Essex xmlrpc N/A, use gsys instead.')
            return None
        return self._proxy

    def set_fan_pwm(self, fan_id, pwm_percent):
        """Set the fan duty cycle.

        Args:
          fan_id: The fan number from 0-2
          pwm_percent: The duty cycle in percent
        Returns:
          returns True is successful otherwise False.
        """
        if self._proxy is None:
            logging.debug('Essex xmlrpc N/A, use gsys instead.')
            return False
        value = self._proxy.set_fan_pwm(fan_id, pwm_percent)
        logging.debug('Essex xmlrpc set_fan_pwm({}, {})= {}'.format(
            fan_id, pwm_percent, value))
        return value

    def get_fan_rpm(self, fan_id):
        """Get the fan rpm.

        Args:
          fan_id: The fan number from 0-2
        Returns:
          returns the RPM of the specified fan.
        """
        if self._proxy is None:
            logging.debug('Essex xmlrpc N/A, use gsys instead.')
            return 0
        value = self._proxy.get_fan_rpm(fan_id)
        logging.debug('Essex xmlrpc get_fan_rpm({})= {}'.format(fan_id, value))
        return value

    def get_rev(self):
        """Get the Essex rev.

        Returns:
          returns the Essex rev.
        """
        if self._proxy is None:
            logging.debug('Essex xmlrpc N/A, use gsys instead.')
            return None
        value = self._proxy.get_rev()
        logging.debug('Essex xmlrpc get_rev()= {}'.format(value))
        return value
