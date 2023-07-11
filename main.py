""""this code login into amazon account and fetch information from wishlist and send sms to share
 information about product name and price """

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from twilio.rest import Client

# defining constants
CHROME_DRIVER_PATH = YOUR DRIVER PATH
MOBILE_NO = YOUR MOBILE NUMBER
PASSWORD = YOUR PASSWORD

# using twilio to send sms about product details
VIRTUAL_TWILIO_NUMBER = ""
VERIFIED_NUMBER = ""  # your registered number in twilio
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

service = Service(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.get("https://www.amazon.in/")


class Products:

    def __init__(self, path):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww"
                        ".amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2"
                        ".0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid"
                        ".claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid"
                        ".ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        time.sleep(5)

        # sign-in using mobile number
        username = self.driver.find_element(By.XPATH, '//*[@id="ap_email"]')
        username.send_keys(MOBILE_NO)
        time.sleep(2)
        username.send_keys(Keys.ENTER)

        # entering password
        password = self.driver.find_element(By.XPATH, '//*[@id="ap_password"]')
        password.send_keys(PASSWORD)
        time.sleep(2)
        password.send_keys(Keys.ENTER)

    def find_wishlist_price(self):
        time.sleep(5)
        self.driver.get("https://www.amazon.in/hz/wishlist/ls?requiresSignIn=1&ref_=nav_AccountFlyout_wl")

        time.sleep(2)
        # fetching product Information
        name_of_product = self.driver.find_elements(By.CSS_SELECTOR, '.a-size-small h2')
        price_of_product = self.driver.find_elements(By.CLASS_NAME, 'a-price')
        # creating dictionary of product details
        product_details = {}
        for n in range(len(name_of_product)):
            product_details[n] = {
                "name": name_of_product[n].text,
                "price": price_of_product[n].text,
            }
        # converting dictionary into string
        dict_string = ', '.join([f'{key}: {value}' for key, value in product_details.items()])
        # storing product details into csv file
        new_file = pd.DataFrame(product_details)
        new_file.to_csv("wishlist")
        time.sleep(2)
        # defining sms details
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=dict_string,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
        print(message.body) # sending sms about product details in wishlist



# calling functions
bot = Products(CHROME_DRIVER_PATH)
bot.login()
bot.find_wishlist_price()
