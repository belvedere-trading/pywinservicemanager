Add-Type -ReferencedAssemblies System.ServiceProcess -Language CSharp @"
using System;
using System.Diagnostics;
using System.ServiceProcess;

namespace WindowsService 
{
    public class WindowsService : ServiceBase
    {
        public WindowsService()
        {
            this.ServiceName = "TestService";
            this.CanPauseAndContinue = true;
            this.CanStop = true;
            System.IO.File.AppendAllText("C:\\temp.txt", "In Constructor" + Environment.NewLine);
        }

        public static WindowsService GetWindowsService()
        {
            return new WindowsService();
        }

        protected override void Dispose(bool disposing)
        {
            base.Dispose(disposing);
        }

        protected override void OnStart(string[] args)
        {
            System.IO.File.AppendAllText("C:\\temp.txt", "In OnStart" + Environment.NewLine);
            base.OnStart(args);
        }

        protected override void OnStop()
        {
            System.IO.File.AppendAllText("C:\\temp.txt", "In onStop." + Environment.NewLine);
            base.OnStop();
        }

        protected override void OnPause()
        {
            System.IO.File.AppendAllText("C:\\temp.txt", "In OnPause." + Environment.NewLine);
            base.OnPause();
        }

        protected override void OnContinue()
        {
            System.IO.File.AppendAllText("C:\\temp.txt", "In OnContinue." + Environment.NewLine);
            base.OnContinue();
        }
    }
}
"@;

Try
{
    [WindowsService.WindowsService]::Run([WindowsService.WindowsService]::GetWindowsService())
}
Catch
{
    $ErrorMessage = $_.Exception.Message
    $FailedItem = $_.Exception.ItemName
    [System.IO.File]::AppendAllText("C:\\temp.txt", $_.Exception.ToString())
    
}

