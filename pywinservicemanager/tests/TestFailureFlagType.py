from mock import MagicMock, patch
import unittest

class TestFailureFlagType(unittest.TestCase):
    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global FailureFlagType
        from pywinservicemanager.ConfigurationTypes import FailureFlagType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = FailureFlagType(value)
        self.assertEquals(t.StringValue(), bool(value))
        self.assertEquals(t.Win32Value(), bool(value))

    def TestInitWithParametersOfNotTypeBool(self):
        self.assertRaises(ValueError, FailureFlagType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = True
        t = FailureFlagType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = True
        t = FailureFlagType(value)
        t2 = FailureFlagType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = True
        value2 = False
        t = FailureFlagType(value1)
        t2 = FailureFlagType(value2)
        self.assertNotEquals(t, t2)
