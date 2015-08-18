from mock import MagicMock, patch
import unittest

class TestDelayedAutoStartInfoType(unittest.TestCase):
    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global DelayedAutoStartInfoType
        from pywinservicemanager.ConfigurationTypes import DelayedAutoStartInfoType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = DelayedAutoStartInfoType(value)
        self.assertEquals(t.StringValue(), bool(value))
        self.assertEquals(t.Win32Value(), bool(value))

    def TestInitWithParametersOfNotTypeBool(self):
        self.assertRaises(ValueError, DelayedAutoStartInfoType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = True
        t = DelayedAutoStartInfoType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = True
        t = DelayedAutoStartInfoType(value)
        t2 = DelayedAutoStartInfoType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = True
        value2 = False
        t = DelayedAutoStartInfoType(value1)
        t2 = DelayedAutoStartInfoType(value2)
        self.assertNotEquals(t, t2)
