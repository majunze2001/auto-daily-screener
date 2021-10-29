#Daily Screener

This is the macOS version of Auto Daily Screener. Most original code is kept and I added a test of date. Now it will only run once everyday even if you run it for multiple times.

## Requirements

- Need MacBook and Google Chrome. 

## How do I use this?
Download the app file and follow the instructions. The instructions are only slightly different from those for Windows.

### Making a new device

This script works by bypassing the NYU mfa but to do that, you'll need to create a new device. Here's how:

1. After submitting your username and password, you'll come to the NYU DUO multi-factor authentication page. Click 'Add a new device'

2. Just do your authentication with your standard device (probably your phone)

3. Now pick 'Tablet', 'Android', 'I have DUO mobile installed', and 'Email me an activation link instead'

4. Send the link to your email. Once you receive it, **don't** click it (it's okay if you accidentally do). However, the link itself is what matters. (The link format is like this: https://m---------.duosecurity.com/android/--------------------)

5. ***IMPORTANT***
Right click the app (DailyScreener)–––> "Show Package Contents" –––> Contents –––> Resources –––> Right click credentials.json –––> "Open With TextEdit" then fill in your netID, password, and the link you received. Your final credentials.json should look like this:
{
    "netID": "YournetID",
    "password": "YourPassword",
    "deviceURL": "https://m---------.duosecurity.com/android/--------------------",
    "counter": 0,
    "hotpSecret": "",
    "needSecret": true,
    "last": 0
}
Pay attention to the APOSTROPHES and DO NOT change other data
***REMEMBER to SAVE***

6. Now go all way back out and run the app once. If there is an error, go to check your credential file. You're almost there but you need to do one more thing.

7. Refresh the DUO mobile page (or just open a new window). Go to 'my settings and devices' and reauthenticate with your phone (or another device) like you did before. You should see a new Android device. For the default device option, set it to the new device you made and save. 

8. You're done! If you check your email, the confirmation message should appear soon. You can put this app on your desktop and runs it everyday.






