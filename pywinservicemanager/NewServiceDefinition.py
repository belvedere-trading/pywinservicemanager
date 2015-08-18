from pywinservicemanager.ConfigurationTypes import ConfigurationTypeFactory
from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationType


class NewServiceDefinition(object):
    def __init__(self, serviceName, displayName, binaryPathName, startType=None,
                      serviceType=None, errorControl=None, loadOrderGroup=None,
                      dependencies=None, serviceStartName=None, description=None,
                      failureActions=None, failureFlag=None, preShutdownInfo=None,
                      serviceSIDInfo=None, delayedAutoStartInfo=False):

        self.__valdateFailureActions(failureActions)

        self.ServiceName = ConfigurationTypeFactory.CreateConfigurationType('ServiceName', serviceName)
        self.DisplayName = ConfigurationTypeFactory.CreateConfigurationType('DisplayName', displayName)
        self.BinaryPathName = ConfigurationTypeFactory.CreateConfigurationType('BinaryPathName', binaryPathName)
        self.StartType = ConfigurationTypeFactory.CreateConfigurationType('StartType', startType)
        self.ServiceType = ConfigurationTypeFactory.CreateConfigurationType('ServiceType', serviceType)
        self.ErrorControl = ConfigurationTypeFactory.CreateConfigurationType('ErrorControl', errorControl)
        self.LoadOrderGroup = ConfigurationTypeFactory.CreateConfigurationType('LoadOrderGroup', loadOrderGroup)
        self.Dependencies = ConfigurationTypeFactory.CreateConfigurationType('Dependencies', dependencies)
        self.ServiceStartName = ConfigurationTypeFactory.CreateConfigurationType('ServiceStartName', serviceStartName)
        self.Description = ConfigurationTypeFactory.CreateConfigurationType('Description', description)
        self.FailureActions = failureActions
        self.FailureFlag = ConfigurationTypeFactory.CreateConfigurationType('FailureFlag', failureFlag)
        self.PreShutdownInfo = ConfigurationTypeFactory.CreateConfigurationType('PreShutdownInfo', preShutdownInfo)
        self.ServiceSIDInfo = ConfigurationTypeFactory.CreateConfigurationType('ServiceSIDInfo', serviceSIDInfo)
        self.DelayedAutoStartInfo = ConfigurationTypeFactory.CreateConfigurationType('DelayedAutoStartInfo', delayedAutoStartInfo)

    def __valdateFailureActions(self, failureActions):
        if not isinstance(failureActions, FailureActionConfigurationType) and failureActions is not None:
            raise ValueError('The parameter FailureActions must be of type FailureActionConfigurationType or NoneType, but it is of type {0}'.format( type(failureActions).__name__))
