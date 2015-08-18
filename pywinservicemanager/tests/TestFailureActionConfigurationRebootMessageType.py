from mock import MagicMock, patch
import unittest

class TestFailureActionConfigurationRebootMessageType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        global FailureActionConfigurationRebootMessageType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationRebootMessageType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = FailureActionConfigurationRebootMessageType (value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, FailureActionConfigurationRebootMessageType , int(1))

    def TestInitWithCorrectParameters(self):
        value = 'RebootMessageText'
        t = FailureActionConfigurationRebootMessageType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'RebootMessageText'
        t = FailureActionConfigurationRebootMessageType(value)
        t2 = FailureActionConfigurationRebootMessageType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'RebootMessageText'
        value2 = 'RebootMessage1'
        t = FailureActionConfigurationRebootMessageType(value1)
        t2 = FailureActionConfigurationRebootMessageType(value2)
        self.assertNotEquals(t, t2)
