# NSAllowsArbitraryLoads exception test in Info.plist files
### Introduction
Advanced transport security(ATS) is a set of requirements set by Apple(the software company, not fruit) for TLS configuration of servers used by iOS apps  
They also added a way to add exceptions in apps Info.plist files so that connections to servers that are not ATS compliant work normally  
One of the exceptions was to disable this ATS check for all outbound connections. As one might expect, a lot of people added this exception for the apps they developed  
At WWDC 2016 Apple announced that they are going to start enforcing ATS checks at the App store and all apps using this exception will have to provide a reasonable explanation for having this exception  
This tool will help you quickly identify Info.plist files where this exception is set

### Usage
python plist_check.py -d directory_to_start_scan  

Directory to start scan is the path where the script should start looking for Info.plist files. It will find all Info.plist files in that path and stores the result(pass/fail) in a json file for each file found. It will also print out all the files that didn't pass. You can then look at those projects and update them accordingly  
As app bundles are directories, the best way to use this is to put all your iOS app bundles in one directory and point the tool at that directory

### Useful links
ATS requirements doc: https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html#//apple_ref/doc/uid/TP40009251-SW35  
What's new in security talk at WWDC 2016: https://developer.apple.com/videos/play/wwdc2016/706/ first part of the talk is dedicated to ATS  
NSAppTransportSecurity Cocoa key - https://developer.apple.com/library/ios/documentation/General/Reference/InfoPlistKeyReference/Articles/CocoaKeys.html#//apple_ref/doc/uid/TP40009251-SW33