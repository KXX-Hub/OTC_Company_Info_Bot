import os
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import utilities as utils


detail_info = []  # 定義為全域變數
url = "https://mops.twse.com.tw/mops/web/t05sr01_1"
driver = webdriver.Chrome()
config = utils.read_config()
config_element_list = [config.get('company_code'), config.get('company_name'),
                       config.get('publish_date'), config.get('publish_time'),
                       ]



def driver_click(locator):
    """Click the element.
    :param locator: The locator of the element.
    """
    WebDriverWait(driver, 10).until(ec.presence_of_element_located(locator)).click()


def search_results_by_config(rows, element_list):
    all_results = []
    element_set = set(element_list)
    for row in rows[0:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        row_text = [cell.text for cell in cells]
        detail_info.append(cells[5].id)
        if "default" in element_set or element_set.intersection(row_text):
            row_data = [cell.text for cell in cells]
            all_results.append(row_data)
    return all_results


def get_initialize_search_result():
    """
    Get initialize search result.
    :return: The filtered search results.
    """
    driver.get(url)
    driver.maximize_window()
    try:
        driver_click((By.XPATH, '//*[@id="details-button"]'))
        driver_click((By.XPATH, '//*[@id="proceed-link"]'))
    except:
        pass
    rows = driver.find_elements(By.CSS_SELECTOR, ".odd, .even")
    desktop_path = utils.get_os_specific_path('')
    try:
        print("| Start getting initialize search result |\n")
        if all(element == "default" for element in config_element_list):
            print("\n- Searching all results...\n")
        else:
            non_default_elements = [element for element in config_element_list if element != "default"]
            print("- Searching result for following elements:", non_default_elements)
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
        utils.save_results_to_csv(all_results, folder_path)

    except IndexError:
        print("=" * 110 + "\n")
        print("System error, please check if the data is correct")
        time.sleep(10)
    finally:
        print("Initial result has been printed, Now getting detailed information\n")


def get_detail_info_page_table(path):
    """Get the detail information of the company.
    :param path: The XPath to the input element.
    :return: None
    """
    driver.get(url)
    driver_click((By.XPATH, path))
    # print("--------------------------------------------------------")
    time.sleep(10000)


def get_detail_info():
    """Get detail information Page
    :return: None
    """
    driver.get(url)
    try:
        driver_click((By.XPATH, '//*[@id="details-button"]'))
        driver_click((By.XPATH, '//*[@id="proceed-link"]'))
    except:
        pass
    print("| Start getting detail information |\n")

    detail_info_path = '//*[@id="table01"]/form[2]/table/tbody/tr[2]/td[6]/input'
    get_detail_info_page_table(detail_info_path)


if __name__ == '__main__':
    get_initialize_search_result()
    get_detail_info()
