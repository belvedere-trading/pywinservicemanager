import win32service # pylint: disable=import-error
from pywinservicemanager.ServiceEntity import ServiceEntity
from pywinservicemanager.ServiceStatusProcessEntity import ServiceStatusProcessEntity
from pywinservicemanager.NewServiceDefinition import NewServiceDefinition
from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory

def CreateService(newServiceDefinition):
    if not isinstance(newServiceDefinition, NewServiceDefinition):
        msg = 'newServiceDefinition parameter must be type of NewServiceDefinition, but it is of type {0}'
        raise TypeError(msg.format(type(newServiceDefinition).__name__))
    service = ServiceEntity.GenerateNewServiceFromServiceDefinition(newServiceDefinition)
    return service

def GetService(serviceName):
    if not ServiceExists(serviceName):
        raise Exception('Service: {0} does not exist'.format(serviceName))

    serviceNameConfiguration = ConfigurationTypeFactory.CreateConfigurationType('ServiceName', serviceName)
    service = ServiceEntity.GenerateFromOperatingSystem(serviceNameConfiguration)
    return service

def QueryAllServicesStatus(includeDriverServices=False):
    returnValue = []
    servicesRaw = []
    serviceConfigManagerHandle = None
    try:
        serviceConfigManagerHandle = win32service.OpenSCManager('', None, win32service.SC_MANAGER_ALL_ACCESS)
        if includeDriverServices:
            servicesRaw += win32service.EnumServicesStatusEx(serviceConfigManagerHandle, win32service.SERVICE_DRIVER)

        servicesRaw += win32service.EnumServicesStatusEx(serviceConfigManagerHandle)
        for rawService in servicesRaw:
            serviceStatus = ServiceStatusProcessEntity(**rawService)
            returnValue.append(serviceStatus.Status)
        return returnValue
    finally:
        if serviceConfigManagerHandle:
            win32service.CloseServiceHandle(serviceConfigManagerHandle)

def ServiceExists(serviceName):
    return ServiceEntity.ServiceExists(serviceName)

def GetServiceStatus(serviceName):
    if not ServiceExists(serviceName):
        raise Exception('Service: {0} does not exist'.format(serviceName))

    serviceNameConfiguration = ConfigurationTypeFactory.CreateConfigurationType('ServiceName', serviceName)
    with ServiceEntity.GenerateFromOperatingSystem(serviceNameConfiguration) as service:
        return service.GetServiceStatus()
