from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import utilities as utils

url = "https://mops.twse.com.tw/mops/web/t05sr01_1"
driver = webdriver.Chrome()
config = utils.read_config()
company_code = config.get('company_code')
company_name = config.get('company_name')
key_word = config.get('key_word')
publish_date = config.get('publish_date')
publish_time = config.get('publish_time')
config_element_list = [company_code, company_name, key_word, publish_date, publish_time]


def driver_click(locator):
    """Click element.
    :param locator: Locator of element.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).click()


def get_company_news():
    driver.get(url)
    rows = driver.find_elements(By.CSS_SELECTOR, ".odd, .even")

    try:
        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            matched_elements = []

            for element in config_element_list:
                if element == "default":
                    matched_elements.append(True)
                else:
                    # Check if the element matches any cell's text value
                    found = False
                    for cell in cells:
                        if element == cell.text:
                            found = True
                            break
                    matched_elements.append(found)

            # If all elements in config_element_list are matched, print the row's data
            if all(matched_elements):
                for cell in cells:
                    print(cell.text, end="\t")
                print()
    except IndexError:
        print("System error, please check if the data is correct.")
        time.sleep(10)
    finally:
        # Close the webdriver after processing
        print("Initial result has been printed, Now getting detailed information...")
        driver.quit()


def get_detail_info():
    """Get detail information of the search result."""


if __name__ == '__main__':
    get_company_news()
