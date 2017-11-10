from mock import MagicMock, patch
import unittest

class TestServiceStartNameType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global ServiceStartNameType
        from pywinservicemanager.ConfigurationTypes import ServiceStartNameType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = ServiceStartNameType(value)
        self.assertEquals(t.StringValue(), u'LocalSystem')
        self.assertEquals(t.Win32Value(), u'LocalSystem')

    def TestInitWithParametersOfNotTypeString(self):
        self.assertRaises(ValueError, ServiceStartNameType, bool(True))

    def TestInitWithCorrectParameters(self):
        value = 'name'
        t = ServiceStartNameType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'name'
        t = ServiceStartNameType(value)
        t2 = ServiceStartNameType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'name'
        value2 = 'name1'
        t = ServiceStartNameType(value1)
        t2 = ServiceStartNameType(value2)
        self.assertNotEquals(t, t2)
