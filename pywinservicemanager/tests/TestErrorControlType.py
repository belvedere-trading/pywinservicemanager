from mock import MagicMock, patch
import unittest


class TestErrorControlType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SERVICE_ERROR_IGNORE = 0
        self.mockwin32service.SERVICE_ERROR_NORMAL = 1
        self.mockwin32service.SERVICE_ERROR_SEVERE = 2
        self.mockwin32service.SERVICE_ERROR_CRITICAL = 3
        global ErrorControlType
        from pywinservicemanager.ConfigurationTypes import ErrorControlType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = ErrorControlType(value)
        self.assertEquals(t.StringValue(), 'ERROR_NORMAL')
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_ERROR_NORMAL)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, ErrorControlType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = 'ERROR_CRITICAL'
        t = ErrorControlType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_ERROR_CRITICAL)

    def TestEquals(self):
        value = 'ERROR_IGNORE'
        t = ErrorControlType(value)
        t2 = ErrorControlType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'ERROR_CRITICAL'
        value2 = 'ERROR_IGNORE'
        t = ErrorControlType(value1)
        t2 = ErrorControlType(value2)
        self.assertNotEquals(t, t2)
