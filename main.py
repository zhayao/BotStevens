# © 2021 Zhangchi Yao <yaozc@umich.edu>
from playwright.sync_api import sync_playwright
import random
import time

def reserve_for_passHolder(playwright):
    userName = input("Enter your login email: ")
    passWord = input("Enter your login password: ")
    passHolderName = input("Enter pass Holder's Name: ")
    date = input("Enter your target booking date (current mo only): ")
    phoneNumber = input("Enter your phone #: ")
    
    browser = playwright.chromium.launch()
    print("Launching Chromium..")
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.stevenspass.com/account/login-page.aspx?url=%2fplan-your-trip%2flift-access%2freservations.aspx%3freservation%3dtrue")
    page.fill("form[id=\"returningCustomerForm_3\"] input[name=\"UserName\"]", userName)
    page.fill("form[id=\"returningCustomerForm_3\"] input[name=\"Password\"]", passWord)
    print("Login now")
    with page.expect_navigation():
        page.press("form[id=\"returningCustomerForm_3\"] input[name=\"Password\"]", "Enter")

    page.goto("https://www.stevenspass.com/plan-your-trip/lift-access/reservations.aspx")

    page.click("button[id=\"passHolderReservationsSearchButton\"]")

    time.sleep(5)
    targetDate = "text=\"{}\"".format(date)
    tried = 0
    # Check if target date is available
    while(page.is_disabled(targetDate)):
        page.goto("https://www.stevenspass.com/plan-your-trip/lift-access/reservations.aspx")
        tried += 1
        waitingTime = random.randrange(60, 240)
        print("Attempt# ", tried, " will try after ", waitingTime, " sec")
        time.sleep(waitingTime)
        page.click("button[id=\"passHolderReservationsSearchButton\"]")
        # wait_for_selector can be a better choice but selector having
        # troubles to wait correctly until calander finish loading
        # page.wait_for_selector("text=passholder_reservations__calendar__day")
        time.sleep(6)

    page.click(targetDate)

    assignTo = "text=\"{}\"".format(passHolderName)
    page.click(assignTo)

    page.click("//button[normalize-space(.)='Assign Pass Holders']")

    page.fill("input[name=\"phone\"]", phoneNumber)
    page.click("text=/.*I have reviewed and saved or p.*/")
    page.click("text=\"Complete Reservation\"")

    page.close()
    context.close()
    browser.close()

with sync_playwright() as playwright:
    reserve_for_passHolder(playwright)

