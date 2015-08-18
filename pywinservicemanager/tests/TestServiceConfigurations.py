from mock import MagicMock, patch
import unittest


class mock_constants(object):
    SERVICE_WIN32_SHARE_PROCESS = 1
    SERVICE_WIN32_OWN_PROCESS = 2
    SERVICE_KERNEL_DRIVER = 3
    SERVICE_FILE_SYSTEM_DRIVER = 4

    SERVICE_ERROR_CRITICAL = 0
    SERVICE_ERROR_IGNORE = 1
    SERVICE_ERROR_NORMAL = 2
    SERVICE_ERROR_SEVERE =3

    SERVICE_BOOT_START = 0
    SERVICE_SYSTEM_START = 1
    SERVICE_AUTO_START = 2
    SERVICE_DEMAND_START = 3
    SERVICE_DISABLED = 4

class TestServiceConfigurations(unittest.TestCase):
    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})


        self.mockwin32service.SERVICE_WIN32_SHARE_PROCESS = mock_constants.SERVICE_WIN32_SHARE_PROCESS
        self.mockwin32service.SERVICE_WIN32_OWN_PROCESS = mock_constants. SERVICE_WIN32_OWN_PROCESS
        self.mockwin32service.SERVICE_KERNEL_DRIVER = mock_constants.SERVICE_KERNEL_DRIVER
        self.mockwin32service.SERVICE_FILE_SYSTEM_DRIVER = mock_constants.SERVICE_FILE_SYSTEM_DRIVER

        self.mockwin32service.SERVICE_ERROR_CRITICAL = mock_constants.SERVICE_ERROR_CRITICAL
        self.mockwin32service.SERVICE_ERROR_IGNORE = mock_constants.SERVICE_ERROR_IGNORE
        self.mockwin32service.SERVICE_ERROR_NORMAL = mock_constants.SERVICE_ERROR_NORMAL
        self.mockwin32service.SERVICE_ERROR_SEVERE = mock_constants.SERVICE_ERROR_SEVERE

        self.mockwin32service.SERVICE_BOOT_START = mock_constants.SERVICE_BOOT_START
        self.mockwin32service.SERVICE_SYSTEM_START = mock_constants.SERVICE_SYSTEM_START
        self.mockwin32service.SERVICE_AUTO_START = mock_constants.SERVICE_AUTO_START
        self.mockwin32service.SERVICE_DEMAND_START = mock_constants.SERVICE_DEMAND_START
        self.mockwin32service.SERVICE_DISABLED = mock_constants.SERVICE_DISABLED

        self.mockwin32service.OpenService.return_value = 1
        self.mockwin32service.QueryServiceConfig = MagicMock(side_effect=TestServiceConfigurations.QueryServiceConfig)
        self.patcher.start()

        global win32service
        import win32service
        global ServiceConfigurations
        global NewServiceDefinition
        from pywinservicemanager.ServiceConfigurations import ServiceConfigurations
        from pywinservicemanager.NewServiceDefinition import NewServiceDefinition

    def tearDown(self):
        self.patcher.stop()

    @staticmethod
    def QueryServiceConfig(serviceHandle):
        serviceDefinition = TestServiceConfigurations.GetNonExistentArgs()
        args = serviceDefinition.__dict__
        values = [None]*len(ServiceConfigurations.indexesOfServiceConfig)

        for key,value in ServiceConfigurations.indexesOfServiceConfig.iteritems():
            if key == 'TagId':
                values[value] = 0
            else:
                values[value] = args[key].Win32Value()

        return values

    @staticmethod
    def GetNonExistentArgs():
        newServiceDefinition = NewServiceDefinition(serviceName="MyTestService",
                                                    displayName = "MyTestService",
                                                    binaryPathName ="C:\\Windows\\System32\\cmd.exe /c echo hello",
                                                    startType = 'AUTO_START',
                                                    serviceType = 'WIN32_SHARE_PROCESS',
                                                    errorControl = 'ERROR_IGNORE',
                                                    dependencies = ['dependentService'],
                                                    serviceStartName ='username',
                                                    loadOrderGroup = None )
        return newServiceDefinition

    def TestCreateFromNonExisting(self):
        configs = TestServiceConfigurations.GetNonExistentArgs()
        service = ServiceConfigurations.GenerateFromOperatingSystem(1, configs.ServiceName)
        self.assertTrue(service == service)

    def TestCreateFromExisting(self):
        configs = TestServiceConfigurations.GetNonExistentArgs()
        service = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(configs)
        self.assertTrue(service == service)

    def TestCreateFromNonExistingAndExisting(self):
        configs = TestServiceConfigurations.GetNonExistentArgs()
        service1 = ServiceConfigurations.GenerateFromOperatingSystem(1, configs.ServiceName)
        configs2 = TestServiceConfigurations.GetNonExistentArgs()
        service2 = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(configs)
        self.assertTrue(service1 == service2)

    def TestCreateFromNonExistingWithDefaults(self):
        newServiceDefinition = NewServiceDefinition(serviceName = "MyTestService",
                                                    displayName = "MyTestService",
                                                    binaryPathName = "C:\\Windows\\System32\\cmd.exe /c echo hello")

        service = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=newServiceDefinition)

        self.assertTrue(service._configs['ServiceType'].Win32Value() == self.mockwin32service.SERVICE_WIN32_OWN_PROCESS)
        self.assertTrue(service._configs['LoadOrderGroup'].Win32Value() == u'')
        self.assertTrue(service._configs['BinaryPathName'].Win32Value() == "C:\\Windows\\System32\\cmd.exe /c echo hello" )
        self.assertTrue(service._configs['ServiceStartName'].Win32Value() == u'LocalSystem')
        self.assertTrue(service._configs['ServiceName'].Win32Value() == "MyTestService")
        self.assertTrue(service._configs['DisplayName'].Win32Value() == "MyTestService")
        self.assertTrue(service._configs['StartType'].Win32Value() == self.mockwin32service.SERVICE_DEMAND_START)
        self.assertTrue(service._configs['Dependencies'].Win32Value() == None)
        self.assertTrue(service._configs['ErrorControl'].Win32Value() == self.mockwin32service.SERVICE_ERROR_NORMAL)

    def TestEqualsIsTrue(self):
        configs = TestServiceConfigurations.GetNonExistentArgs()
        service = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
        service1 = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
        self.assertTrue(service == service1)

    def TestEqualsIsFalse(self):
        configs = TestServiceConfigurations.GetNonExistentArgs()
        service = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
        for key, value in service._configs.iteritems():
            if key == 'TagId':
                continue
            service1 = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
            if isinstance(value, int):
                service1._configs[key] = service1._configs[key]+1
            if isinstance(value, list):
                service1._configs[key] = None
            else:
                service1._configs[key] = 'NewValue'
            equals = service == service1
            self.assertFalse(equals, key + ' is not compared')

    def TestNotEqualsIsTrue(self):
        configs = TestServiceConfigurations.GetNonExistentArgs()
        service = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
        for key, value in service._configs.iteritems():
            if key == 'TagId':
                continue
            service1 = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
            if isinstance(value, int):
                service1._configs[key] = service1._configs[key]+1
            if isinstance(value, list):
                service1._configs[key] = None
            else:
                service1._configs[key] = 'NewValue'
            equals = service == service1
            self.assertTrue(not equals, key + ' is not compared')

    def TestNotEqualsIsFalse(self):
        configs = TestServiceConfigurations.GetNonExistentArgs()
        service = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
        service1 = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition=configs)
        equals = service != service1
        self.assertFalse(equals)
