import abc
import win32service # pylint: disable=import-error

class ConfigurationBase(object):
    """ This class is the base class for all 'Configruations'. The basic idea of this
        base class is to 'box', the term being loosely used here, all of the constants to have easily readable
        and manipulated values that are mapped to their constant value.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def Mappings(self):
        '''
            An abstact property this returns either None or a dictionary of human readable strings
            that are then mapped to their constants for a given configuration
        '''
        raise NotImplementedError()

    def __init__(self, cls, value, listOfValidTypes, isWin32Value=False):
        self._className = cls.__class__.__name__
        self._mappings = cls.Mappings

        if isWin32Value:
            self.value = self._getWin32Value(value)
            return

        self.__validateMappedValue(value, listOfValidTypes)
        self.value = value

    def _getWin32Value(self, value):
        '''
            Should be used internally to the class. This method will return the human readable value given
            a valid win32 constant for the configuration in question
        '''
        if not self._mappings:
            return value

        if value != None and value not in self._mappings.values():
            ConfigurationBase.__raiseMappingErrorException(self._mappings, self._className, value, isWin32Value=True)
        for key, win32value in self._mappings.iteritems():
            if win32value == value:
                return key

    def __validateMappedValue(self, value, listOfValidTypes):
        '''
            Should be used internally to the class. This method validates that the value passed
            is a valid string that is mapped to a constant. If the value is invalid, and exception will be raised.
        '''
        ConfigurationBase.__validateTypes(value, self._className, listOfValidTypes)
        if not self._mappings:
            return
        if value != None and value not in self._mappings.keys():
            ConfigurationBase.__raiseMappingErrorException(self._mappings, self._className, value, isWin32Value=False)

    @classmethod
    def _getPropertiesAsDict(cls):
        return dict((key, value) for (key, value) in cls._DerivedType().__dict__.items()
                    if not key.startswith('_') and not callable(value) and key != 'Mappings')

    @abc.abstractmethod
    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return

    @abc.abstractmethod
    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return

    @classmethod
    def _DerivedType(cls):
        '''
            This is the type of the derived class
        '''
        return cls

    def __eq__(self, other):
        if not isinstance(other, self._DerivedType()):
            return False
        return self.Win32Value() == other.Win32Value()

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    def __str__(self):
        return str(self.StringValue())

    def __repr__(self):
        return str(self.StringValue())

    @staticmethod
    def __raiseMappingErrorException(mappingDictionary, parameterName, valueRecieved, isWin32Value):
        '''Should be used internally to the class. This method is a helper function that raises an exception
        given an incorrect mapping value
        '''
        if isWin32Value:
            validValues = ','.join([str(value) for value in mappingDictionary.values()])
        else:
            validValues = ','.join(mappingDictionary.keys() + ['None'])

        errorMsg = 'The parameter {0} is not a valid value. Valid values are : {1}. Value received {2}'
        raise ValueError(errorMsg.format(parameterName, validValues, valueRecieved))

    @staticmethod
    def __validateTypes(value, derivedClassName, validTypes):
        '''Should be used internally to the class. This method does type checking for the given configuration.
        If the type of the value is passed is invalid, an excpetion will be raised.
        '''
        validTypeLength = len(validTypes)
        if not validTypes or validTypeLength == 0:
            return True

        isValid = False
        for validType in validTypes:
            if isinstance(value, validType):
                isValid = True

        if not isValid:
            validTypesAsStrings = [validType.__name__ for validType in validTypes]
            validTypesString = ','.join(validTypesAsStrings)
            errorMsg = '{0} is not a valid type. Valid Types are : {1}. Type received {2}'
            raise ValueError(errorMsg.format(derivedClassName, validTypesString, type(value)))
        return True


class ConfigurationTypeFactory(object):

    @staticmethod
    def CreateConfigurationType(typeName, value, isWin32Value=False):
        typeMappings = {'ServiceName': ServiceNameType,
                        'DisplayName': DisplayNameType,
                        'BinaryPathName': BinaryPathNameType,
                        'StartType': ServiceStartType,
                        'ServiceType': ServiceType,
                        'ErrorControl': ErrorControlType,
                        'LoadOrderGroup': LoadOrderGroupType,
                        'Dependencies': DependenciesType,
                        'ServiceStartName': ServiceStartNameType,
                        'Description': DescriptionType,
                        'FailureActions': FailureActionConfigurationType,
                        'FailureFlag': FailureFlagType,
                        'PreShutdownInfo': PreShutdownInfoType,
                        'ServiceSIDInfo': ServiceSIDInfoType,
                        'DelayedAutoStartInfo': DelayedAutoStartInfoType,
                        'CurrentState': CurrentStateType,
                        'ControlsAccepted': ControlsAcceptedType,
                        'Win32ExitCode': Win32ExitCodeType,
                        'CheckPoint': CheckPointType,
                        'WaitHint': WaitHintType,
                        'ProcessId': ProcessIdType,
                        'ServiceFlags': ServiceFlagsType,
                        'TagId': TagIdType}

        if typeName in typeMappings.keys():
            if typeName == 'FailureActions':
                return FailureActionConfigurationType.GetInstanceFromDictionary(value)
            return typeMappings[typeName](value, isWin32Value)

        validValues = ','.join(typeMappings.keys())
        errorMsg = 'The parameter typeName is not a valid value. Value Passed: {0}. Valid values are : {1}'
        raise ValueError(errorMsg.format(value, validValues))


class FailureActionTypeFactory(object):

    @staticmethod
    def CreateNoAction(delay):
        executionAction = FailureActionExecutionType('NONE')
        actionDelay = FailureActionDelayType(delay)
        return FailureActionType(executionAction, actionDelay)

    @staticmethod
    def CreateRestartAction(delay):
        executionAction = FailureActionExecutionType('RESTART')
        actionDelay = FailureActionDelayType(delay)
        return FailureActionType(executionAction, actionDelay)

    @staticmethod
    def CreateRebootAction(delay):
        executionAction = FailureActionExecutionType('REBOOT')
        actionDelay = FailureActionDelayType(delay)
        return FailureActionType(executionAction, actionDelay)

    @staticmethod
    def CreateRunCommandAction(delay):
        executionAction = FailureActionExecutionType('RUN_COMMAND')
        actionDelay = FailureActionDelayType(delay)
        return FailureActionType(executionAction, actionDelay)


class BinaryPathNameType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [str, unicode]
        super(BinaryPathNameType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class CheckPointType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [int]
        super(CheckPointType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class ControlsAcceptedType(ConfigurationBase):
    ACCEPT_NETBINDCHANGE = win32service.SERVICE_ACCEPT_NETBINDCHANGE
    ACCEPT_PARAMCHANGE = win32service.SERVICE_ACCEPT_PARAMCHANGE
    ACCEPT_PAUSE_CONTINUE = win32service.SERVICE_ACCEPT_PAUSE_CONTINUE
    ACCEPT_PRESHUTDOWN = win32service.SERVICE_ACCEPT_PRESHUTDOWN
    ACCEPT_SHUTDOWN = win32service.SERVICE_ACCEPT_SHUTDOWN
    ACCEPT_STOP = win32service.SERVICE_ACCEPT_STOP
    ACCEPT_HARDWAREPROFILECHANGE = win32service.SERVICE_ACCEPT_HARDWAREPROFILECHANGE
    ACCEPT_POWEREVENT = win32service.SERVICE_ACCEPT_POWEREVENT
    ACCEPT_SESSIONCHANGE = win32service.SERVICE_ACCEPT_SESSIONCHANGE

    @property
    def Mappings(self):
        return None

    @property
    def Types(self):
        returnValue = []
        for key, value in self._getPropertiesAsDict().iteritems():
            if key == 'Types':
                continue
            if (value & self.value) == value:
                returnValue.append(key)
        return returnValue

    def __init__(self, value, isWin32Value=False):
        validTypes = [int]
        super(ControlsAcceptedType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.Types

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class CurrentStateType(ConfigurationBase):
    CONTINUE_PENDING = win32service.SERVICE_CONTINUE_PENDING
    PAUSE_PENDING = win32service.SERVICE_PAUSE_PENDING
    PAUSED = win32service.SERVICE_PAUSED
    RUNNING = win32service.SERVICE_RUNNING
    START_PENDING = win32service.SERVICE_START_PENDING
    STOP_PENDING = win32service.SERVICE_STOP_PENDING
    STOPPED = win32service.SERVICE_STOPPED

    @property
    def Mappings(self):
        return self._getPropertiesAsDict()

    def __init__(self, value, isWin32Value=False):
        validTypes = [int, str]
        super(CurrentStateType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.Mappings[self.value]


class DelayedAutoStartInfoType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        if value is None:
            value = False
        validTypes = [bool]
        super(DelayedAutoStartInfoType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class DependenciesType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [list, type(None)]
        super(DependenciesType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class DescriptionType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [unicode, str, type(None)]
        super(DescriptionType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class DisplayNameType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [unicode, str]
        super(DisplayNameType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class ErrorControlType(ConfigurationBase):
    ERROR_IGNORE = win32service.SERVICE_ERROR_IGNORE
    ERROR_NORMAL = win32service.SERVICE_ERROR_NORMAL
    ERROR_SEVERE = win32service.SERVICE_ERROR_SEVERE
    ERROR_CRITICAL = win32service.SERVICE_ERROR_CRITICAL

    @property
    def Mappings(self):
        return self._getPropertiesAsDict()

    def __init__(self, value, isWin32Value=False):
        if value is None:
            value = 'ERROR_NORMAL'
        validTypes = []
        super(ErrorControlType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.Mappings[self.value]


class FailureActionConfigurationCommandLineType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [str, unicode, type(None)]
        super(FailureActionConfigurationCommandLineType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class FailureActionConfigurationRebootMessageType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [str, unicode, type(None)]
        super(FailureActionConfigurationRebootMessageType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class FailureActionConfigurationResetPeriodType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [int, type(None)]
        super(FailureActionConfigurationResetPeriodType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class FailureActionConfigurationType(ConfigurationBase):

    @property
    def Mappings(self):
        return None
    #pylint: disable=R0913
    def __init__(self, failureActionsTypeList=None, resetPeriodType=None,
                 rebootMessageType=None, commandLineType=None, isWin32Value=False):
        self.__validateFailureActionsTypeListParameter(failureActionsTypeList)
        super(FailureActionConfigurationType, self).__init__(self, None, [], isWin32Value)

        if failureActionsTypeList is None:
            failureActionsTypeList = []
        self.failureActionsTypeList = failureActionsTypeList

        if not isinstance(resetPeriodType, FailureActionConfigurationResetPeriodType):
            resetPeriodType = FailureActionConfigurationResetPeriodType(resetPeriodType)
        self.resetPeriodType = resetPeriodType

        if not isinstance(rebootMessageType, FailureActionConfigurationRebootMessageType):
            rebootMessageType = FailureActionConfigurationRebootMessageType(rebootMessageType)
        self.rebootMessageType = rebootMessageType

        if not isinstance(commandLineType, FailureActionConfigurationCommandLineType):
            commandLineType = FailureActionConfigurationCommandLineType(commandLineType)
        self.commandLineType = commandLineType

    @staticmethod
    def GetInstanceFromDictionary(configruationAsDict):

        if 'ResetPeriod' in configruationAsDict:
            resetPeriod = configruationAsDict['ResetPeriod']

        if 'RebootMsg' in configruationAsDict:
            rebootMessage = configruationAsDict['RebootMsg']

        if 'Command' in configruationAsDict:
            commandLine = configruationAsDict['Command']

        failureActions = []
        if 'Actions' in configruationAsDict:
            for action in  configruationAsDict['Actions']:
                failureActionExecutionType = FailureActionExecutionType(action[0], True)
                failureActionDelayType = FailureActionDelayType(action[1], True)
                failureAction = FailureActionType(failureActionExecutionType, failureActionDelayType)
                failureActions.append(failureAction)

        return FailureActionConfigurationType(failureActions,
                                              FailureActionConfigurationResetPeriodType(resetPeriod),
                                              FailureActionConfigurationRebootMessageType(rebootMessage),
                                              FailureActionConfigurationCommandLineType(commandLine))


    def StringValue(self):
        """Retrieve the data as it's string Value"""
        actions = []
        for action in self.failureActionsTypeList:
            actions.append(action.StringValue())

        return str({'ResetPeriod': self.resetPeriodType.StringValue(),
                    'RebootMsg': self.rebootMessageType.StringValue(),
                    'Command': self.commandLineType.StringValue(),
                    'Actions': str(actions)})


    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        failureActions = []
        for failureAction in self.failureActionsTypeList:
            failureActions.append(failureAction.Win32Value())

        return {'ResetPeriod': self.resetPeriodType.Win32Value(),
                'RebootMsg': self.rebootMessageType.Win32Value(),
                'Command': self.commandLineType.Win32Value(),
                'Actions': failureActions}

    def __eq__(self, other):
        if not isinstance(other, self._DerivedType()):
            return False
        return self.resetPeriodType == other.resetPeriodType and \
               self.rebootMessageType == other.rebootMessageType and \
               self.commandLineType == other.commandLineType and \
               self.failureActionsTypeList == other.failureActionsTypeList

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    @staticmethod
    def __validateFailureActionsTypeListParameter(failureActionsTypeList):
        if failureActionsTypeList is None:
            return
        if not isinstance(failureActionsTypeList, list):
            msg = 'failureActionsTypeList parameter must be of type list of FailureActionType, but the oject is not a list'
            raise ValueError(msg)
        for element in failureActionsTypeList:
            if not isinstance(element, FailureActionType):
                msg = 'failureActionsTypeList parameter must be of type list of FailureActionType, '
                msg += 'but not all elements are of Type FailureActionType'
                raise ValueError(msg)


class FailureActionDelayType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [int, long, type(None)]
        super(FailureActionDelayType, self).__init__(self, value, validTypes, isWin32Value)
        if not value  is None:
            value = long(value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class FailureActionExecutionType(ConfigurationBase):
    NONE = win32service.SC_ACTION_NONE
    RESTART = win32service.SC_ACTION_RESTART
    REBOOT = win32service.SC_ACTION_REBOOT
    RUN_COMMAND = win32service.SC_ACTION_RUN_COMMAND

    @property
    def Mappings(self):
        return self._getPropertiesAsDict()

    def __init__(self, value, isWin32Value=False):
        if value is None:
            value = 'NONE'
        super(FailureActionExecutionType, self).__init__(self, value, [], isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.Mappings[self.value]


class FailureActionType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, failureActionExecutionType, failureActionDelayType, isWin32Value=False):
        if not isinstance(failureActionExecutionType, FailureActionExecutionType) and \
           not isinstance(failureActionDelayType, FailureActionDelayType):
            msg = 'The argument "failureActionExecutionType" and "failureActionDelayType" are not of the types of their namesakes, '
            msg += 'and should be. failureActionExecutionType is of type {0} and failureActionDelayType is of type of {1}'
            raise ValueError(msg.format(type(failureActionExecutionType).__name__, type(failureActionDelayType).__name__))

        super(FailureActionType, self).__init__(self, None, [], isWin32Value)
        self.failureActionExecutionType = failureActionExecutionType if failureActionExecutionType else FailureActionExecutionType(None)
        self.failureActionDelayType = failureActionDelayType if failureActionDelayType else FailureActionDelayType(None)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return {'FailureActionType' : self.failureActionExecutionType.StringValue(),
                'Delay': self.failureActionDelayType.StringValue()}

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return (self.failureActionExecutionType.Win32Value(), self.failureActionDelayType.Win32Value())

    def __eq__(self, other):
        if not isinstance(other, FailureActionType):
            return False
        return self.failureActionExecutionType == other.failureActionExecutionType and \
               self.failureActionDelayType == other.failureActionDelayType


class FailureFlagType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        if value is None:
            value = False
        validTypes = [bool]
        super(FailureFlagType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class LoadOrderGroupType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        if isinstance(value, str):
            value = unicode(value)
        if value is None:
            value = unicode('')
        validTypes = [unicode, str, type(None)]
        super(LoadOrderGroupType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value

class PreShutdownInfoType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [int, long, type(None)]
        super(PreShutdownInfoType, self).__init__(self, value, validTypes, isWin32Value)

        if isinstance(value, int):
            value = long(value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class ProcessIdType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [int]
        super(ProcessIdType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class ServiceFlagsType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [int]
        super(ServiceFlagsType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class ServiceNameType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [unicode, str]
        super(ServiceNameType, self).__init__(self, value, validTypes, isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class ServiceSIDInfoType(ConfigurationBase):
    SID_TYPE_NONE = win32service.SERVICE_SID_TYPE_NONE
    SID_TYPE_RESTRICTED = win32service.SERVICE_SID_TYPE_RESTRICTED
    SID_TYPE_UNRESTRICTED = win32service.SERVICE_SID_TYPE_UNRESTRICTED

    def __init__(self, value, isWin32Value=False):
        if value is None:
            value = 'SID_TYPE_NONE'
        super(ServiceSIDInfoType, self).__init__(self, value, [str], isWin32Value)

    @property
    def Mappings(self):
        return self._getPropertiesAsDict()

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.Mappings[self.value]


class ServiceStartNameType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        validTypes = [unicode, str, type(None)]
        super(ServiceStartNameType, self).__init__(self, value, validTypes, isWin32Value)

        if value is None:
            self.value = u'LocalSystem'

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class ServiceStartType(ConfigurationBase):
    AUTO_START = win32service.SERVICE_AUTO_START
    DEMAND_START = win32service.SERVICE_DEMAND_START
    BOOT_START = win32service.SERVICE_BOOT_START
    DISABLED = win32service.SERVICE_DISABLED
    SYSTEM_START = win32service.SERVICE_SYSTEM_START

    @property
    def Mappings(self):
        return self._getPropertiesAsDict()

    def __init__(self, value, isWin32Value=False):
        if value is None:
            value = 'DEMAND_START'
        super(ServiceStartType, self).__init__(self, value, [], isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.Mappings[self.value]


class ServiceType(ConfigurationBase):
    WIN32_SHARE_PROCESS = win32service.SERVICE_WIN32_SHARE_PROCESS
    WIN32_OWN_PROCESS = win32service.SERVICE_WIN32_OWN_PROCESS
    KERNEL_DRIVER = win32service.SERVICE_KERNEL_DRIVER
    FILE_SYSTEM_DRIVER = win32service.SERVICE_FILE_SYSTEM_DRIVER
    INTERACTIVE_SHARE_PROCESS = win32service.SERVICE_INTERACTIVE_PROCESS | win32service.SERVICE_WIN32_SHARE_PROCESS
    INTERACTIVE_OWN_PROCESS = win32service.SERVICE_INTERACTIVE_PROCESS | win32service.SERVICE_WIN32_OWN_PROCESS

    @property
    def Mappings(self):
        return self._getPropertiesAsDict()

    def __init__(self, value, isWin32Value=False):
        if value is None:
            value = 'WIN32_OWN_PROCESS'
        super(ServiceType, self).__init__(self, value, [], isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.Mappings[self.value]


class TagIdType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        super(TagIdType, self).__init__(self, value, [], isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class WaitHintType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        super(WaitHintType, self).__init__(self, value, [int], isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value


class Win32ExitCodeType(ConfigurationBase):

    @property
    def Mappings(self):
        return None

    def __init__(self, value, isWin32Value=False):
        super(Win32ExitCodeType, self).__init__(self, value, [int], isWin32Value)

    def StringValue(self):
        """Retrieve the data as it's string Value"""
        return self.value

    def Win32Value(self):
        """Retrieve the data as it's win32 api Value"""
        return self.value
