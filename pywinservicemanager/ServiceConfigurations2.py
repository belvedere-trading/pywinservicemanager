import win32service # pylint: disable=import-error
from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory

class ServiceConfigurations2(object):

    Mappings = {'DelayedAutoStartInfo' : win32service.SERVICE_CONFIG_DELAYED_AUTO_START_INFO,
                'Description' : win32service.SERVICE_CONFIG_DESCRIPTION,
                'FailureActions' : win32service.SERVICE_CONFIG_FAILURE_ACTIONS,
                'FailureFlag' : win32service.SERVICE_CONFIG_FAILURE_ACTIONS_FLAG,
                'PreShutdownInfo' : win32service.SERVICE_CONFIG_PRESHUTDOWN_INFO,
                'ServiceSIDInfo' : win32service.SERVICE_CONFIG_SERVICE_SID_INFO}

    def __init__(self, serviceName, configurations):
        self.ServiceName = serviceName
        self.configurations = configurations

    @property
    def Configurations(self):
        return dict((key, value.StringValue()) for key, value in self.configurations.iteritems())

    @staticmethod
    def GenerateFromOperatingSystem(serviceConfigManagerHandle, serviceName):
        configurations = ServiceConfigurations2.__GetConfigurations2FromExistingService(serviceConfigManagerHandle, serviceName)
        return ServiceConfigurations2(serviceName, configurations)

    @staticmethod
    def GenerateNewServiceFromServiceDefinition(newServiceDefinition):
        configurations = ServiceConfigurations2.__GetConfigurations2FromNonExistingService(newServiceDefinition)
        return ServiceConfigurations2(newServiceDefinition.ServiceName, configurations)

    @staticmethod
    def __GetConfigurations2FromExistingService(serviceConfigManagerHandle, serviceName):
        serviceConfig2Handle = None
        configSettings = {}
        try:
            serviceConfig2Handle = win32service.OpenService(serviceConfigManagerHandle,
                                                            serviceName.StringValue(),
                                                            win32service.SERVICE_QUERY_CONFIG)
            for key, _ in ServiceConfigurations2.Mappings.iteritems():
                configSetting = None
                config2Enum = ServiceConfigurations2.Mappings[key]
                try:
                    configSetting = win32service.QueryServiceConfig2(serviceConfig2Handle, config2Enum)
                #There are some configs that are only valid on certain windows versions
                except Exception:
                    configSetting = None

                configSettingType = ConfigurationTypeFactory.CreateConfigurationType(key, configSetting, True)
                configSettings.update({key: configSettingType})
        finally:
            if serviceConfig2Handle is not None:
                win32service.CloseServiceHandle(serviceConfig2Handle)

        return configSettings

    @staticmethod
    def __GetConfigurations2FromNonExistingService(newServiceDefinition):
        configSettings = {}
        newServiceDefinitioConfigs = vars(newServiceDefinition)
        for configKey, _ in ServiceConfigurations2.Mappings.iteritems():
            configSettings[configKey] = newServiceDefinitioConfigs[configKey]

        return configSettings

    @staticmethod
    def __SetConfigrations(serviceHandle, configurationName, value):
        if value is None:
            return
        try:
            win32service.ChangeServiceConfig2(serviceHandle, configurationName, value.Win32Value())
        except NotImplementedError:
            # ChangeServiceConfig2 and/or config type not implemented on this version of NT or win32service
            pass

    def Save(self, serviceConfigManagerHandle):
        serviceConfig2Handle = None
        currentConfigs = ServiceConfigurations2.__GetConfigurations2FromExistingService(serviceConfigManagerHandle, self.ServiceName)
        try:
            serviceConfig2Handle = win32service.OpenService(serviceConfigManagerHandle,
                                                            self.ServiceName.StringValue(),
                                                            win32service.SERVICE_CHANGE_CONFIG | win32service.SERVICE_START)

            for key, value in ServiceConfigurations2.Mappings.iteritems():
                if currentConfigs[key] != self.configurations[key] and \
                   self.configurations[key] != None and \
                   self.configurations[key].StringValue() != None:
                    ServiceConfigurations2.__SetConfigrations(serviceConfig2Handle, value, self.configurations[key])
        except:
            raise
        finally:
            win32service.CloseServiceHandle(serviceConfig2Handle)

    def UpdateConfiguration(self, configurationName, value):
        if configurationName == 'FailureActions':
            self.configurations[configurationName] = value
            return

        self.configurations[configurationName] = ConfigurationTypeFactory.CreateConfigurationType(configurationName, value)

    def __eq__(self, other):
        if not isinstance(other, ServiceConfigurations2):
            return False
        for configKey in self.configurations.keys():
            if self.configurations[configKey] != other.configurations[configKey]:
                return False
        return True

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result
