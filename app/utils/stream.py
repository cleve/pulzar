import configparser

class Config:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read(config_path)

    def get_configs(self, section):
        """Get all configs from a section"""
        pass

    def get_config(self, section, config):
        """Get config from a section"""
        pass