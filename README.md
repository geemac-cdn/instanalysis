# instanalysis
aka "Instagram Analysis"
<br>
A Python-based data extraction suite for Instagram profiles.  Use this tool to gather information on Instagram profiles, likes on posts and follower/following lists.  Outputs to JSON files for analysis using Pandas, Spark, etc.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites
A Windows-based system<br>
Windows 10 recommended<br>
If you are using a Linux desktop, use these instructions to setup a vitual machine running Windows 10
```
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
ChromeDriver - WebDriver for Chrome<br>
Important: ensure the version you download matches your version of chrome (for example, If you are using Chrome version 81, please download ChromeDriver 81.0.4044.69)<br>
This project was developed using the chromedriver_win32.zip package
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
Install Anaconda<br>
From the start menu, open the Anaconda command prompt.  Type the following to install Selenium webdriver for Python (this will install to the base environment)
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
  <li><b>txt_dir_output</b> - This is where the JSON files will be output.  Either change this value to match an existing sub-folder or create a sub-folder to match the default value</li>
  <li><b>user_login</b> - Uncomment this line and fill it with your Instagram login name</li>
  <li><b>user_password</b> - Uncomment this line and fill it with your Instagram password</li>
  <li><b>tgt_user</b> - This is the Instagram user that you will extract information from.  Replace the default name (now defunct) with an account you wish to extract.  If you need a sample account, try "worldofbenches".  Remember that you must use the account name (e.g."johnsmith12345") instead of the account's full name (e.g. "John Smith").</li>
  <li><b>num_posts</b> - If you change the default, ensure it is an integer value greater than or equal to 1</li>
</ul>
In the second cell, uncomment the first line and comment the second line (this will force the program to use the login name and password you supply, rather than defaulting to the config.ini file)
Run the entire notebook.  You should see the following - <br>
<ol>
  <li>A Chrome window opens on the login screen and automatically logs in using the credentials you provided</li>
  <li>Browser navigates to the profile page of the account you selected</li>
  <li>Pop up windows open for both users followed and users following.  In both cases, the pop up window periodically scrolls until it reaches the bottom then closes (this step will by far take the longest time)</li>
  <li>Profile page starts scrolling, revealing more post thumbnails</li>
  <li>The notebook completes and displays the filename for the output file</li>
</ol>
Check the output directory you defined.  A JSON file should be generated.  Open the file in a text editor and you should see JSON code describing the target account, their followers, users they are following and a list of URL's for their most recent posts.

## Built With
<ol>
  <li>Jupyter Lab</li>
  <li>Visual Studio Code</li>
  <li>Selenium</li>
</ol>

## To Do List
<ol>
  <li>Add notebooks to analyze JSON output (currently testing in Databricks.  Please message me if you'd like it now)</li>
  <li>Create notebook for end-to-end workflow (data extraction, analysis, output) </li>
  <li>Move JSON-generation code to utility includes</li>
  <li>Add processing for videos (currently they are skipped)</li>
</ol>


## Other Notes
See FAQ.md
