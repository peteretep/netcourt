import logging
import time

import schedule
from decouple import config
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

FORMAT = "%(asctime)-15s %(message)s"
logging.basicConfig(filename="netcourt.log", format=FORMAT, level=logging.DEBUG)

logging.info("Starting Netcourt program")
USERNAME = config("USERNAME")
PASSWORD = config("PASSWORD")


def netcourt():

    driver = webdriver.Firefox()
    driver.implicitly_wait(10)  # seconds
    driver.get("https://members.glasgowclub.org/connect/")

    assert "Online Booking" in driver.title

    username = driver.find_element_by_id("ctl00_MainContent_InputLogin")
    username.send_keys(USERNAME)
    password = driver.find_element_by_id("ctl00_MainContent_InputPassword")
    password.send_keys(PASSWORD)

    driver.find_element_by_id("ctl00_MainContent_btnLogin").click()

    driver.find_element_by_link_text("Queens Park Tennis").click()

    table = driver.find_element_by_id("slotsGrid")
    available_slots = []
    try:
        logging.info("Trying 7pm")
        seven = table.find_element_by_xpath("tbody/tr[12]")
        available_slots = seven.find_elements_by_class_name("itemnotavailable")
        available_slots[0].click()
        driver.find_element_by_link_text("19:00").click()
        driver.find_element_by_id("ctl00_MainContent_btnBasket").click()
        driver.close()
        return
    except (NoSuchElementException, IndexError) as e:
        logging.warning("No courts available at 19:00")
        logging.warning(f"{e}")
    try:
        logging.info("Trying 8pm")
        eight = table.find_element_by_xpath("tbody/tr[13]")
        available_slots = eight.find_elements_by_class_name("itemavailable")
        available_slots[0].click()
        driver.find_element_by_link_text("20:00").click()
        driver.find_element_by_id("ctl00_MainContent_btnBasket").click()
        driver.close()
        return
    except (NoSuchElementException, IndexError) as e:
        logging.warning("No courts available at 20:00")
        logging.warning(f"{e}")
    try:
        logging.info("Trying 6pm")
        six = table.find_element_by_xpath("tbody/tr[11]")
        available_slots = six.find_elements_by_class_name("itemavailable")
        available_slots[0].click()
        driver.find_element_by_link_text("18:00").click()
        driver.find_element_by_id("ctl00_MainContent_btnBasket").click()
        driver.close()
        return
    except (NoSuchElementException, IndexError) as e:
        logging.warning("No courts available at 18:00")
        logging.warning(f"{e}")

    driver.close()


schedule.every().day.at("00:01").do(netcourt)

while True:
    schedule.run_pending()
    time.sleep(1)
