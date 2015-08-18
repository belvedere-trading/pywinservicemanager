from mock import MagicMock, patch
import unittest

class TestFailureActionConfigurationCommandLineType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global FailureActionConfigurationCommandLineType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationCommandLineType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = FailureActionConfigurationCommandLineType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, FailureActionConfigurationCommandLineType, int(1))

    def TestInitWithCorrectParameters(self):
        value = 'CommandLineText'
        t = FailureActionConfigurationCommandLineType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'CommandLineText'
        t = FailureActionConfigurationCommandLineType(value)
        t2 = FailureActionConfigurationCommandLineType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'CommandLineText'
        value2 = 'CommandLineText1'
        t = FailureActionConfigurationCommandLineType(value1)
        t2 = FailureActionConfigurationCommandLineType(value2)
        self.assertNotEquals(t, t2)
