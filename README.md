# instanalysis
aka "Instagram Analysis"
<br>
A Python-based data extraction suite for Instagram profiles.  Use this tool to gather information on Instagram profiles, likes on posts and follower/following lists.  Outputs to JSON files for analysis using Pandas, Spark, etc.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites
A Windows-based system
```
Windows 10 recommended.
If you are using a Linux desktop, use these instructions to setup a vitual machine running Windows 10
https://www.groovypost.com/howto/windows-10-install-virtualbox/
```
A Python 3.x development environment
(Anaconda is highly recommended and will be referenced for the rest of this document)
```
https://www.anaconda.com/
```
Google Chrome
```
https://www.google.com/chrome/
```
ChromeDriver - WebDriver for Chrome
Important: ensure the version you download matches your version of chrome (for example, If you are using Chrome version 81, please download ChromeDriver 81.0.4044.69) 
```
https://chromedriver.chromium.org/downloads
```
An active Instagram account.  If you don't have one sign up here -
```
https://www.instagram.com/accounts/emailsignup/
```
(optional) A VPN service
### Installing
Install Google Chrome 
<br>
Unzip the chromedriver_win32.zip file.  Copy the chromedriver.exe file to your windows system directory.  The following file and pathname should exist by the end of this step -
```
c:\Windows\System32\chromedriver.exe
```
Install Anaconda. From the start menu, open the Anaconda command prompt.  Type the following to install Selenium webdriver for Python (this will install to the base environment)
```
pip install -U selenium
```
Proceed to the next section to test your installation
### Testing the Installation
Clone or download this project. <br>
Open Anaconda navigator.  Launch JupyterLab. In the left panel, browse to where you downloaded the instanalysis project and open the following notebook -
```
QA_FullProfile.ipynb
```
Update the configuration in the first cell as required -
<ul>
  <li>txt_dir_output - This is where the JSON files will be output.  Either change this value to match an existing sub-folder or create a sub-folder to match the default value</li?
  <li>user_login - Uncomment this line and fill it with your Instagram login name</li>
  <li>user_password - Uncomment this line and fill it with your Instagram password</li>
  <li>tgt_user - This is the Instagram user that you will extract information from.  Keep the default value or enter an account name you wish to extract.  Remember that you must use the account name (e.g."tonyrobbins") instead of the account's full name (e.g. "Tony Robbins"). If you don't use the default, select an account with not too many followers (<500) so the demo runs reasonably fast</li>
  <li>num_posts - If you change the default, ensure it is an integer valus greater than or equal to 1</li>
</ul>
Run the entire notebook.  You should see the following
<ol>
  <li>A Chrome window opens on the login screen</li>
  <li>Automatic login using the credentials you provided</li>
  <li>Browser navigates to the profile page of the account you selected</li>
  <li>Pop up windows open for both users followed and users following.  In both cases, the pop up window periodically scrolls until it reaches the bottom then closes (this step will by far take the longest time)</li>
  <li>Profile page starts scrolling, revealing more post thumbnails</li>
  <li>The Chrome window closes</li>
</ol>
Check the output directory you defined.  A JSON file should be generated.  Open the file in a text editor and you should see JSON code describing the target account, their followers, users they are following and a list of URL's for their most recent posts.
