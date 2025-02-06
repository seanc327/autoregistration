import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# config
chromedriver = "[chromedriver-path]" # usually /usr/local/bin/chromedriver
profilepath = "[chrome-profile-path]" # find in chrome://version/
profiledir = "Default" # or "Profile x"; match with profilepath
schedulebuilder = "[schedule-link]"
user = "[username]"
password = "[password]"
passtime = "[HH:MM:SS]" #%H:%M:%S

# setup
options = Options()
options.add_argument(f"--user-data-dir={profilepath}")
options.add_argument(f"--profile-directory={profiledir}")

# webdriver
service = Service(chromedriver)
driver = webdriver.Chrome(service=service, options=options)

# registration
try:
    driver.get(schedulebuilder)
    time.sleep(5) 

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(user)
    driver.find_element(By.ID, "password").send_keys(password, Keys.RETURN)

    register = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.register_trigger"))
    )
    print("register button found")

    # countdown until waitlist time
    def wait_until_pass_time(target_time):
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            if current_time >= target_time:
                print("registering")
                break
            else:
                print(f"current time: {current_time}, pass time: {target_time}")
                if int(current_time.split(":")[1]) % 10 == 0:
                    driver.refresh()
                    print("refresh")
                
                time.sleep(15)

    wait_until_pass_time(passtime)

    # click register
    driver.execute_script("arguments[0].click();", register)
    print("registered!")

    # waitlisting option
    try:
        waitlist = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#NoPTAWaitlistQuestion .btn-primary"))
        )
        
        # click waitlist
        driver.execute_script("arguments[0].click();", waitlist)
        print("waitlisting allowed")
    except TimeoutException:
        print("no waitlisting needed")

finally:
    time.sleep(60)
    driver.quit()