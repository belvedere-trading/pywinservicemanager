import win32service
from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory
from pywinservicemanager.NewServiceDefinition import NewServiceDefinition

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
      self._configs = configurations

    @property
    def Configurations(self):
        return dict((key, value.StringValue()) for key, value in self._configs.iteritems())

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
        returnConfigs= {}
        try:
            serviceHandle = win32service.OpenService(serviceConfigManagerHandle, serviceName.StringValue(), win32service.SERVICE_QUERY_CONFIG)
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

        for key in ServiceConfigurations.indexesOfServiceConfig.keys():
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
        self._configs[configurationName] = ConfigurationTypeFactory.CreateConfigurationType(configurationName, value)

    def _SaveNewService(self, serviceConfigManagerHandle, serviceStartNamePassword=None):
        serviceHandle = None
        try:
            serviceHandle = win32service.CreateService(serviceConfigManagerHandle,
                                                       self._configs['ServiceName'].Win32Value(),
                                                       self._configs['DisplayName'].Win32Value(),
                                                       win32service.SERVICE_ALL_ACCESS, # desired access
                                                       self._configs['ServiceType'].Win32Value(),
                                                       self._configs['StartType'].Win32Value(),
                                                       self._configs['ErrorControl'].Win32Value(),
                                                       self._configs['BinaryPathName'].Win32Value(),
                                                       self._configs['LoadOrderGroup'].Win32Value(),
                                                       0,
                                                       self._configs['Dependencies'].Win32Value(),
                                                       self._configs['ServiceStartName'].Win32Value(),
                                                       serviceStartNamePassword)
        finally:
            if serviceHandle is not None:
                win32service.CloseServiceHandle(serviceHandle)

    def _SaveExistingService(self, serviceConfigManagerHandle, serviceStartNamePassword=None):
        serviceHandle = None
        try:
            serviceHandle = win32service.OpenService(serviceConfigManagerHandle, self._configs['ServiceName'].StringValue(),  win32service.SERVICE_CHANGE_CONFIG | win32service.SERVICE_START)
            win32service.ChangeServiceConfig(serviceHandle,
                                             self._configs['ServiceType'].Win32Value(),
                                             self._configs['StartType'].Win32Value(),
                                             self._configs['ErrorControl'].Win32Value(),
                                             self._configs['BinaryPathName'].Win32Value(),
                                             self._configs['LoadOrderGroup'].Win32Value(),
                                             0,
                                             self._configs['Dependencies'].Win32Value(),
                                             self._configs['ServiceStartName'].Win32Value(),
                                             serviceStartNamePassword,
                                             self._configs['DisplayName'].Win32Value())
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def __eq__(self, other):
        if not isinstance(other, ServiceConfigurations):
            return False

        for key in self._configs.keys():
            # TagId is not something that we can assign, so we do not take it into account
            # when checking equality
            if key == 'TagId':
                    continue
            if  self._configs[key] != other._configs[key]:
                return False

        return True

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result
