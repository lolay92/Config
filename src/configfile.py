# Python unittest + mocks tutos
# https://www.youtube.com/watch?v=RNVspDHVIA0&list=PLe4mIUXfbIqaXv8kRvUqgrMREq-p5GgdV&index=3 : Python Mocks (3 videos)
# https://www.youtube.com/watch?v=6tNS--WetLI : Unittest tuto

# Python logging + decorators + property decorators tutos
# https://www.youtube.com/watch?v=-ARI4Cz-awo&t=324s : Logging basics
# https://www.youtube.com/watch?v=jxmzY9soFXg : Logging advanced
# https://www.youtube.com/watch?v=FsAPt_9Bf3U&t=73s : Decorators - Dynamically Alter The Functionality Of Your Functions
# https://www.youtube.com/watch?v=KlBPCzcQNU8 : Decorators With Arguments
# https://www.youtube.com/watch?v=jCzT9XFZ5bw : Property Decorators - Getters, Setters, and Deleters


import os
import logging
from configparser import ConfigParser
from typing import Dict, Any

# Logging set up
# logging.basicConfig(filename='configfilebuilder.log', level=logging.DEBUG,
#                     format='%(asctime)s:%(levelname)s:%(message)s')

# Logging set up
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s::%(message)s")

# Setting typing alias
_treeStructType = Dict[str, Dict[str, Any]]


class ConfigErr(Exception):
    pass


class ConfigFileGenerator:
    def __init__(self, path_to_file: str) -> None:
        """ConfigFileGenerator object instance creation with the destination folder path as an arg."""
        self.config = ConfigParser()
        self.path_to_file = path_to_file
        if os.path.isfile(self.path_to_file):
            logging.info(
                f"There is already an existing config file at this location: {path_to_file}"
            )

    def write_config(self, configmap: _treeStructType) -> ConfigParser:
        """This function aims to create a configuration file based on a tree map that
        follows the following tree structure! e.g. : configmap = {'section1': {'key1': 'value1',
        'key2': 'value2', 'key3': 'value3'}, 'section2': {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}}"""
        try:  # Build structure
            self.config.read_dict(configmap)
        except TypeError as TErr:
            # raise TErr(f"configmap attribute does not follow the tree structure!")
            pass
        except Exception as e:
            print(f"Error::{e}")
        else:  # Avoid overriding an existing file
            if os.path.isfile(self.path_to_file):
                raise ConfigErr(
                    f"The file requested to be created exists already: {self.path_to_file}"
                )
            else:
                with open(self.path_to_file, "w") as conf:
                    self.config.write(conf)
        return self.config

    def add_config(self, other_configmap: _treeStructType) -> ConfigParser:
        self.config.read(self.path_to_file)
        sections = [*other_configmap]
        existing_sections = self.config.sections()
        temp_config = ConfigParser()
        if not isinstance(other_configmap, Dict):  # Error Handling
            raise TypeError("configmap arg should be in tree format/structure!")
        # Create a temporary config file and overwrite/update the option/value for new sections
        temp_config.read_dict(other_configmap)
        # Checking for no section duplication and add new sections
        for section in sections:
            if section in existing_sections:
                raise ConfigErr(f"{section} already exists in the configuration file!")
            else:
                # Add new section with options and values
                self.config.add_section(section)
                self._config_merger(temp_config, section)
        # Write the file after updating it
        with open(self.path_to_file, "w") as conf:
            self.config.write(conf)

        return self.config

    def _config_merger(
        self, config_to_merge: ConfigParser, section: str
    ) -> ConfigParser:

        # Complete config file with new section and options & values from config_to_merge
        for option, value in config_to_merge.items(section):
            self.config.set(section, option, value)
        return self.config

    @staticmethod
    def update_section(path: str, section: str, option: str, value: Any) -> None:
        try:
            edit_conf = ConfigParser()
            if not os.path.isfile(path):
                raise FileNotFoundError(f"file does not exist at this location: {path}")
        except Exception as e:
            print(f"Error::{e}")
        else:
            edit_conf.read(path)
            edit_conf[section][option] = value
            with open(path, "w") as conf:
                edit_conf.write(conf)

    @staticmethod
    def rm_section(path: str, section: str) -> None:
        try:
            edit_conf = ConfigParser()
            if not os.path.isfile(path):
                raise FileNotFoundError(f"file does not exist at this location: {path}")
        except Exception as e:
            print(f"Error::{e}")
        else:
            edit_conf.read(path)
            edit_conf.remove_section(section)
            with open(path, "w") as conf:
                edit_conf.write(conf)
