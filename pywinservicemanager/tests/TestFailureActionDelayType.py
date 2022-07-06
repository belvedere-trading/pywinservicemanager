from mock import MagicMock, patch
from nose_parameterized import parameterized
import six
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

    @parameterized.expand([t] for t in six.integer_types)
    def TestInitWithIntTypeParameters(self, int_type):
        value = int_type(1)
        t = FailureActionDelayType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    @parameterized.expand([t] for t in six.integer_types)
    def TestEquals(self, int_type):
        value = int_type(1)
        t = FailureActionDelayType(value)
        t2 = FailureActionDelayType(value)
        self.assertEquals(t, t2)

    @parameterized.expand([t] for t in six.integer_types)
    def TestNotEquals(self, int_type):
        value1 = int_type(1)
        value2 = int_type(2)
        t = FailureActionDelayType(value1)
        t2 = FailureActionDelayType(value2)
        self.assertNotEquals(t, t2)

    def TestValueCastToLong(self):
        value = 1
        t = FailureActionDelayType(value)
        long_type = long if six.PY2 else int #pylint: disable=undefined-variable
        self.assertEquals(type(t.StringValue()), long_type)
        self.assertEquals(type(t.Win32Value()), long_type)
