"""This python will handle some extra functions."""
import sys
from os.path import exists

import yaml
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# | OTC_Company_Info_Bot                 |
# | Made by KXX (MIT License)            |
# ++--------------------------------++
# | This is the config file for the bot. |
# | Please fill the config file before   |
# Key word that you want to search for.
key_word : "default"
# Company code that you want to search for.
company_code : "default"
# Company name that you want to search for.
company_name : "default"
# The date that you want to search for.
publish_date : "default"
# The time that you want to search for.
publish_time : "default"
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
                'key_word': data['key_word'],
                'company_code': data['company_code'],
                'company_name': data['company_name'],
                'publish_date': data['publish_date'],
                'publish_time': data['publish_time']
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()
