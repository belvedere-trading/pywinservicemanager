from mock import MagicMock, patch
import unittest

class TestDependenciesType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()
        global DependenciesType
        from pywinservicemanager.ConfigurationTypes import DependenciesType

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithParametersNone(self):
        value = None
        t = DependenciesType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithParametersOfNotTypeList(self):
        self.assertRaises(ValueError, DependenciesType, 'asdf')

    def TestInitWithCorrectParameters(self):
        value = ['a', 'b']
        t = DependenciesType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestInitWithEmptyList(self):
        value = []
        t = DependenciesType(value)
        self.assertEquals(t.StringValue(), value)
        self.assertEquals(t.Win32Value(), value)

    def TestEquals(self):
        value = ['a', 'b']
        t = DependenciesType(value)
        t2 = DependenciesType(value)
        self.assertEquals(t, t2)

    def TestNotEquals(self):
        value1 = ['a', 'b']
        value2 = []
        t = DependenciesType(value1)
        t2 = DependenciesType(value2)
        self.assertNotEquals(t, t2)
