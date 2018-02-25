# bamboohr-google-calendar-sync
Application for syncing your personal calendar between BambooHR and Google Calendars.
BambooHR provides iCal links for your entire company and "Who's off today" calendars, but does not give you a personal calendar with your own Time Off requests out of the box. This application fills the void by populating a google calendar of your choice with your BambooHR Time Off requests

This application performs a 1-way-sync from BambooHR into any given Google Calendar. 

## Authentication
Authentication against BambooHR is done via an API Access Key

## Installation
1. Install the dependencies: `sudo pip install -r requirements.txt` (or create a virtualenv to do it in)
2. Find out you BambooHR employee ID. This can be done by logging in to BambooHR and going to "My Info". Your employee ID is at the end of the URL. eg `https://yourcompany.bamboohr.com/employees/pto/?id=12345`
3. Create a Google Application with access to your Calendar and get the secrets stored locally: TBD
4. If possible, get an Access Key for BambooHR. This is done by logging into BambooHR, selecting your avatar/initials in the top-right and selecting **API Keys**. If this is not possible (it's not available for all users) you can still login with a username and password
5. If you do not want to use your default calendar, find the Calendar ID for the calendar you want to use:
    1. Open up Google Calendars
    2. Hit the three dots next to the calendar you want to use and select "Setting and sharing"
    3. Calendar ID is listed under the "Integrate Calendar" section, eg `1234567890abcdefghijk@group.calendar.google.com`
    
## First run
When you first run the program, it will run interactively and you will be presented with some configuration options. You will also need to authenticate against Google using a browser so this first run so run this on a device with a browser installed.
Once you have run through this initial configuration, your preferences will be saved and so all further interactions can be run in a non-interactive session or cronjob. If you want to run this on a headless server, it is best to run it locally on your machine first, then just copy the config files (see below) to your server. 

Example Runthrough:
```
BambooHR Company: mycompany
Employee ID: 123456
BambooHR Access Token (leave blank to use username/password):
BambooHR username: fredbloggs@mycomany.com
Password:
Google Calendar ID: 1234567890abcdefghijk@group.calendar.google.com
Updating/Creating 15 items
Done
```

Second Runthrough:
```
Updating/Creating 15 items
Done
```

## Config files
All config files are stored under ${HOME}/.config/bamboohr

## Notes
In order to not hammer the BambooHR APIs, I suggest not running this too often. Once a week/day should be enough for most people.