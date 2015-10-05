# Python Windows Service Manager
---

Python Windows Service Manager is a python package that helps to easily manage windows services, mirroring the functionality of the Windows Service Controller Utility (sc.exe). It allows to easily manage both Driver and Win32 services. The following can be achieved using this package:

 * Create, Remove, or Update a service configuration
 * Query a specific or all Service Statuses
 * Get a service configuration
 * Verify a service exists
 * Start, Stop, Pause, Continue, Interrogate a service

## Pre-requisites
    pywin32>=219
    * **This cannot be installed via pypi.
    This has to be the precompiled version.**
## Installation
* Clone this repository
* Put the repo dir in your PYTHONPATH
* Run:
    ```
    python setup.py install
    ```

## How to run Unit Tests

1.  pip install nose, mock
2.  From the module's root directory, run 'nosetests .'

## Usage
---
This module attempts to follow the ORM design Pattern, where the Class WindowsServiceConfigurationManager would be your context, and object that represents the data store is a ServiceEntity.

### WindowsServiceConfigurationManager
---
This is the entry point for all operations. This module has static methods that:
- Creates or Gets a Service, and returns a Entity object that represents that service
- Query All Service Statuses
- Verify a service exists
- Gets a specific service's status

The following Describes these operations in detail:

* **Create a New Service:**

    The CreateService() function takes a parameter of Type NewServiceDefinition. The following describes the NewServiceDefinition constructor and its arguments:

    **NewServiceDefinition:**
    1.  **serviceName *(Required)***: The name of the service.
          * Valid Values: Any non empty string
    2.  **displayName *(Required)***: Indicates the friendly name that identifies the service to the user
        * Valid Values: Any non empty string
    3.  **binaryPathName *(Required)***: Specifies the path to the executable file for the service.
        * Validate Values: Any non empty string that points to an executable
    2.  **startType**: Indicates how and when the service is started
        * Valid String Values: AUTO_START, DEMAND_START, BOOT_START, DISABLED, SYSTEM_START, INTERACTIVE_SHARE_PROCESS,  INTERACTIVE_OWN_PROCESS
        * Default Value:  DEMAND_START
    3.  **serviceType**: Represents the type of the service
        * Valid String Values: WIN32_SHARE_PROCESS, WIN32_OWN_PROCESS, KERNEL_DRIVER, FILE_SYSTEM_DRIVER
        * Default Value:  WIN32_OWN_PROCESS
    4.  **errorControl**: Specifies how to proceed if the driver for the service or device fails to load or initialize properly
        * Valid String Values: ERROR_CRITICAL, ERROR_IGNORE, ERROR_NORMAL, ERROR_SEVERE
        * Default Value:  ERROR_NORMAL
    5.  **loadOrderGroup**: The name of the load ordering group of which this service is a member
        * Valid Value: String of Group Name
        * Default Value: None
    5.  **dependencies**:
        * Valid Value: Array of Existing Service Names
        * Default Value: None
    6.  **serviceStartName**: Name of the account in which the service runs
        * Valid Value: A valid user account as a string
        * Default Value: The System Account
    7.  **description**: The description of the service
        * Valid Value: Any string
        * Default Value: An empty string
    8.  **failureActions**: Represents the action the service controller should take on each failure of a service
        * Valid Value: FailureActionConfigurationType
        * Default Value: None

        ** ***See 'Complex Example for Creating Service' for an example, or the Section that describes the 'FailureActionConfigurationType'***
    9.  **failureFlag**: Specifies whether recovery actions will be triggered when a service stops as the result of an error
        * Valid Value: Boolean
        * Default Value: False
    10. **preShutdownInfo**: The time-out value, in milliseconds.
        * Valid Value: long or int
        * Default Value: 180,000 milliseconds
    11. **serviceSIDInfo**: Represents a service security identifier
        * Valid String Value: SID_TYPE_NONE, SID_TYPE_RESTRICTED, SID_TYPE_UNRESTRICTED
        * Default Value: SID_TYPE_UNRESTRICTED
    12. **delayedAutoStartInfo**: The value that indicates whether the service should be delayed from starting until other automatically started services are running.
        * Valid Value: Boolean
        * Default Value: False

    **Most simplistic example of creating a service**
     ```

    from pywinservicemanager.WindowsServiceConfigurationManager import CreateService
    from pywinservicemanager.NewServiceDefinition import NewServiceDefinition

    serviceName = 'TestService'
    displayName = 'MyTestService'
    binaryPathName = 'c:\\myBinary.exe'

    newServiceDefinition = NewServiceDefinition(serviceName=serviceName,
                                                displayName=displayName,
                                                binaryPathName=binaryPathName)

    myService = CreateService(newServiceDefinition)

    # Note that the Create Service Method just creates the entity in memeory.
    # To save it to the 'DataStore', you must call Save()
    myService.Save()
    ```

    **Most complex example of creating a service**
     ```
    from pywinservicemanager.WindowsServiceConfigurationManager import CreateService
    from pywinservicemanager.NewServiceDefinition import NewServiceDefinition
    import pywinservicemanager.ConfigurationTypes as ConfigurationTypes

    serviceName = 'TestService'
    displayName = 'MyTestService'
    binaryPathName = 'c:\\myBinary.exe'
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
    resetPeriod = 1
    rebootMsg = 'MyRebootMessage'
    commandLine = 'MyCommandLine'
    failureActions = FailureActionConfigurationType(failureActionList, resetPeriod, rebootMsg, commandLine)


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

    myService = CreateService(newServiceDefinition)

    # Note that the Create Service Method just creates the entity in memeory.
    # To save it to the 'DataStore', you must call Save()
    myService.Save(password)

    ```

* **Delete a Service:**
     ```

    from pywinservicemanager.WindowsServiceConfigurationManager import GetService
    serviceName = "TestService"
    myService = GetService(serviceName)

    # Note that the GetService Method reads for the data store and creates the entity in memeory.
    # To delete it from the 'DataStore', you must call Delete()
    myService.Delete()

    ```

* **Query All Services Statuses**:
    Returns a list of each installed service's status. (Please see status definition below for more details)
    ```

    from pywinservicemanager.WindowsServiceConfigurationManager import QueryAllServicesStatus

    statuses = QueryAllServicesStatus()
    print statuses

    ```
* **Service Exists**:
    ```

    from pywinservicemanager.WindowsServiceConfigurationManager import ServiceExists

    serviceName = 'TestService'
    serviceExists = ServiceExists(serviceName)
    print serviceExists

    ```

* **Get Service Status**:
    Returns a single service's status (Please see status definition below for more details)
    ```

    from pywinservicemanager.WindowsServiceConfigurationManager import GetServiceStatus
    serviceName = 'TestService'
    serviceStatus = GetServiceStatus(serviceName)
    print serviceStatus

    ```

### ServiceEntity
---
This is the object that maps to the service.

The object contains the following commands for each service:
- Save
- Delete
- Start
- Stop
- Pause
- Continue
- Interrogate
- GetServiceStatus
- UpdateConfiguration
- Exists

You need to make sure that the commands Pause, Continue, and Interrogate are able to be excepted by the service. The accepted commands are dependent on 2 things. First, if the service is configurated to accept such commands, and second, if the current state of the service allows that command to be called on the service. The code examples below shows how to deal with this. Furthermore, if a service is not in a "Running" state, than Stop cannot be called. Vis-a-versa, if a service is not in a "Stopped" state, then Start cannot be called.


* **UpdateConfiguration**: Used to update a service's configuration in memeory. You must call the save method to persist the service.

    ```
    from pywinservicemanager.WindowsServiceConfigurationManager import GetService

    serviceName = 'TestService'
    myService = GetService(serviceName)
    myService.UpdateConfiguration('StartType', 'DEMAND_START')
    myService.Save()

    ```
* **Save**: Saves the current state of the ServiceEntity as a service in the OS. You can pass a password as an argument to this function if one is needed, the default value is `None`
    ```
    from pywinservicemanager.WindowsServiceConfigurationManager import GetService

    serviceName = 'TestService'
    myService = GetService(serviceName)
    myService.UpdateConfiguration('ServiceStartName', 'MyDomain\\MyNewUser')
    myService.Save('MyNewPassword')

    ```
* **Delete**: Deletes the Service
   Deletes a service. Please note that you if your service is running, you will need to stop the service for it to be deleted. Also, if anything has a handle open to the service, those need to be closed as well. If Delete() is called on service in which a handle is open, then it will be 'Marked for Deletion' and will not be deleted until all handles are closed.
   ```
   from pywinservicemanager.WindowsServiceConfigurationManager import GetService

   serviceName = 'TestService'
   myService = GetService(serviceName)
   myService.Delete()

     ```

* **Start**: Deletes the Service
  Starts a given service that has is stopped. If the service is not stopped, an exception will be thrown. Also, if the service does not return from the Start command within 30 seconds, a TimeoutException is thrown

   ```
   from pywinservicemanager.WindowsServiceConfigurationManager import GetService

   serviceName = 'TestService'
   myService = WindowsServiceConfigurationManager.GetService(serviceName)
   myService.Start()

     ```

* **Stop**: Stops the Service
  Stops a given service that is started. If the service is not started, an exception will be thrown. Also, if the service does not return from the Stop command within 30 seconds, a TimeoutException is thrown
   ```
   from pywinservicemanager.WindowsServiceConfigurationManager import GetService

   serviceName = 'TestService'
   myService = WindowsServiceConfigurationManager.GetService(serviceName)
   myService.Stop()

   ```

* **Continue**: Continues the Service after it was paused
  Stops a given service that is Paused and/or has the value ACCEPT_PAUSE_CONTINUE in ControlsAccepted. If not, an exception will be thrown. Also, if the service does not return from the Continue command within 30 seconds, a TimeoutException is thrown
   ```
    from pywinservicemanager.WindowsServiceConfigurationManager import GetService

    serviceName = 'TestService'
    myService = GetService(serviceName)
    status = myService.GetServiceStatus()
    if 'ACCEPT_PAUSE_CONTINUE' in status['ControlsAccepted']:
        myService.Continue()

     ```

* **Pause**: Pauses the Service
  Pauses a given service that is Paused and/or has the value ACCEPT_PAUSE_CONTINUE in ControlsAccepted. If not, an exception will be thrown. Also, if the service does not return from the Pause command within 30 seconds, a TimeoutException is thrown
   ```
    from pywinservicemanager.WindowsServiceConfigurationManager import GetService

    serviceName = 'TestService'
    myService = GetService(serviceName)
    myServiceStatus = myService.GetServiceStatus().Status
    if 'ACCEPT_PAUSE_CONTINUE' in status['ControlsAccepted']:
        myService.Pause()

     ```

* **Interrogate**: Interrogates the Service
   ```
    from pywinservicemanager.WindowsServiceConfigurationManager import GetService

    serviceName = 'TestService'
    myService = GetService(serviceName)
    myService.Interrogate()

     ```

* **GetServiceStatus**: Deletes the Service
  Returns a the service's status (Please see status definition below for more details)
   ```
   from pywinservicemanager.WindowsServiceConfigurationManager import GetService

   serviceName = 'TestService'
   myService = WindowsServiceConfigurationManager.GetService(serviceName)
   status = myService.GetServiceStatus()
   print status

     ```

* **Exists**: Deletes the Service
  Returns if the service exists
   ```
   from pywinservicemanager.WindowsServiceConfigurationManager import Exists

   serviceName = 'TestService'
   myService = WindowsServiceConfigurationManager.GetService(serviceName)
   print myService.Exists()

     ```

### FailureActionConfigurationType
---
Represents the action the service controller should take on each failure of a service. A service is considered failed when it terminates without reporting a status of SERVICE_STOPPED to the service controller

The constructor of this object takes the following parameters:
1. failureActionsTypeList
    * Valid Value: List of FailureActionType Objects (see below)
    * Default:Value None
2. resetPeriodType: The time after which to reset the failure count to zero if there are no failures, in seconds
    * Valid Value: int or ResetPeriodType(see below)
    * Default:Value None
3. rebootMessageType: The message to be broadcast to server users before rebooting in response to the SC_ACTION_REBOOT service controller action
    * Valid Value: string or RebootMessageType (see below)
    * Default:Value None
4. commandLineType:  The command line of the process for the CreateProcess function to execute in response to the SC_ACTION_RUN_COMMAND service controller action. This process runs under the same account as the service.
    * Valid Value: string or CommandLineType (see below)
    * Default:Value None

Example:
```
import pywinservicemanager.ConfigurationTypes as ConfigurationTypes

failureActionList = []
delay = 1000
failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRestartAction(delay))
failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRunCommandAction(delay))
resetPeriod = ConfigurationTypes.FailureActionConfigurationResetPeriodType(1)
rebootMsg = ConfigurationTypes.FailureActionConfigurationRebootMessageType('MyRebootMessage')
commandLine = ConfigurationTypes.FailureActionConfigurationCommandLineType('MyCommandLineCommand')
failureActions = ConfigurationTypes.FailureActionConfigurationType(failureActionList, resetPeriod, rebootMsg, commandLine)
#or
failureActionList = []
delay = 1000
failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRestartAction(delay))
failureActionList.append(ConfigurationTypes.FailureActionTypeFactory.CreateRunCommandAction(delay))
resetPeriod = 1
rebootMsg = 'MyRebootMessage'
commandLine = 'MyCommandLine'
failureActions = ConfigurationTypes.FailureActionConfigurationType(failureActionList, resetPeriod, rebootMsg, commandLine)

```

[More information about FailureActionConfiguration Mapping](https://msdn.microsoft.com/en-us/library/windows/desktop/ms685939(v=VS.85).aspx)

### FailureActionType
---
Represents an action that the service control manager can perform.

A FailureAction type can be reurned by the factory object FailureActionTypeFactory, where there are 4 methods defined and an int which represents the delaly as the input parameter:
1. Factory Methods:
    * FailureActionTypeFactory.CreateNoAction(delay): No action.
    * FailureActionTypeFactory.CreateRestartAction(delay): Restart the service.
    * FailureActionTypeFactory.CreateRebootAction(delay): Reboot the computer. If the service uses the reboot action, the caller must have the SE_SHUTDOWN_NAME [privilege](https://msdn.microsoft.com/en-us/library/windows/desktop/aa379306(v=vs.85).aspx). For more information, see [Running with Special Privileges.](https://msdn.microsoft.com/en-us/library/windows/desktop/ms717802(v=vs.85).aspx)
    * FailureActionTypeFactory.CreateRunCommandAction(delay):  Run a command.
2.  delay: The time to wait before performing the specified action, in milliseconds.

Example:
```
import pywinservicemanager.ConfigurationTypes as ConfigurationTypes

myAction = ConfigurationTypes.FailureActionTypeFactory.CreateRestartAction(300)
```
[More information about FailureAction](https://msdn.microsoft.com/en-us/library/windows/desktop/ms685126(v=vs.85).aspx)

### ResetPeriodType
---
The time after which to reset the failure count to zero if there are no failures, in seconds.
The input is of time int

Example:
```
import pywinservicemanager.ConfigurationTypes as ConfigurationTypes

resetPeriod = ConfigurationTypes.FailureActionConfigurationResetPeriodType(1)

```

### FailureActionConfigurationRebootMessageType
---
The message to be broadcast to server users before rebooting in response to the SC_ACTION_REBOOT service controller action.
If this value is None, the reboot message is unchanged. If the value is an empty string (""), the reboot message is deleted and no message is broadcast.

Example:
```
import pywinservicemanager.ConfigurationTypes as ConfigurationTypes

rebootMessage = ConfigurationTypes.FailureActionConfigurationRebootMessageType("My Reboot Message")

```

### FailureActionConfigurationRebootMessageType
---
The command line of the process for the CreateProcess function to execute in response to the SC_ACTION_RUN_COMMAND service controller action. This process runs under the same account as the service.
If this value is None, the command is unchanged. If the value is an empty string (""), the command is deleted and no program is run when the service fails.

Example:
```
import pywinservicemanager.ConfigurationTypes as ConfigurationTypes

commandLine = ConfigurationTypes.FailureActionConfigurationCommandLineType("myCmd.exe")

```

### Further Information
---
For more information the windows API implemented in the package and/or how the service controller utility works, please consult [win32service documentation](http://docs.activestate.com/activepython/2.6/pywin32/win32service.html)
