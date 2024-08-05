# webcapturetool [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/wyattshanahan/webcapturetool/graphs/commit-activity)
A tool built to capture screenshots of a large number of sites from a csv document.
This program is optimised for use on Windows 11 systems.

# Dependencies
This program requires the following dependencies:
- [Geckodriver 0.34.0](https://github.com/mozilla/geckodriver/releases/tag/v0.34.0)
- [Selenium](https://github.com/SeleniumHQ/selenium)

# How to Use This Program
This program automates capturing screenshots of websites. It utilises GeckoDriver and Selenium to automate this process.

To install Selenium, you can use ``pip install -U selenium``.

Geckodriver should be downloaded from the Geckodriver github repository (found above) and the executable placed in the same directory as the python script.

This program requires a CSV document containing the URLs of all sites to be screenshotted. If the csv document is in a different directory, give the entire file path to the document.
It will save screenshots in the same directory as the script, using the URLs as the file names. See final.csv included in the repository for an example implementation.

The program will take 1 argument, which is the name and path of the csv document in the form:
``python driver.py <name.csv>``

Any unreachable sites will be recorded in a text document named unreachable_sites.txt.

# Update Notes for dev2024.07
This update adds the following features:
- Encapsulated helper functions
- Automated Unit Testing (via pytest) for helper functions
- Automatically seperated screenshots
- Improved error handling and various bug fixes

# Upcoming Features

Want to see upcoming features? Take a look at the dev branch to see work-in-progress developments. 

Some features currently being worked on include:
- Encapsulation of core functionality
- Automated unit testing to ensure stability and security
- Automated CI pipeline to perform unit testing
- Improved documentation

# driver2024_04

``driver2024_04.py`` is a classic version of the application. This was implemented prior to the encapsulation project, and is available for users needing to use the classic version. 
