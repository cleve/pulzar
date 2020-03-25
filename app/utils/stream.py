import configparser

class Config:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read(config_path)

    def get_sections(self):
        """Get all sections"""
        return self.config.sections()

    def get_config(self, section, config):
        """Get config from a section"""
        if config in self.config:
            return self.config[section][config]
        return None