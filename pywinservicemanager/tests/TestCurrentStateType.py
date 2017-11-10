from mock import MagicMock, patch
import unittest


class TestCurrentStateType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SERVICE_CONTINUE_PENDING = 0
        self.mockwin32service.SERVICE_PAUSE_PENDING = 1
        self.mockwin32service.SERVICE_PAUSED = 2
        self.mockwin32service.SERVICE_RUNNING = 3
        self.mockwin32service.SERVICE_START_PENDING = 4
        self.mockwin32service.SERVICE_STOP_PENDING = 5
        self.mockwin32service.SERVICE_STOPPED = 6

        global CurrentStateType
        from pywinservicemanager.ConfigurationTypes import CurrentStateType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        self.assertRaises(ValueError, CurrentStateType, None)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, CurrentStateType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = 'PAUSE_PENDING'
        t = CurrentStateType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), t.PAUSE_PENDING)

    def TestInitWithCorrectWin32Parameters(self):
        value = self.mockwin32service.SERVICE_RUNNING
        t = CurrentStateType(value, True)
        self.assertEquals(t.StringValue(), 'RUNNING')
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'STOP_PENDING'
        t = CurrentStateType(value)
        t2 = CurrentStateType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'STOPPED'
        value2 = 'START_PENDING'
        t = CurrentStateType(value1)
        t2 = CurrentStateType(value2)
        self.assertNotEquals(t, t2)
