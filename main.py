import os
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import utilities as utils

url = "https://mops.twse.com.tw/mops/web/t05sr01_1"
driver = webdriver.Chrome()
config = utils.read_config()
config_element_list = [config.get('company_code'), config.get('company_name'), config.get('key_word'),
                       config.get('publish_date'), config.get('publish_time'), ]


def driver_click(locator):
    """Click element.
    :param locator: Locator of element.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).click()


def search_results_by_config(rows, element_list):
    """
    Process search results and return the filtered data.
    :param rows: The list of rows containing search results.
    :param element_list: The list of elements to match in the search results.
    :return: The filtered search results.
    """
    all_results = []
    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        matched_elements = []
        row_data = []

        for element in element_list:
            if element == "default":
                matched_elements.append(True)
            else:
                found = False
                for cell in cells:
                    if element == cell.text:
                        found = True
                        break
                matched_elements.append(found)

        if all(matched_elements):
            for cell in cells:
                row_data.append(cell.text)
            all_results.append(row_data)

    return all_results


def getting_initialize_search_result():
    """Get initialize search result.
    :return: The filtered search results.
    """
    driver.get(url)
    driver.maximize_window()
    rows = driver.find_elements(By.CSS_SELECTOR, ".odd, .even")
    desktop_path = utils.get_os_specific_path('')
    try:
        print("| Start getting initialize search result |\n")
        all_results = search_results_by_config(rows, config_element_list)
        # Print the results to the console
        print("=" * 110 + f"\n")
        print("| Result |\n")
        for result in all_results:
            print("\t".join(result))

        # Save the results to a CSV file with date and number of records in the file name
        today_date = date.today().strftime("%Y-%m-%d")
        folder_name = os.path.join(config.get('folder_name'), today_date)
        folder_path = os.path.join(desktop_path, folder_name)
        utils.create_folder_if_not_exists(folder_path)
        utils.save_search_results_to_csv(all_results, folder_path)

    except IndexError:
        print("=" * 110 + "\n")
        print("System error, please check if the data is correct")
        time.sleep(10)
    finally:
        print("Initial result has been printed, Now getting detailed information\n")
        print("=" * 110)
        driver.quit()


def get_detail_info_page():  # TODO finish this function
    """Get detail information Page
    :return: The detail information.
    """
    all_results = []


if __name__ == '__main__':
    getting_initialize_search_result()
