from mock import MagicMock, patch
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

    def TestEquals(self):
        failureActionExecutionType = FailureActionExecutionType('RUN_COMMAND')
        failureActionDelayType = FailureActionDelayType(long(1))
        value = FailureActionType(failureActionExecutionType, failureActionDelayType)
        value1 = FailureActionType(failureActionExecutionType, failureActionDelayType)
        self.assertEquals(value, value1)

    def TestNotEquals(self):
        failureActionExecutionType = FailureActionExecutionType('REBOOT')
        failureActionDelayType = FailureActionDelayType(long(1))
        failureActionExecutionType1 = FailureActionExecutionType('RESTART')
        failureActionDelayType1 = FailureActionDelayType(long(2))
        value = FailureActionType(failureActionExecutionType, failureActionDelayType)
        value1 = FailureActionType(failureActionExecutionType1, failureActionDelayType1)
        self.assertNotEquals(value, value1)
