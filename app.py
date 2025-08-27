from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import streamlit as st
import logging
from datetime import datetime
import os
import platform
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open("date_log.txt", "r") as file:
    dates = file.readlines()
    dates = [line.strip() for line in dates]

if "run" not in st.session_state:
    st.session_state.run = 1
else:
    st.session_state.run += 1

logger.info(f"Run {st.session_state.run}")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# Display and collect multiselect for days
days_selected = [day.lower() for day in st.multiselect("Select days:", options=days)]

day1 = input("Please input day1 required: ").lower()
day2 = input("Please input day2 required: ").lower()

days_selected = [day1, day2]


def get_linux_driver():
    # Detect paths
    driver_path = subprocess.run(['which', 'chromedriver'], capture_output=True, text=True).stdout.strip()
    browser_path = subprocess.run(['which', 'chromium'], capture_output=True, text=True).stdout.strip()

    if not driver_path or not browser_path:
        st.error("❌ Could not find chromedriver or chromium in PATH.")
        return None

    # Set up options
    chrome_options = Options()
    chrome_options.binary_location = browser_path
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36")

    # Optional: ensure /tmp is writable
    if not os.access("/tmp", os.W_OK):
        st.warning("⚠️ /tmp is not writable. Chromium may fail to launch.")

    # Launch driver
    try:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        st.error("🚨 Failed to launch Chromium")
        st.exception(e)
        return None
    

def get_driver_for_os():
    system = platform.system().lower()
    if system == 'windows':
    # Local Windows setup
        driver_path = os.path.join(os.path.dirname(__file__), "chromedriver-win64", "chromedriver.exe")
        service = Service(driver_path)
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(service=service, options=chrome_options)
    elif system == 'linux':
    # Streamlit Cloud or local Linux
        return get_linux_driver()
    else:
        raise Exception(f"Unsupported OS: {system}")
    

if (len(days_selected) == 2 
    and datetime.today().weekday() == 2 # Wednesday
    and datetime.today().strftime("%Y-%m-%d") not in dates): # not yet run today (and thus this week)

    logger.info(f"\n\nCriteria met: {datetime.now()}\n\n")

    driver = get_driver_for_os()
    driver.get("https://momschef.co.za/")

    for day in days_selected:

        day_anchor = driver.find_element(By.XPATH, f'//a[@href="https://momschef.co.za/product/{day}-adult/"]')
        day_anchor.click()

        std_button = [item for item in driver.find_elements(By.CLASS_NAME, "variable-item-span-button") if item.text == "Adult, Standard"][0]
        std_button.click()

        qty_input = driver.find_element(By.NAME, "quantity")
        qty_input.clear()
        qty_input.send_keys(3)

        sleep(3) # otherwise it asks me to select a product (done with std_button right above)

        add_cart_btn = driver.find_element(By.CLASS_NAME, "single_add_to_cart_button")
        add_cart_btn.click()

        driver.get("https://momschef.co.za/") # back to home page

    driver.get("https://momschef.co.za/checkout")

    first_name_input = driver.find_element(By.ID, "billing_first_name")
    first_name_input.send_keys("Paul")

    last_name_input = driver.find_element(By.ID, "billing_last_name")
    last_name_input.send_keys("Claassen")

    phone_input = driver.find_element(By.ID, "billing_phone")
    phone_input.send_keys("0795052593")

    email_input = driver.find_element(By.ID, "billing_email")
    email_input.send_keys("linda.claassen.89@gmail.com")

    suburb_dropdown = driver.find_element(By.CLASS_NAME, "select2-selection__arrow")
    suburb_dropdown.click()
    suburb_dropdown = driver.find_element(By.XPATH, "//*[contains(@id, 'Brooklyn')]")
    suburb_dropdown.click()

    address_input_1 = driver.find_element(By.ID, "billing_address_1")
    address_input_1.send_keys("340 Mackenzie Street")

    postcode_input = driver.find_element(By.ID, "billing_postcode")
    postcode_input.send_keys("0181")

    total_bdi = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="order_review"]/table/tfoot/tr[4]/td/strong/span/bdi')))
    if total_bdi.text == "R438,00":
        place_order_btn = driver.find_element(By.ID, "place_order")
        # place_order_btn.click()

        with open("date_log.txt", "a") as file:
            file.write(f"{datetime.today()}\n")

else:
    logger.info(f"\n\nCriteria not met: {datetime.now()}\n\n")
