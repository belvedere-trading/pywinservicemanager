from mock import MagicMock, patch
import unittest

class TestPreShutdownInfoType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global PreShutdownInfoType
        from pywinservicemanager.ConfigurationTypes import PreShutdownInfoType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = PreShutdownInfoType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithParametersOfNotTypeString(self):
        self.assertRaises(ValueError, PreShutdownInfoType , 'asdf')

    def TestInitWithLongParameters(self):
        value = long(1)
        t = PreShutdownInfoType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithIntParameters(self):
        value = 1
        t = PreShutdownInfoType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = long(1)
        t = PreShutdownInfoType(value)
        t2 = PreShutdownInfoType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = long(1)
        value2 = long(2)
        t = PreShutdownInfoType(value1)
        t2 = PreShutdownInfoType(value2)
        self.assertNotEquals(t, t2)
