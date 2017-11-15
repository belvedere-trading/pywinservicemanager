import win32service # pylint: disable=import-error
from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory

class ServiceConfigurations(object):
    # these indexes are defined by the win32 interface... I am definately not a fan of this type of design
    indexesOfServiceConfig = {'ServiceType': 0,
                              'StartType': 1,
                              'ErrorControl': 2,
                              'BinaryPathName': 3,
                              'LoadOrderGroup': 4,
                              'TagId': 5,
                              'Dependencies': 6,
                              'ServiceStartName': 7,
                              'DisplayName': 8}

    def __init__(self, configurations):
        self.configurations = configurations

    @property
    def Configurations(self):
        return dict((key, value.StringValue()) for key, value in self.configurations.iteritems())

    @staticmethod
    def GenerateFromOperatingSystem(serviceConfigManagerHandle, serviceName):
        configurations = ServiceConfigurations.__CreateFromExistingService(serviceConfigManagerHandle, serviceName)
        return ServiceConfigurations(configurations)

    @staticmethod
    def GenerateNewServiceFromServiceDefinition(newServiceDefinition):
        configurations = ServiceConfigurations.__CeateFromNonExistentService(newServiceDefinition)
        return ServiceConfigurations(configurations)

    @staticmethod
    def __CreateFromExistingService(serviceConfigManagerHandle, serviceName):
        serviceHandle = None
        returnConfigs = {}
        try:
            serviceHandle = win32service.OpenService(serviceConfigManagerHandle,
                                                     serviceName.StringValue(),
                                                     win32service.SERVICE_QUERY_CONFIG)
            savedConfigs = win32service.QueryServiceConfig(serviceHandle)
            returnConfigs = {'ServiceName': serviceName}

            for key, value in ServiceConfigurations.indexesOfServiceConfig.iteritems():
                returnConfigs[key] = ConfigurationTypeFactory.CreateConfigurationType(key, savedConfigs[value], True)
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)
        return returnConfigs

    @staticmethod
    def __CeateFromNonExistentService(newServiceDefinition):
        configs = {'ServiceName': newServiceDefinition.ServiceName}
        newServiceDefinitionAsDict = vars(newServiceDefinition)

        for key, _ in ServiceConfigurations.indexesOfServiceConfig.iteritems():
            value = newServiceDefinitionAsDict.get(key, None)
            # TagId is a value that is assigned by the OS, thus we just create a config type with the default
            if key == 'TagId':
                configs[key] = ConfigurationTypeFactory.CreateConfigurationType('TagId', 0, False)
            else:
                configs[key] = value

        return configs

    def Save(self, serviceExists, serviceConfigManagerHandle, serviceStartNamePassword=None):
        if serviceExists:
            self._SaveExistingService(serviceConfigManagerHandle, serviceStartNamePassword)
        else:
            self._SaveNewService(serviceConfigManagerHandle, serviceStartNamePassword)

    def UpdateConfiguration(self, configurationName, value):
        self.configurations[configurationName] = ConfigurationTypeFactory.CreateConfigurationType(configurationName, value)

    def _SaveNewService(self, serviceConfigManagerHandle, serviceStartNamePassword=None):
        serviceHandle = None
        try:
            serviceHandle = win32service.CreateService(serviceConfigManagerHandle,
                                                       self.configurations['ServiceName'].Win32Value(),
                                                       self.configurations['DisplayName'].Win32Value(),
                                                       win32service.SERVICE_ALL_ACCESS, # desired access
                                                       self.configurations['ServiceType'].Win32Value(),
                                                       self.configurations['StartType'].Win32Value(),
                                                       self.configurations['ErrorControl'].Win32Value(),
                                                       self.configurations['BinaryPathName'].Win32Value(),
                                                       self.configurations['LoadOrderGroup'].Win32Value(),
                                                       0,
                                                       self.configurations['Dependencies'].Win32Value(),
                                                       self.configurations['ServiceStartName'].Win32Value(),
                                                       serviceStartNamePassword)
        finally:
            if serviceHandle is not None:
                win32service.CloseServiceHandle(serviceHandle)

    def _SaveExistingService(self, serviceConfigManagerHandle, serviceStartNamePassword=None):
        serviceHandle = None
        try:
            serviceHandle = win32service.OpenService(serviceConfigManagerHandle,
                                                     self.configurations['ServiceName'].StringValue(),
                                                     win32service.SERVICE_CHANGE_CONFIG | win32service.SERVICE_START)
            win32service.ChangeServiceConfig(serviceHandle,
                                             self.configurations['ServiceType'].Win32Value(),
                                             self.configurations['StartType'].Win32Value(),
                                             self.configurations['ErrorControl'].Win32Value(),
                                             self.configurations['BinaryPathName'].Win32Value(),
                                             self.configurations['LoadOrderGroup'].Win32Value(),
                                             0,
                                             self.configurations['Dependencies'].Win32Value(),
                                             self.configurations['ServiceStartName'].Win32Value(),
                                             serviceStartNamePassword,
                                             self.configurations['DisplayName'].Win32Value())
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def __eq__(self, other):
        if not isinstance(other, ServiceConfigurations):
            return False

        for key in self.configurations.keys():
            # TagId is not something that we can assign, so we do not take it into account
            # when checking equality
            if key == 'TagId':
                continue
            if  self.configurations[key] != other.configurations[key]:
                return False
        return True

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result
