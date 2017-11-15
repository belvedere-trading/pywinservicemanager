from mock import MagicMock, patch
import unittest

class TestLoadOrderGroupType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global LoadOrderGroupType
        from pywinservicemanager.ConfigurationTypes import LoadOrderGroupType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = LoadOrderGroupType(value)
        self.assertEquals(t.StringValue(), u'')
        self.assertEquals(t.Win32Value(), u'')

    def TestInitWithParametersOfNotTypeString(self):
        self.assertRaises(ValueError, LoadOrderGroupType, bool(True))

    def TestInitWithUnicodeParameters(self):
        value = u'name'
        t = LoadOrderGroupType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithStringParameters(self):
        value = 'name'
        t = LoadOrderGroupType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = u'name'
        t = LoadOrderGroupType(value)
        t2 = LoadOrderGroupType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = u'name'
        value2 = u'name1'
        t = LoadOrderGroupType(value1)
        t2 = LoadOrderGroupType(value2)
        self.assertNotEquals(t, t2)
