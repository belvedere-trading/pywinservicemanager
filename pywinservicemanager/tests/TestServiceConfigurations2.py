from mock import MagicMock, patch
import unittest


class TestServiceConfigurations2(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.mockFailureAction = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SERVICE_CONFIG_DELAYED_AUTO_START_INFO = 3
        self.mockwin32service.SERVICE_CONFIG_DESCRIPTION = 1
        self.mockwin32service.SERVICE_CONFIG_FAILURE_ACTIONS = 2
        self.mockwin32service.SERVICE_CONFIG_FAILURE_ACTIONS_FLAG = 4
        self.mockwin32service.SERVICE_CONFIG_PRESHUTDOWN_INFO = 7
        self.mockwin32service.SERVICE_CONFIG_SERVICE_SID_INFO =5

        self.mockwin32service.SERVICE_SID_TYPE_NONE = 0
        self.mockwin32service.SERVICE_SID_TYPE_RESTRICTED = 3
        self.mockwin32service.SERVICE_SID_TYPE_UNRESTRICTED = 1

        self.mockwin32service.SC_ACTION_NONE = 0
        self.mockwin32service.SC_ACTION_REBOOT = 2
        self.mockwin32service.SC_ACTION_RESTART = 1
        self.mockwin32service.SC_ACTION_RUN_COMMAND =3

        self.mockwin32service.OpenService.return_value = 1
        self.mockwin32service.QueryServiceConfig2 = MagicMock(side_effect=TestServiceConfigurations2.GetServiceConfig2Value)

        global win32service
        import win32service
        global FailureActionTypeFactory
        from pywinservicemanager.ConfigurationTypes import FailureActionTypeFactory
        global FailureActionType
        from pywinservicemanager.ConfigurationTypes import FailureActionType
        global FailureActionConfigurationType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationType
        global FailureActionConfigurationRebootMessageType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationRebootMessageType
        global FailureActionConfigurationCommandLineType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationCommandLineType
        global FailureActionConfigurationResetPeriodType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationResetPeriodType
        global ServiceConfigurations2
        from pywinservicemanager.ServiceConfigurations2 import ServiceConfigurations2
        global NewServiceDefinition
        from pywinservicemanager.NewServiceDefinition import NewServiceDefinition

    def tearDown(self):
        self.patcher.stop()
    def GetNewConfig2Params(self):

        failureActionList = []
        failureActionList.append(FailureActionTypeFactory.CreateRestartAction(300))
        failureActionList.append(FailureActionTypeFactory.CreateRunCommandAction(0))
        rebootMessage = FailureActionConfigurationRebootMessageType('rebootMessage')
        command = FailureActionConfigurationCommandLineType('command')
        resetPeriod = FailureActionConfigurationResetPeriodType(300)
        FailureActions = FailureActionConfigurationType(failureActionList, resetPeriod, rebootMessage, command)


        newServiceDefinition = NewServiceDefinition(serviceName="TestService",
                                                    displayName = "TestService",
                                                    binaryPathName ="C:\\Windows\\System32\\cmd.exe /c echo hello",
                                                    delayedAutoStartInfo=False,
                                                    failureFlag=False,
                                                    preShutdownInfo = long(18000),
                                                    serviceSIDInfo ='SID_TYPE_UNRESTRICTED',
                                                    description ='TestService',
                                                    failureActions=FailureActions)
        return newServiceDefinition

    @staticmethod
    def GetServiceConfig2Value(serviceConfig2Handle, config):
        values = {win32service.SERVICE_CONFIG_SERVICE_SID_INFO: win32service.SERVICE_SID_TYPE_UNRESTRICTED,
                  win32service.SERVICE_CONFIG_DESCRIPTION: 'TestService',
                  win32service.SERVICE_CONFIG_FAILURE_ACTIONS: {'Actions': ((1, 300), (3, 0)), 'Command': 'command', 'RebootMsg': 'rebootMessage', 'ResetPeriod': 300},
                  win32service.SERVICE_CONFIG_FAILURE_ACTIONS_FLAG: False,
                  win32service.SERVICE_CONFIG_PRESHUTDOWN_INFO: 18000L,
                  win32service.SERVICE_CONFIG_DELAYED_AUTO_START_INFO: False}
        return values[config]

    def TestCreateNewServiceEntity(self):
        configs = self.GetNewConfig2Params()
        service = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(configs)
        self.assertTrue(service == service)

    def TestGetServiceEntityFromExisting(self):
        configs = self.GetNewConfig2Params()
        service = ServiceConfigurations2.GenerateFromOperatingSystem(-1, configs.ServiceName)
        self.assertTrue(service == service)

    def TestBothExistingAndNonExisting(self):
        configs = self.GetNewConfig2Params()
        service = ServiceConfigurations2.GenerateFromOperatingSystem(-1, configs.ServiceName)
        service1 = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(configs)
        self.assertTrue(service == service1)
        self.assertTrue(service.Configurations == service1.Configurations)

    def TestUpdateFailureActionsConfiguration(self):
        configs = self.GetNewConfig2Params()
        service = ServiceConfigurations2.GenerateFromOperatingSystem(-1, configs.ServiceName)
        service2 = ServiceConfigurations2.GenerateFromOperatingSystem(-1, configs.ServiceName)

        failureActionList = []
        delay = 1000
        failureActionList.append(FailureActionTypeFactory.CreateRestartAction(delay))
        resetPeriod = 1
        rebootMsg = None
        commandLine = None
        failureActions = FailureActionConfigurationType(failureActionList, resetPeriod, rebootMsg, commandLine)
        service.UpdateConfiguration('FailureActions', failureActions)
        service2.Configurations['FailureActions'] = failureActions

        self.assertTrue(service, service2)

    def TestBothExistingAndNonExistingConfigDictsAreEqual(self):
        configs = self.GetNewConfig2Params()
        service = ServiceConfigurations2.GenerateFromOperatingSystem(-1, configs.ServiceName)
        kwargs = self.GetNewConfig2Params()
        service1 = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(configs)
        self.assertTrue(service.Configurations == service1.Configurations)

    def TestEqualsIsTrue(self):
        configs = self.GetNewConfig2Params()
        service = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(configs)
        service1 = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(configs)
        self.assertTrue(service == service1)

    def TestNotEqualsIsFalse(self):
        configs = self.GetNewConfig2Params()
        service = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(configs)
        service1 = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(configs)
        equals = service == service1
        self.assertFalse(not equals)
