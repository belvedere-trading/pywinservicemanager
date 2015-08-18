from mock import MagicMock, patch
import unittest


class TestServiceStartType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SERVICE_BOOT_START = 0
        self.mockwin32service.SERVICE_SYSTEM_START = 1
        self.mockwin32service.SERVICE_AUTO_START = 2
        self.mockwin32service.SERVICE_DEMAND_START = 3
        self.mockwin32service.SERVICE_DISABLED = 4

        global ServiceStartType
        from pywinservicemanager.ConfigurationTypes import ServiceStartType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = ServiceStartType(value)
        self.assertEquals(t.StringValue(), 'DEMAND_START')
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_DEMAND_START)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, ServiceStartType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = 'DEMAND_START'
        t = ServiceStartType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_DEMAND_START)

    def TestEquals(self):
        value = 'DISABLED'
        t = ServiceStartType(value)
        t2 = ServiceStartType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'BOOT_START'
        value2 = 'SYSTEM_START'
        t = ServiceStartType(value1)
        t2 = ServiceStartType(value2)
        self.assertNotEquals(t, t2)
