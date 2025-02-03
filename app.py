
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from datetime import datetime

# Function to get the Chrome user profile path dynamically
def get_chrome_profile_path():
    profile_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default")
    return profile_path

# Function to initialize the Chrome WebDriver with the user profile
def initialize_driver():
    chromedriver_path = r"chromedriver.exe"  # Replace with your actual ChromeDriver path
    profile_path = get_chrome_profile_path()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={profile_path}")

    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    return driver

# Function to send a WhatsApp message
def send_whatsapp_message(driver, phone_number, message):
    try:
        driver.get("https://web.whatsapp.com")
        wait = WebDriverWait(driver, 60)

        # Check if already logged in
        print("Checking login status...")
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))
            print("Already logged in!")
        except TimeoutException:
            print("Not logged in. Waiting for QR code to be scanned...")
            wait.until(EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label='Scan me!']")))
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']")))
            print("Logged in successfully!")

        # Search for the phone number
        print("Searching for the contact...")
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@role='textbox']")))
        search_box.clear()
        search_box.send_keys(phone_number)
        search_box.send_keys(Keys.ENTER)

        # Wait for the chat to load and send the message
        print("Opening chat...")
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")))
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        print(f"Message sent to {phone_number} successfully!")
    except TimeoutException as e:
        print(f"Timed out waiting for elements: {e}. Check your internet connection or QR code scanning.")
    except NoSuchElementException as e:
        print(f"Could not find the required elements on the page: {e}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to wait until the scheduled time
def wait_until(target_time):
    while datetime.now() < target_time:
        time.sleep(1)

# Main function
if __name__ == "__main__":
    phone_number = input("Enter the phone number : ")
    message = input("Enter the message: ")
    scheduled_time_str = input("Enter the scheduled time : ")

    try:
        scheduled_time = datetime.strptime(scheduled_time_str, "%Y-%m-%d %H:%M:%S")
        if scheduled_time <= datetime.now():
            print("Scheduled time must be in the future.")
        else:
            print(f"Message scheduled for {scheduled_time}. Waiting...")
            wait_until(scheduled_time)

            driver = initialize_driver()
            send_whatsapp_message(driver, phone_number, message)

            time.sleep(15)
            driver.quit()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
