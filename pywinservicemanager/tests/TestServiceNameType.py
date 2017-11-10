from mock import MagicMock, patch
import unittest


class TestServiceNameType(unittest.TestCase):
    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global ServiceNameType
        from pywinservicemanager.ConfigurationTypes import ServiceNameType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        self.assertRaises(ValueError, ServiceNameType, None)

    def TestInitWithParametersOfNotTypeString(self):
        self.assertRaises(ValueError, ServiceNameType, bool(True))

    def TestInitWithCorrectParameters(self):
        value = 'name'
        t = ServiceNameType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'name'
        t = ServiceNameType(value)
        t2 = ServiceNameType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'name'
        value2 = 'name1'
        t = ServiceNameType(value1)
        t2 = ServiceNameType(value2)
        self.assertNotEquals(t, t2)
