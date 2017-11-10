from mock import MagicMock, patch
import unittest


class TestBinaryPathNameType(unittest.TestCase):
    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global BinaryPathNameType
        from pywinservicemanager.ConfigurationTypes import BinaryPathNameType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        self.assertRaises(ValueError, BinaryPathNameType, None)

    def TestInitWithParametersOfNotTypeString(self):
        self.assertRaises(ValueError, BinaryPathNameType, bool(True))

    def TestInitWithCorrectParameters(self):
        value = 'name'
        t = BinaryPathNameType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'name'
        t = BinaryPathNameType(value)
        t2 = BinaryPathNameType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'name'
        value2 = 'name1'
        t = BinaryPathNameType(value1)
        t2 = BinaryPathNameType(value2)
        self.assertNotEquals(t, t2)
