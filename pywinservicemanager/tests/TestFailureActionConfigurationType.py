from mock import MagicMock, patch
import unittest

class TestFailureActionConfigurationType(unittest.TestCase):

    def setUp(self):
        self.mockwin32service = MagicMock()
        self.patcher = patch.dict('sys.modules', {'win32service': self.mockwin32service})
        self.patcher.start()

        self.mockwin32service.SC_ACTION_NONE = 0
        self.mockwin32service.SC_ACTION_REBOOT = 1
        self.mockwin32service.SC_ACTION_RESTART = 2
        self.mockwin32service.SC_ACTION_RUN_COMMAND =3

        global FailureActionType
        global FailureActionExecutionType
        global FailureActionDelayType
        global FailureActionConfigurationType
        global FailureActionConfigurationResetPeriodType
        global FailureActionConfigurationRebootMessageType
        global FailureActionConfigurationCommandLineType
        global FailureActionTypeFactory
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationType
        from pywinservicemanager.ConfigurationTypes import FailureActionType
        from pywinservicemanager.ConfigurationTypes import FailureActionExecutionType
        from pywinservicemanager.ConfigurationTypes import FailureActionDelayType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationResetPeriodType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationRebootMessageType
        from pywinservicemanager.ConfigurationTypes import FailureActionConfigurationCommandLineType
        from pywinservicemanager.ConfigurationTypes import FailureActionTypeFactory

    def tearDown(self):
        self.patcher.stop()

    def TestInitWithDefaultParameters(self):
        value = None
        config1 = FailureActionConfigurationType()
        config2 = FailureActionConfigurationType()
        self.assertEquals(config1.StringValue(), config2.StringValue())
        self.assertEquals(config1.Win32Value(), config2.Win32Value())

    def TestInitWithParametersNone(self):
        value = None
        config1 = FailureActionConfigurationType(value, value, value, value)
        config2 = FailureActionConfigurationType(value, value, value, value)
        self.assertEquals(config1.StringValue(), config2.StringValue())
        self.assertEquals(config1.Win32Value(), config2.Win32Value())

    def TestInitWithNonListOfFailureActions(self):
        action = FailureActionTypeFactory.CreateNoAction(long(1))
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        self.assertRaises(ValueError, FailureActionConfigurationType, action, resetPeriod, rebootMsg, commandLine)

    def TestInitWithUnBoxedResetPeriod(self):
        actions = [ FailureActionTypeFactory.CreateRestartAction(long(1))]
        resetPeriod = 1
        resetPeriod1 = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        config1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        config2 = FailureActionConfigurationType(actions, resetPeriod1, rebootMsg, commandLine)
        self.assertEquals(config1.StringValue(), config2.StringValue())
        self.assertEquals(config1.Win32Value(), config2.Win32Value())

    def TestInitWithUnBoxedRebootMessage(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = 'MyRebootMessage'
        rebootMsg1 = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        config1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        config2 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg1, commandLine)
        self.assertEquals(config1.StringValue(), config2.StringValue())
        self.assertEquals(config1.Win32Value(), config2.Win32Value())

    def TestInitWithUnBoxedCommandLine(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = 'MyCommandLine'
        commandLine1 = FailureActionConfigurationCommandLineType('MyCommandLine')
        config1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        config2 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine1)
        self.assertEquals(config1.StringValue(), config2.StringValue())
        self.assertEquals(config1.Win32Value(), config2.Win32Value())

    def TestInitWithListOfFailureActions(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        failureActions = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        t = failureActions.StringValue()
        self.assertEquals(failureActions.StringValue(), failureActions.StringValue())
        self.assertEquals(failureActions.Win32Value(), failureActions.Win32Value())

    def TestEquals(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        failureActions1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        failureActions2 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        self.assertEquals(failureActions1, failureActions2)

    def TestNotEqualsCommandLine(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        commandLine2 = FailureActionConfigurationCommandLineType('MyCommandLine2')
        failureActions1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        failureActions2 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine2)
        self.assertNotEquals(failureActions1, failureActions2)

    def TestNotEqualsRebootMessage(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        rebootMsg1 = FailureActionConfigurationRebootMessageType('MyRebootMessage1')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        failureActions1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        failureActions2 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg1, commandLine)
        self.assertNotEquals(failureActions1, failureActions2)

    def TestNotEqualsResetPeriod(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        resetPeriod2 = FailureActionConfigurationResetPeriodType(2)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        failureActions1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        failureActions2 = FailureActionConfigurationType(actions, resetPeriod2, rebootMsg, commandLine)
        self.assertNotEquals(failureActions1, failureActions2)

    def TestNotEqualsActions(self):
        actions = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        actions1 = [ FailureActionTypeFactory.CreateNoAction(long(2))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        resetPeriod2 = FailureActionConfigurationResetPeriodType(2)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        failureActions1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        failureActions2 = FailureActionConfigurationType(actions1, resetPeriod, rebootMsg, commandLine)
        self.assertNotEquals(failureActions1, failureActions2)

    def TestNotEqualsActions2(self):
        actions = [ FailureActionTypeFactory.CreateRebootAction(long(1))]
        actions1 = [ FailureActionTypeFactory.CreateNoAction(long(1))]
        resetPeriod = FailureActionConfigurationResetPeriodType(1)
        resetPeriod2 = FailureActionConfigurationResetPeriodType(2)
        rebootMsg = FailureActionConfigurationRebootMessageType('MyRebootMessage')
        commandLine = FailureActionConfigurationCommandLineType('MyCommandLine')
        failureActions1 = FailureActionConfigurationType(actions, resetPeriod, rebootMsg, commandLine)
        failureActions2 = FailureActionConfigurationType(actions1, resetPeriod, rebootMsg, commandLine)
        self.assertNotEquals(failureActions1, failureActions2)
