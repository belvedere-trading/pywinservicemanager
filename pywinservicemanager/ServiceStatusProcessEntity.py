import win32service
from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory

class ServiceStatusProcessEntity(object):

    __listOfStatusFields = ['ServiceType',
                            'CurrentState',
                            'ControlsAccepted',
                            'Win32ExitCode',
                            'CheckPoint',
                            'WaitHint',
                            'ProcessId',
                            'ServiceFlags',
                            'ServiceName',
                            'DisplayName']

    def __init__(self, **kwargs):
        self.Status = {}
        for field in self.__listOfStatusFields:
            if field not in kwargs:
                raise ValueError('"{0}" is not a field in the dictionary parameter "kwargs" and needs to be'.format(field))
            self.Status[field] = ConfigurationTypeFactory.CreateConfigurationType(field, kwargs[field], True)
