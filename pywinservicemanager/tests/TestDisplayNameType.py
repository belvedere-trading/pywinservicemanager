from mock import MagicMock, patch
import unittest

class TestDisplayNameType(unittest.TestCase):
    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global DisplayNameType
        from pywinservicemanager.ConfigurationTypes import DisplayNameType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        self.assertRaises(ValueError, DisplayNameType, None)

    def TestInitWithParametersOfNotTypeString(self):
        self.assertRaises(ValueError, DisplayNameType, bool(True))

    def TestInitWithCorrectParameters(self):
        value = 'name'
        t = DisplayNameType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'name'
        t = DisplayNameType(value)
        t2 = DisplayNameType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'name'
        value2 = 'name1'
        t = DisplayNameType(value1)
        t2 = DisplayNameType(value2)
        self.assertNotEquals(t, t2)
