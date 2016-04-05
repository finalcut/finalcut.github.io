---
layout: post
title: "Deploying Azure Worker Role via Team City"
description:
headline:
date: 2016-04-05 08:48:18 -0400
category: continuous-integration
tags: [azure,teamcity,ci]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
Setting up Team City for deployment of an Azure Website was sort of complicated but, overall, not too bad.  The built in build steps all worked together pretty nicely and I didn't have to provide any external scripts or utilities to help with the process.  Deployment of an Azure Worker Role is not quite the same.

I owe big thanks to Scott Kirkland whose post, [CI Deployment Of Azure Web Roles Using TeamCity](http://weblogs.asp.net/srkirkland/ci-deployment-of-azure-web-roles-using-teamcity) was the basis for my own understanding.

This post assumes you already have an Azure "Worker Role" project created and you are ready to deploy it to the cloud.  In fact, it assumes you've already published it from within Visual Studio at some point.  I am using Visual Studio 2012 and I can't comment on how to do that step in more modern versions of Visual Studio so I am going to skip it.

The biggest change between my post and Scott Kirkland's is the fact that the Azure PowerShell Script had to be updated to support the way the commandlets are installed now (4 years after Scott's post).

## Team City Server Prerequisites
1. [Azure SDK](https://azure.microsoft.com/en-us/develop/net/) - Just go, log in, download and install the SDK you need.
2. [Azure Powershell](https://azure.microsoft.com/en-us/documentation/articles/powershell-install-configure/) - This page has a few different ways to install Azure PowerShell.  I used the first one called "WebPI". I don't use PowerShell much and I was unable to get the second option (the PowerShell Gallery) to work on my Team City server.  **After installing I did have to reboot.**
3. Your Azure *publishsettings* file.  The easiest way to do this is to open your Azure PowerShell and then execute the command `Get-AzurePublishSettingsFile`.  This will open your default browser and require you to login.  Once you've logged in the file will download automatically.  I suggest you move it to somewhere handy like `C:\TeamCity` and rename it to something like `azure.publishsettings`.  The default name is fairly opaque.

Once you have completed that you need to set up your TeamCity Project.

## Team City Project Setup
I have three build steps in my project; NuGet Install, MSBuild, and PowerShell.

### Nuget Install

![nuget install settings](/images/deploy-worker-role-to-azure/nuget.png)


### MSBuild

![msbuild publish](/images/deploy-worker-role-to-azure/msbuild.png)


You'll want to run your Team City build once before you add the PowerShell steps.  Just make sure MSBuild works okay and to make sure everything is kosher.  At this point I had to modify the two files created by the build; `ServiceConfiguration.Cloud.csfg` and `ServiceConfiguration.Local.Csfg` by adding a node called `ConfigurationSettings` and another called `Certificates`. Both of these nodes I was able to copy from the files in my Visual Studio project.  I intentionally don't commit either of those files to version control (Git) because they contain some secrets in them.  Your `ConfigurationSettings` should have at least five settings under it:

1. Microsoft.WindowsAzure.Plugins.RemoteAccess.Enabled
2. Microsoft.WindowsAzure.Plugins.RemoteAccess.AccountUsername
3. Microsoft.WindowsAzure.Plugins.RemoteAccess.AccountEncryptedPassword
4. Microsoft.WindowsAzure.Plugins.RemoteAccess.AccountExpiration
5. Microsoft.WindowsAzure.Plugins.RemoteForwarder.Enabled

Plus you'll have at least one `Certificate`

1. Microsoft.WindowsAzure.Plugins.RemoteAccess.PasswordEncryption

My project would not build on TeamCity without those values.

At this point, it should be obvious, that you want to keep your TeamCity server secure. You've already downloaded your publishsettings file (which contains sensitive data) and you've put sensitive data in these csfg files.  I don't know if there is a better way to do this! If there is please leave a comment.


### PowerShell
Finally, we need to define the PowerShell step; this part uses the commandlets you installed before via PowerShell script that will either create the new deployment if you've never deployed before OR will update the existing deployment.  This script is almost entirely from [Scott's blog](http://weblogs.asp.net/srkirkland/ci-deployment-of-azure-web-roles-using-teamcity) with the exception of a few minor mods to get it working with the current Azure SDK and commandlets.

![msbuild publish](/images/deploy-worker-role-to-azure/powershell.png)

In the `Script Source` field you'll need to put your version of the following PowerShell script. You just have to update the first seven values to match your settings.  Then confirm the paths for the `Import-Module` commands.  Here is the script (or a [gist](https://gist.github.com/finalcut/db002990a0b083f4fa42d5a353250c5c) if you prefer).  I identified my changes to his script with the `::CHANGE::` prefix to a couple comments.  You'll see not much has changed.

```posh
#Modified and simplified version of https://www.windowsazure.com/en-us/develop/net/common-tasks/continuous-delivery/
$subscription = "MY SUBSCRIPTION"  #not your subscription ID but the actual name of the subscription.
$service = "MY SERVICE"
$slot = "staging" #staging or production
$projectName = "PROJECT IN SOLUTION WITH THE WORKER ROLE DEFINED"
$buildConfigName = "release"  #debug or release...
$storageAccountName = "MY AZURE STORAGE ACCOUNT NAME"
$pathToPublishSettingsFile = "c:\TeamCity\azure.publishsettings"
$deploymentLabel = "ContinuousDeploy to $service v%build.number%"


$package = "$($projectName)\bin\$($buildConfigName)\app.publish\$($projectName).cspkg"
$configuration =  "$($projectName)\bin\$($buildConfigName)\app.publish\ServiceConfiguration.Cloud.cscfg"
$timeStampFormat = "g"

Write-Output "Running Azure Imports"
# ::CHANGE:: I had to update these as the stuff at Scotts blog was outdated
Import-Module "C:\Program Files (x86)\Microsoft SDKs\Azure\PowerShell\ResourceManager\AzureResourceManager\AzureRM.Profile\AzureRM.Profile.psd1"
Import-Module "C:\Program Files (x86)\Microsoft SDKs\Azure\PowerShell\Storage\Azure.Storage\Azure.Storage.psd1"
Import-Module "C:\Program Files (x86)\Microsoft SDKs\Azure\PowerShell\ServiceManagement\Azure\Azure.psd1"

# ::CHANGE:: I added variable for pathToPublishSettingsFile
Import-AzurePublishSettingsFile $(pathToPublishSettingsFile)
# ::CHANGE:: I had to add the $storageAccount name instead of using the $service here
Set-AzureSubscription -CurrentStorageAccount $storageAccountName -SubscriptionName $subscription

function Publish(){
 $deployment = Get-AzureDeployment -ServiceName $service -Slot $slot -ErrorVariable a -ErrorAction silentlycontinue
 Write-Output $deployment

 if ($a[0] -ne $null) {
    Write-Output "$(Get-Date -f $timeStampFormat) - No deployment is detected. Creating a new deployment. "
 }

 if ($deployment.Name -ne $null) {
    #Update deployment inplace (usually faster, cheaper, won't destroy VIP)
    Write-Output "$(Get-Date -f $timeStampFormat) - Deployment exists in $servicename.  Upgrading deployment."
    UpgradeDeployment
 } else {
    CreateNewDeployment
 }
}

function CreateNewDeployment()
{
    write-progress -id 3 -activity "Creating New Deployment" -Status "In progress"
    Write-Output "$(Get-Date -f $timeStampFormat) - Creating New Deployment: In progress"

    $opstat = New-AzureDeployment -Slot $slot -Package $package -Configuration $configuration -label $deploymentLabel -ServiceName $service

    $completeDeployment = Get-AzureDeployment -ServiceName $service -Slot $slot
    $completeDeploymentID = $completeDeployment.deploymentid

    write-progress -id 3 -activity "Creating New Deployment" -completed -Status "Complete"
    Write-Output "$(Get-Date -f $timeStampFormat) - Creating New Deployment: Complete, Deployment ID: $completeDeploymentID"
}

function UpgradeDeployment()
{
    write-progress -id 3 -activity "Upgrading Deployment" -Status "In progress"
    Write-Output "$(Get-Date -f $timeStampFormat) - Upgrading Deployment: In progress"

    # perform Update-Deployment
    $setdeployment = Set-AzureDeployment -Upgrade -Slot $slot -Package $package -Configuration $configuration -label $deploymentLabel -ServiceName $service -Force

    $completeDeployment = Get-AzureDeployment -ServiceName $service -Slot $slot
    $completeDeploymentID = $completeDeployment.deploymentid

    write-progress -id 3 -activity "Upgrading Deployment" -completed -Status "Complete"
    Write-Output "$(Get-Date -f $timeStampFormat) - Upgrading Deployment: Complete, Deployment ID: $completeDeploymentID"
}

Write-Output "Create Azure Deployment"
Publish
```

At this point you should be able to run your build on TeamCity and see that your worker role has been deployed properly.  You can always tell by viewing the build log on TeamCity and by going to your Cloud Service "Dashboard" on the Azure Management Portal and looking in the right column for "Deployment Label"  It should say something like `ContinuousDeploy to MyService v39` which is the value defined in the above script as `$deploymentLabel`.
