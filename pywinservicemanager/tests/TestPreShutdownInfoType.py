from mock import MagicMock, patch
from nose_parameterized import parameterized
import six
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

    @parameterized.expand([t] for t in six.integer_types)
    def TestInitWithIntTypeParameters(self, int_type):
        value = int_type(1)
        t = PreShutdownInfoType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    @parameterized.expand([t] for t in six.integer_types)
    def TestEquals(self, int_type):
        value = int_type(1)
        t = PreShutdownInfoType(value)
        t2 = PreShutdownInfoType(value)
        self.assertEquals(t, t2)

    @parameterized.expand([t] for t in six.integer_types)
    def TestNotEquals(self, int_type):
        value1 = int_type(1)
        value2 = int_type(2)
        t = PreShutdownInfoType(value1)
        t2 = PreShutdownInfoType(value2)
        self.assertNotEquals(t, t2)
