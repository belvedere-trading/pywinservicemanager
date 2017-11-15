from mock import MagicMock, patch
import unittest


class TestServiceType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SERVICE_FILE_SYSTEM_DRIVER = 1
        self.mockwin32service.SERVICE_KERNEL_DRIVER = 2
        self.mockwin32service.SERVICE_WIN32_OWN_PROCESS = 16
        self.mockwin32service.SERVICE_WIN32_SHARE_PROCESS = 32

        global ServiceType
        from pywinservicemanager.ConfigurationTypes import ServiceType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = ServiceType(value)
        self.assertEquals(t.StringValue(), 'WIN32_OWN_PROCESS')
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_WIN32_OWN_PROCESS)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, ServiceType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = 'WIN32_SHARE_PROCESS'
        t = ServiceType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_WIN32_SHARE_PROCESS)

    def TestEquals(self):
        value = 'FILE_SYSTEM_DRIVER'
        t = ServiceType(value)
        t2 = ServiceType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'KERNEL_DRIVER'
        value2 = 'WIN32_OWN_PROCESS'
        t = ServiceType(value1)
        t2 = ServiceType(value2)
        self.assertNotEquals(t, t2)
