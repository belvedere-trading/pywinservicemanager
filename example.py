from pywinservicemanager.WindowsServiceConfigurationManager import QueryAllServicesStatus, CreateService, GetService, GetServiceStatus, ServiceExists
from pywinservicemanager.NewServiceDefinition import NewServiceDefinition
import pywinservicemanager.ConfigurationTypes as ConfigurationTypes
import pprint
import time
import os

if __name__ == '__main__':

    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    serviceName = 'TestService'
    displayName = 'MyTestService'
    binaryPathName = 'C:\\Windows\\System32\\cmd.exe /c C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe -ExecutionPolicy Bypass -File {0}\\testService.ps1'.format(currentDirectory)
    startType = 'DEMAND_START'
    serviceType= 'WIN32_OWN_PROCESS'
    errorControl= 'ERROR_IGNORE'
    loadOrderGroup = None
    dependencies= ['nsi']
    description= 'This is a test Service'
    failureFlag = False
    preShutdownInfo= 18000
    serviceSIDInfo = 'SID_TYPE_UNRESTRICTED'
    userName = None
    password = None
    delayedAutoStartInfo = False

    failureActionList = []
    delay = 1000
    failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRestartAction(delay))
    failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRunCommandAction(delay))
    resetPeriod = ConfigurationTypes.FailureActionConfigurationResetPeriodType(1)
    rebootMsg = ConfigurationTypes.FailureActionConfigurationRebootMessageType('MyRebootMessage')
    commandLine = ConfigurationTypes.FailureActionConfigurationCommandLineType('MyCommandLine')
    failureActions = ConfigurationTypes.FailureActionConfigurationType(failureActionList, resetPeriod, rebootMsg, commandLine)


    newServiceDefinition = NewServiceDefinition(serviceName=serviceName,
                                                displayName=displayName,
                                                binaryPathName=binaryPathName,
                                                startType=startType,
                                                serviceType=serviceType,
                                                errorControl=errorControl,
                                                loadOrderGroup=loadOrderGroup,
                                                dependencies=dependencies,
                                                serviceStartName=userName,
                                                description=description,
                                                failureActions=failureActions,
                                                failureFlag=failureFlag,
                                                preShutdownInfo=preShutdownInfo,
                                                serviceSIDInfo=serviceSIDInfo,
                                                delayedAutoStartInfo=delayedAutoStartInfo)
    # GetAllServices
    allService = QueryAllServicesStatus(True)
    if len(allService) > 0:
        print '\nFirst Service from "Query All Services"'
        print allService[0]

    #Create a Service
    with CreateService(newServiceDefinition) as service1:
        service1.Save(password)
        print '\n\nNew Service Configruations:'
        pprint.pprint(service1.Configurations)

        #Get an Existing Service
        with GetService(serviceName) as service2:

            print '\n\nGetting Existing Service Configurations:'
            pprint.pprint(service2.Configurations)

            print ''
            print '\n\nGetting Existing Service Status:'
            status = service2.GetServiceStatus()
            pprint.pprint(status)

            print '\n\nThese 2 services sould be that same'
            pprint.pprint(service1 == service2)

            status  = service2.GetServiceStatus()
            status = service2.Start()
            print '\n\nGetting status after Start'
            pprint.pprint(status)

            print ''
            status = service2.Stop()
            print '\n\nGetting status after Stop'
            pprint.pprint(status)

            #Pause Service if that command is accepted by the service
            status = service2.GetServiceStatus()
            if 'ACCEPT_PAUSE_CONTINUE' in status['ControlsAccepted'].StringValue():
                status = service2.Pause()
                print '\n\nGetting status after Pause'
                pprint.pprint(status)

            #Continue Service if that command is accepted by the service
            status = service2.GetServiceStatus()
            if 'ACCEPT_PAUSE_CONTINUE' in status['ControlsAccepted'].StringValue():
                status = service2.Continue()
                print '\n\nGetting status after Continue'
                pprint.pprint(status)

            # Update a configuration of a Service
            service2.UpdateConfiguration('StartType', 'AUTO_START')
            service2.Save()
            print '\n\nGetting Configurations after Updating StartType to AUTO_START'
            pprint.pprint(service2.Configurations)

            # Update a configuration of a Service
            service2.UpdateConfiguration('Description', 'UpdatingTest Description')
            service2.Save()
            print '\n\nGetting Configurations after Updating Description to "UpdatingTest Description"'
            pprint.pprint(service2.Configurations)

            #Service2 now has 2 different configurations
            assert (service2 != service1)

            #Delete Service. If the service is not stopped, the OS will mark the delete as pending until
            #the service is stopped
            status = service2.Stop()
            service2.Delete()
            print '\n\nDeleted Service'

            #Check if Service Exists
            print '\n\nService Exists'
            print service2.Exists()
