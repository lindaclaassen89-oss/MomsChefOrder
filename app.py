from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import streamlit as st
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if "run" not in st.session_state():
    st.session_state.run = 1
else:
    st.session_state.run += 1

logger.info(f"Run {st.session_state.run}")

st.title("Daily Task Checklist")

days = {
    "Monday": False,
    "Tuesday": False,
    "Wednesday": False,
    "Thursday": False,
    "Friday": False
}

# Display checkboxes
for day in days:
    days[day] = st.multiselect(day)

# Show completed tasks
days_selected = [day.lower() for day, chosen in days.items() if chosen]
if days_selected:
    logger.info("Days selected:")
    for day in days_selected:
        logger.info(f"- {day}")
else:
    logger.info("No days selected yet.")

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)

# driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://momschef.co.za/")

# day1 = input("Please input day1 required: ").lower()
# day2 = input("Please input day2 required: ").lower()

# days = [day1, day2]

# for day in days:

#     day_anchor = driver.find_element(By.XPATH, f'//a[@href="https://momschef.co.za/product/{day}-adult/"]')
#     day_anchor.click()

#     std_button = [item for item in driver.find_elements(By.CLASS_NAME, "variable-item-span-button") if item.text == "Adult, Standard"][0]
#     std_button.click()

#     qty_input = driver.find_element(By.NAME, "quantity")
#     qty_input.clear()
#     qty_input.send_keys(3)

#     sleep(3) # otherwise it asks me to select a product (done with std_button right above)

#     add_cart_btn = driver.find_element(By.CLASS_NAME, "single_add_to_cart_button")
#     add_cart_btn.click()

#     driver.get("https://momschef.co.za/") # back to home page


# driver.get("https://momschef.co.za/checkout")

# first_name_input = driver.find_element(By.ID, "billing_first_name")
# first_name_input.send_keys("Paul")

# last_name_input = driver.find_element(By.ID, "billing_last_name")
# last_name_input.send_keys("Claassen")

# phone_input = driver.find_element(By.ID, "billing_phone")
# phone_input.send_keys("0795052593")

# email_input = driver.find_element(By.ID, "billing_email")
# email_input.send_keys("linda.claassen.89@gmail.com")

# suburb_dropdown = driver.find_element(By.CLASS_NAME, "select2-selection__arrow")
# suburb_dropdown.click()
# suburb_dropdown = driver.find_element(By.XPATH, "//*[contains(@id, 'Brooklyn')]")
# suburb_dropdown.click()

# address_input_1 = driver.find_element(By.ID, "billing_address_1")
# address_input_1.send_keys("340 Mackenzie Street")

# postcode_input = driver.find_element(By.ID, "billing_postcode")
# postcode_input.send_keys("0181")

# place_order_btn = driver.find_element(By.ID, "place_order")
# # place_order_btn.click()

# driver.quit()
