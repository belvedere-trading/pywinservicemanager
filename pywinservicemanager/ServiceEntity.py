import win32service
import time
from pywinservicemanager.ServiceConfigurations2 import ServiceConfigurations2
from pywinservicemanager.ServiceConfigurations import ServiceConfigurations
from pywinservicemanager.ServiceStatusProcessEntity import ServiceStatusProcessEntity
from pywinservicemanager.ServiceStatusEntity import ServiceStatusEntity
from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory
from pywinservicemanager.ConfigurationTypes import CurrentStateType

class ServiceEntity(object):

    _TIMEOUT = 30

    def __init__(self, serviceConfigManagerHandle, serviceName, serviceConfigurations, serviceConfigurations2):
        self.__serviceConfigManagerHandle = serviceConfigManagerHandle
        self.__serviceConfigurations = serviceConfigurations
        self.__serviceConfigurations2 = serviceConfigurations2
        self.__serviceName = serviceName

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.__serviceConfigManagerHandle is not None:
            win32service.CloseServiceHandle(self.__serviceConfigManagerHandle)
            self.__serviceConfigManagerHandle = None

    def __del__(self):
        if self.__serviceConfigManagerHandle is not None:
            win32service.CloseServiceHandle(self.__serviceConfigManagerHandle)
            self.__serviceConfigManagerHandle = None

    @staticmethod
    def GenerateFromOperatingSystem(serviceName):
        # Just making sure that the service exists
        if not ServiceEntity.ServiceExists(serviceName.StringValue()):
            raise ValueError('Service "{0}" does not exists'.format(serviceName))

        serviceConfigManagerHandle = win32service.OpenSCManager('', None, win32service.SC_MANAGER_ALL_ACCESS)
        serviceConfigurations = ServiceConfigurations.GenerateFromOperatingSystem(serviceConfigManagerHandle, serviceName)
        serviceConfigurations2 = ServiceConfigurations2.GenerateFromOperatingSystem(serviceConfigManagerHandle, serviceName)
        return ServiceEntity(serviceConfigManagerHandle, serviceName, serviceConfigurations, serviceConfigurations2)

    @staticmethod
    def GenerateNewServiceFromServiceDefinition(newServiceDefinition):
        serviceConfigManagerHandle = win32service.OpenSCManager('', None, win32service.SC_MANAGER_ALL_ACCESS)
        serviceConfigurations = ServiceConfigurations.GenerateNewServiceFromServiceDefinition(newServiceDefinition)
        serviceConfigurations2 = ServiceConfigurations2.GenerateNewServiceFromServiceDefinition(newServiceDefinition)
        return ServiceEntity(serviceConfigManagerHandle, newServiceDefinition.ServiceName, serviceConfigurations, serviceConfigurations2)

    @property
    def ServiceName(self):
        return self.__serviceName.StringValue()

    @property
    def Configurations(self):
        configs = {}
        configs.update(self.__serviceConfigurations.Configurations)
        configs.update(self.__serviceConfigurations2.Configurations)
        return configs

    def Save(self, serviceStartNamePassword=None):
        serviceExists = ServiceEntity.ServiceExists(self.ServiceName)
        self.__serviceConfigurations.Save(serviceExists, self.__serviceConfigManagerHandle, serviceStartNamePassword)
        self.__serviceConfigurations2.Save(self.__serviceConfigManagerHandle)

    def Delete(self):
        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)
            win32service.DeleteService(serviceHandle)
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def Start(self):
        status = self.GetServiceStatus()
        if status['CurrentState'].Win32Value() == CurrentStateType.RUNNING:
            return status

        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)
            win32service.StartService(serviceHandle, {})
            start = time.time()
            status = self.GetServiceStatus()
            while status['CurrentState'].Win32Value() != CurrentStateType.RUNNING:
                if time.time() - start > self._TIMEOUT:
                    raise TimeoutException()
                time.sleep(.5)
                status = self.GetServiceStatus()
            return status
        finally:
            win32service.CloseServiceHandle(serviceHandle)

    def Stop(self):
        status = self.GetServiceStatus()
        if status['CurrentState'].Win32Value() == CurrentStateType.STOPPED:
            return status

        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)

            win32service.ControlService(serviceHandle, win32service.SERVICE_CONTROL_STOP)
            start = time.time()
            status = self.GetServiceStatus()
            while status['CurrentState'].Win32Value() != CurrentStateType.STOPPED:
                if time.time() - start > self._TIMEOUT:
                    raise TimeoutException()
                time.sleep(.5)
                status = self.GetServiceStatus()
            return status
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def Restart(self):
        self.Stop()
        return self.Start()

    def Pause(self):
        status = self.GetServiceStatus()
        if status['CurrentState'].Win32Value() == CurrentStateType.PAUSED:
                return status

        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)
            win32service.ControlService(serviceHandle, win32service.SERVICE_CONTROL_PAUSE)
            start = time.time()
            status = self.GetServiceStatus()
            while status['CurrentState'].Win32Value() != CurrentStateType.PAUSED:
                if time.time() - start > self._TIMEOUT:
                    raise TimeoutException()
                time.sleep(.5)
                status = self.GetServiceStatus()
            return status
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def Continue(self):
        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)
            win32service.ControlService(serviceHandle, win32service.SERVICE_CONTROL_CONTINUE)
            start = time.time()
            status = self.GetServiceStatus()
            while status['CurrentState'].Win32Value() != CurrentStateType.RUNNING:
                if time.time() - start > self._TIMEOUT:
                    raise TimeoutException()
                time.sleep(.5)
                status = self.GetServiceStatus()
            return status
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def Interrogate(self):
        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)
            statusValues = win32service.ControlService(serviceHandle, win32service.SERVICE_CONTROL_INTERROGATE)
            return ServiceStatusEntity(statusValues).Status
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def GetServiceStatus(self):
        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)
            result = win32service.QueryServiceStatusEx(serviceHandle)
            result['ServiceName'] = self.__serviceName.StringValue()
            result['DisplayName'] = self.Configurations['DisplayName']
            statusEntity = ServiceStatusProcessEntity(**result)
            return statusEntity.Status
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def UpdateConfiguration(self, configurationName, value):
        if configurationName in self.__serviceConfigurations.Configurations:
            self.__serviceConfigurations.UpdateConfiguration(configurationName, value)
        elif configurationName in self.__serviceConfigurations2.Configurations:
            self.__serviceConfigurations2.UpdateConfiguration(configurationName, value)
        else:
            raise ValueError('The Configuration Name {0} does not exist'.format(configurationName))

    def GetSid(self):
        serviceHandle = None
        try:
            serviceHandle = ServiceEntity.__getServiceHandle(self.ServiceName, self.__serviceConfigManagerHandle)
            return win32service.QueryServiceConfig2(serviceHandle, win32service.SERVICE_CONFIG_SERVICE_SID_INFO)
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)

    def Exists(self):
        ServiceEntity.ServiceExists(self.ServiceName)

    @staticmethod
    def ServiceExists(serviceName):
        serviceHandle = None
        serviceConfigManagerHandle = None
        try:
            if not serviceConfigManagerHandle:
                serviceConfigManagerHandle = win32service.OpenSCManager('', None, win32service.SC_MANAGER_ALL_ACCESS)
                serviceHandle = ServiceEntity.__getServiceHandle(serviceName, serviceConfigManagerHandle)
            return True
        except Exception, e:
            return False
        finally:
            if serviceHandle:
                win32service.CloseServiceHandle(serviceHandle)
            if serviceConfigManagerHandle:
                win32service.CloseServiceHandle(serviceConfigManagerHandle)

    @staticmethod
    def __getServiceHandle(serviceName, serviceConfigManagerHandle):
        access_rights = [win32service.SERVICE_ALL_ACCESS, win32service.SERVICE_START, win32service.SC_MANAGER_CONNECT]
        for access_right in access_rights:
            try:
                serviceHandle = win32service.OpenService(serviceConfigManagerHandle, serviceName, access_right)
                return serviceHandle
            except Exception, e:
                # try again with different access right
                pass

        raise Exception('Service Name {0} does not exists'.format(self.ServiceName))


    def __eq__(self, other):
        if isinstance(other, ServiceEntity):
            configsAreEqual = self.__serviceConfigurations == other.__serviceConfigurations
            configs2AreEqual = self.__serviceConfigurations2 == other.__serviceConfigurations2
            return configsAreEqual and configs2AreEqual

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

class TimeoutException(Exception):
    def __init__(self, message='The service did not respond to the start or control request in a timely fashion.', errors = None):
        super(TimeoutException, self).__init__(message)
        self.errors = errors
