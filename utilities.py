"""This python will handle some extra functions."""
import csv
import os
import sys
from datetime import date
from os.path import exists
import platform
import yaml
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# | OTC_Company_Info_Bot                 |
# | Made by KXX                          |
# ++------------------------------------++

# |  *For Searching*  |

# Company code that you want to search for.
company_code: "default"

# Company name that you want to search for.
company_name: "default"

# The date that you want to search for.
#format: YYYY/MM/DD
publish_date: "default"

# The time that you want to search for.
#format: HH:MM:SS
publish_time: "default"

#------------------------------------

# |  *For Saving*  |

# The folder name that you want to save the file.
# default: OTC_Company_Info
folder_name: "OTC_Company_Info"
"""
                )
    sys.exit()


def read_config():
    """Read config file.
    Check if config file exists, if not, create one.
    if exists, read config file and return config with dict type.
    :rtype: dict
    """
    if not exists('./config.yml'):
        print("Config file not found, create one by default.\nPlease finish filling config.yml")
        with open('config.yml', 'w', encoding="utf8"):
            config_file_generator()

    try:
        with open('config.yml', 'r', encoding="utf8") as f:
            data = yaml.load(f, Loader=SafeLoader)
            config = {
                'company_code': data['company_code'],
                'company_name': data['company_name'],
                'publish_date': data['publish_date'],
                'publish_time': data['publish_time'],
                'folder_name': data['folder_name']
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def get_os_specific_path(file_name):
    """Get the OS specific path.
    :param file_name: The name of the file.
    :return: The OS specific path.
    """
    if platform.system() == "Windows":
        print("\n|                 Windows                |")
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', file_name)
    elif platform.system() == "Darwin":  # macOS
        print("\n|                 macOS                  |")
        return os.path.join(os.path.join(os.environ['HOME']), 'Desktop', file_name)
    else:
        raise OSError("| Unsupported operating system |")


def create_folder_if_not_exists(folder_path):
    """Create a folder if it does not exist.
    :param folder_path: The path to the folder.
    """
    config = read_config()
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("=" * 110)
        print(f"\n- There is no folder named {config.get('folder_name')} on your desktop.Creating one...")
        print(f"- Folder created: {folder_path}\n")
    else:
        print("=" * 110)
        print(f"\n- Files will be saved to: {folder_path}\n")


def output_to_csv(data, file_path):
    """Output the data to a CSV file.
    :param data: The data to be written to the CSV file.
    :param file_path: The path to the CSV file.
    """
    with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['公司代碼', '公司簡稱', '發言日期', '發言時間', '主旨'])

        # Write data rows (exclude the last row)
        for row in data:
            csv_writer.writerow(row)

    print(f"Results saved to: {file_path}\n")
    print("=" * 110 + "\n")



def save_results_to_csv(all_results, folder_path):
    """Save the search results to a CSV file.
    :param all_results: The search results.
    :param folder_path: The path to the folder where the CSV file will be saved.
    """
    config = read_config()
    config_element_list = [config.get('company_code'), config.get('company_name'),
                           config.get('publish_date'), config.get('publish_time')]

    today_date = date.today().strftime("%Y-%m-%d")
    num_records = len(all_results)

    # Check if there are configurations other than "default"
    has_non_default_config = any(element != "default" for element in config_element_list)

    if has_non_default_config:
        csv_file_name = f"{today_date}_search_results.csv"
    else:
        csv_file_name = f"{today_date}_total{num_records}_records.csv"

    csv_file_path = os.path.join(folder_path, csv_file_name)

    # Check if the file already exists with the same name
    if os.path.exists(csv_file_path):
        # Read the existing file's name and extract the date and record count from it
        existing_file_name = os.path.basename(csv_file_path)
        split_result = existing_file_name.split('_total')
        if len(split_result) == 2:
            existing_date_str, existing_records_str = split_result
            existing_records_str = existing_records_str.split('_')[0]

            # Convert the extracted date and record count to their respective types
            existing_date = date.fromisoformat(existing_date_str)
            existing_records = int(existing_records_str)

            # Compare the existing date and record count with today's date and the current number of records
            if existing_date == date.today() and existing_records >= num_records:
                print("- File is already up to date\n")
                print(f"=" * 110 + f"\n")
                return

    # Save the new search results to a new file or overwrite the existing file
    output_to_csv(all_results, csv_file_path)
