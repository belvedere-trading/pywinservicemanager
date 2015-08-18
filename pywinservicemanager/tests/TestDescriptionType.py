from mock import MagicMock, patch
import unittest

class TestDescriptionType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global DescriptionType
        from pywinservicemanager.ConfigurationTypes import DescriptionType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = DescriptionType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithParametersOfNotTypeString(self):
        self.assertRaises(ValueError, DescriptionType, bool(True))

    def TestInitWithCorrectParameters(self):
        value = 'name'
        t = DescriptionType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = 'name'
        t = DescriptionType(value)
        t2 = DescriptionType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = 'name'
        value2 = 'name1'
        t = DescriptionType(value1)
        t2 = DescriptionType(value2)
        self.assertNotEquals(t, t2)
