import win32service
from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory

ConfigurationTypeFactory

class ServiceStatusEntity(object):
    __indexesOfServiceStatusTypes = {'ServiceType': 0,
                                     'CurrentState': 1,
                                     'ControlsAccepted': 2,
                                     'Win32ExitCode': 3,
                                     'ServiceSpecificExitCode': 4,
                                     'CheckPoint': 5,
                                     'WaitHint': 6}

    def __init__(self, statusValues):
        self.Status = {}

        for statusType, index in self.__indexesOfServiceStatusTypes.iteritems():
            if statusType not in statusValues:
                raise ValueError('"{0}" is not a field in the dictionary parameter "statusValues" and needs to be'.format(statusType))
            self.Status[statusType] = ConfigurationTypeFactory.CreateConfigurationType(statusType, statusValues[index])
