from mock import MagicMock, patch
import unittest

class TestFailureActionExecutionType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SC_ACTION_NONE = 0
        self.mockwin32service.SC_ACTION_RESTART = 1
        self.mockwin32service.SC_ACTION_REBOOT = 2
        self.mockwin32service.SC_ACTION_RUN_COMMAND =3

        global FailureActionExecutionType
        from pywinservicemanager.ConfigurationTypes import FailureActionExecutionType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = FailureActionExecutionType(value)
        self.assertEquals(t.StringValue(), 'NONE')
        self.assertEquals(t.Win32Value(), self.mockwin32service.SC_ACTION_NONE)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, FailureActionExecutionType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = 'RESTART'
        t = FailureActionExecutionType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), self.mockwin32service.SC_ACTION_RESTART)

    def TestEquals(self):
        value = 'RUN_COMMAND'
        t = FailureActionExecutionType(value)
        t2 = FailureActionExecutionType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'RUN_COMMAND'
        value2 = 'RESTART'
        t = FailureActionExecutionType(value1)
        t2 = FailureActionExecutionType(value2)
        self.assertNotEquals(t, t2)
