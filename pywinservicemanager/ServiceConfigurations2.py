import win32service
from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationType
from pywinservicemanager.ConfigurationTypes import ServiceSIDInfoType
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
        self._configs = configurations

    @property
    def Configurations(self):
        return dict((key, value.StringValue()) for key, value in self._configs.iteritems())

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
            serviceConfig2Handle = win32service.OpenService(serviceConfigManagerHandle, serviceName.StringValue(), win32service.SERVICE_QUERY_CONFIG)
            for key in ServiceConfigurations2.Mappings.keys():
                configSetting = None
                config2Enum = ServiceConfigurations2.Mappings[key]
                try:
                    configSetting = win32service.QueryServiceConfig2(serviceConfig2Handle, config2Enum)
                #There are some configs that are only valid on certain windows versions
                except Exception as e:
                    configSetting = None
                    pass

                configSettingType = ConfigurationTypeFactory.CreateConfigurationType(key, configSetting, True)
                configSettings.update({key: configSettingType})
        finally:
            if serviceConfig2Handle is not None:
                win32service.CloseServiceHandle(serviceConfig2Handle)

        return configSettings

    @staticmethod
    def __GetConfigurations2FromNonExistingService(newServiceDefinition):
        serviceConfig2Handle = None
        configSettings = {}
        newServiceDefinitioConfigs = vars(newServiceDefinition)
        for configKey in ServiceConfigurations2.Mappings.keys():
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
            serviceConfig2Handle = win32service.OpenService(serviceConfigManagerHandle, self.ServiceName.StringValue(), win32service.SERVICE_CHANGE_CONFIG | win32service.SERVICE_START)

            for key, value in ServiceConfigurations2.Mappings.iteritems():
                if currentConfigs[key] != self._configs[key] and self._configs[key] != None and self._configs[key].StringValue() != None:
                    ServiceConfigurations2.__SetConfigrations(serviceConfig2Handle, value, self._configs[key])
        except:
            raise
        finally:
            win32service.CloseServiceHandle(serviceConfig2Handle)

    def UpdateConfiguration(self, configurationName, value):
        if configurationName == 'FailureActions':
                self._configs[configurationName] = value
                return

        self._configs[configurationName] = ConfigurationTypeFactory.CreateConfigurationType(configurationName, value)

    def __eq__(self, other):
        if not isinstance(other, ServiceConfigurations2):
            return False
        for configKey in self._configs.keys():
            if self._configs[configKey] != other._configs[configKey]:
                return False
        return True

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result
