from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import time
import pyotp
import json
import requests
import base64
import os
import datetime

def load_settings_values():
    print("loading settings..")
    with open("./credentials.json", "r") as credentialsFile:
        credentialsData = json.load(credentialsFile)
        netID = credentialsData["netID"]
        password = credentialsData["password"]
        deviceURL = credentialsData["deviceURL"]

    return [netID, password, deviceURL]

# Getting the secret from the confirmation URL (credit to Bye DUO and No DUO Lockout for this)
def generate_secret(deviceURL):
    """Returns an unencoded secret from DUO after activating device"""
    deviceURL = deviceURL.lstrip("https://").split("/")
    domain = deviceURL[0][1:]
    key = deviceURL[-1]
    DUO = f"https://api{domain}/push/v2/activation/{key}?customer_protocol=1"
    try:
        req = json.loads(requests.post(DUO).text)
        hotpSecret = req['response']['hotp_secret']            
        print("Successfully activated device and generated secret!")
        return hotpSecret
    except:
        #print(netID, password, counter, hotpSecret, generateSecret, deviceURL, DUO)
        print("Connection error. Maybe the device is already activated?")
        exit(1)

def initialization():
    # initialization 
    if not needSecret:
        print("Initialized")
        return;
    else:
        hotpSecret = generate_secret(deviceURL)
        credentialsData["hotpSecret"] = hotpSecret
        credentialsData["needSecret"] = False
        with open("credentials.json", "w") as credentialsFile:
            credentialsJson = json.dumps(credentialsData, indent = 4)
            credentialsFile.write(credentialsJson)
        print("Secret generated and put into credentials.json file. The program should work now! Exit and restart the program to run it")
        time.sleep(5)
        os._exit(0)
        
def automation():
    if not needSecret:
        hotpSecretEncode = base64.b32encode(hotpSecret.encode('ascii')).decode('utf-8')
        hotp = pyotp.HOTP(hotpSecretEncode)
        code = hotp.at(counter)
        print("Code generated")

        option = webdriver.ChromeOptions()
        option.add_argument("--headless")

        path1 = apath + "/chromedriver"
        path2 = apath + "/credentials.json"
        driver = webdriver.Chrome(path1, options=option)
        wait = WebDriverWait(driver, 10)
        
        # Link to NYU Daily Screener
        driver.get("https://nyu.qualtrics.com/jfe/form/SV_ePNv0eXvGWgCxkq?")
        assert "NYU COVID-19" in driver.title

        # Clicks on Next
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "NextButton"))).click()
        # Selecting yes to 'Do you have a NetID option'
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "QID2-1-label"))).click()
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "NextButton"))).click()
        print("Clicked the next button")

        # Find and fill username/password
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "username")))
        driver.find_element_by_id("username").send_keys(netID)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "password")))
        driver.find_element_by_id("password").send_keys(password)
        wait.until(expected_conditions.element_to_be_clickable((By.NAME, "_eventId_proceed"))).click()
        print("Filled out the username/password, moving on to the next part")


        # Switch to iFrame for DUO authentication
        time.sleep(1)
        #driver.get_screenshot_as_png()
        wait.until(expected_conditions.frame_to_be_available_and_switch_to_it((By.ID, "duo_iframe")))
        #Switched iframes
        time.sleep(1) #temporary, remove later

        # Use HOTP passcode to authenticate
        driver.find_element_by_id("passcode").click()
        driver.find_element_by_class_name("passcode-input").send_keys(code)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "passcode"))).click()
        print("Got to the end")

        # Increment password counter
        with open(path2, "w") as credentialsFile:
            credentialsData["counter"] += 1
            credentialsData["last"] = this
            credentialsJson = json.dumps(credentialsData, indent = 4)
            credentialsFile.write(credentialsJson)


apath = os.getcwd()
path2 = apath + "/credentials.json"

with open(path2, "r") as credentialsFile:
    credentialsData = json.load(credentialsFile)

    netID = credentialsData["netID"]
    password = credentialsData["password"]
    deviceURL = credentialsData["deviceURL"]
    counter = credentialsData["counter"]
    hotpSecret = credentialsData["hotpSecret"]
    needSecret = credentialsData["needSecret"]
    last = credentialsData["last"]

initialization()

today = datetime.date.today()
this = today.day

if (this == last):
    print("already done: " + str(this))
else:
    automation()
    time.sleep(10); #get the next part to load
    print("Finished waiting 10 seconds for it to load the confirmation page")