from mock import MagicMock, patch
import unittest

class TestFailureActionConfigurationResetPeriodType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        global FailureActionConfigurationResetPeriodType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationResetPeriodType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = FailureActionConfigurationResetPeriodType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, FailureActionConfigurationResetPeriodType, float(1))

    def TestInitWithCorrectParameters(self):
        value = int(1)
        t = FailureActionConfigurationResetPeriodType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = int(1)
        t = FailureActionConfigurationResetPeriodType(value)
        t2 = FailureActionConfigurationResetPeriodType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = int(1)
        value2 = int(2)
        t = FailureActionConfigurationResetPeriodType(value1)
        t2 = FailureActionConfigurationResetPeriodType(value2)
        self.assertNotEquals(t, t2)
