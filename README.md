# webcapturetool [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
A webcapture tool built to generate screenshots of a large number of sites at once.
This program is optimised for use on Windows 11 systems.

# Dependencies
This program requires the following dependencies:
- [Geckodriver 0.34.0](https://github.com/mozilla/geckodriver/releases/tag/v0.34.0)
- [Selenium](https://github.com/SeleniumHQ/selenium)

# How to Use This Program
This program automates capturing screenshots of websites. It utilises GeckoDriver and Selenium to automate this process.

To install Selenium, you can use ``pip install -U selenium``.

Geckodriver should be downloaded from the Geckodriver github repository (found above) and the executable placed in the same directory as the python script.

This program requires a CSV document containing the URLs of all sites to be screenshotted. 
It will save screenshots in the same directory as the script, using the URLs as the file names. See final.csv included in the repository for an example implementation.

Any unreachable sites will be recorded in a text document named unreachable_sites.txt.

If you desire the https:// and http:// prefixes on your screenshots, comment out the lines indicated in the code.
