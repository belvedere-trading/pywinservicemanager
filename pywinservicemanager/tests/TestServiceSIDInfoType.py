from mock import MagicMock, patch
import unittest

class TestServiceSIDInfoType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SERVICE_SID_TYPE_NONE = 0
        self.mockwin32service.SERVICE_SID_TYPE_RESTRICTED = 1
        self.mockwin32service.SERVICE_SID_TYPE_UNRESTRICTED = 2

        global ServiceSIDInfoType
        from pywinservicemanager.ConfigurationTypes import ServiceSIDInfoType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        t = ServiceSIDInfoType(None)
        self.assertEquals(t.StringValue(), 'SID_TYPE_NONE')
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_SID_TYPE_NONE)

    def TestInitWithParametersOfNotValidValue(self):
        self.assertRaises(ValueError, ServiceSIDInfoType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = 'SID_TYPE_NONE'
        t = ServiceSIDInfoType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), self.mockwin32service.SERVICE_SID_TYPE_NONE)

    def TestEquals(self):
        value = 'SID_TYPE_RESTRICTED'
        t = ServiceSIDInfoType(value)
        t2 = ServiceSIDInfoType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'SID_TYPE_RESTRICTED'
        value2 = 'SID_TYPE_UNRESTRICTED'
        t = ServiceSIDInfoType(value1)
        t2 = ServiceSIDInfoType(value2)
        self.assertNotEquals(t, t2)
