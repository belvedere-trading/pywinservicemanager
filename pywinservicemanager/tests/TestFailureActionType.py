from mock import MagicMock, patch
from nose_parameterized import parameterized
import six
import unittest

class TestFailureActionType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SC_ACTION_NONE = 0
        self.mockwin32service.SC_ACTION_REBOOT = 1
        self.mockwin32service.SC_ACTION_RESTART = 2
        self.mockwin32service.SC_ACTION_RUN_COMMAND =3

        global FailureActionType
        global FailureActionExecutionType
        global FailureActionDelayType
        from pywinservicemanager.ConfigurationTypes import FailureActionType
        from pywinservicemanager.ConfigurationTypes import FailureActionExecutionType
        from pywinservicemanager.ConfigurationTypes import FailureActionDelayType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        failureActionExecutionType = None
        failureActionDelayType = None
        self.assertRaises(ValueError, FailureActionType, failureActionDelayType, failureActionExecutionType)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, FailureActionType, 'asdf', 1)

    @parameterized.expand([t] for t in six.integer_types)
    def TestEquals(self, int_type):
        failureActionExecutionType = FailureActionExecutionType('RUN_COMMAND')
        failureActionDelayType = FailureActionDelayType(int_type(1))
        value = FailureActionType(failureActionExecutionType, failureActionDelayType)
        value1 = FailureActionType(failureActionExecutionType, failureActionDelayType)
        self.assertEquals(value, value1)

    @parameterized.expand([t] for t in six.integer_types)
    def TestNotEquals(self, int_type):
        failureActionExecutionType = FailureActionExecutionType('REBOOT')
        failureActionDelayType = FailureActionDelayType(int_type(1))
        failureActionExecutionType1 = FailureActionExecutionType('RESTART')
        failureActionDelayType1 = FailureActionDelayType(int_type(2))
        value = FailureActionType(failureActionExecutionType, failureActionDelayType)
        value1 = FailureActionType(failureActionExecutionType1, failureActionDelayType1)
        self.assertNotEquals(value, value1)
