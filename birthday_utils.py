import yaml
import os

def load_settings():
    settings_file = os.getenv('BIRTHDAY_SETTINGS', 'settings.yaml')
    with open(settings_file, 'r') as file:
        settings = yaml.safe_load(file)
    return settings


print('Settings file: ' + os.getenv('BIRTHDAY_SETTINGS', 'settings.yaml'))