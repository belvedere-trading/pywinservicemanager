from mock import MagicMock, patch
import unittest

class TestFailureActionDelayType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global FailureActionDelayType
        from pywinservicemanager.ConfigurationTypes import FailureActionDelayType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = FailureActionDelayType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, FailureActionDelayType, 'asdf')

    def TestInitWithLongParameters(self):
        value = long(1)
        t = FailureActionDelayType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithLongParameters(self):
        value = 1
        t = FailureActionDelayType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = long(1)
        t = FailureActionDelayType(value)
        t2 = FailureActionDelayType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = long(1)
        value2 = long(2)
        t = FailureActionDelayType(value1)
        t2 = FailureActionDelayType(value2)
        self.assertNotEquals(t, t2)
