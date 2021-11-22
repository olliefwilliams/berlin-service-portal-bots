import configparser

from os.path import dirname, abspath, join


class Config:
  def __init__(self):
    self.config_path = join(dirname(dirname(abspath(__file__))), ".cfg")
    self.config = configparser.ConfigParser()
    self.config.read(self.config_path)

  def write(self, section, option, value):
    self.config[section][option] = value
    with open(self.config_path, 'w') as stream:
      self.config.write(stream)

  def ask(self, question):
    return input(question + "\n")

  def ask_int(self, question):
    return int(self.ask(question))

  def ask_boolean(self, question):
    return configparser.RawConfigParser()._convert_to_boolean(self.ask(question))

  def has(self, section, option):
    if self.config[section][option]:
      return 1
    return 0

  def get(self, section, option, question=0):
    try:
      return self.config.get(section, option)
    except:
      value = self.ask(question)
      self.write(section, option, value)
      return value

  def get_int(self, section, option, question=0):
    try:
      return self.config.getint(section, option)
    except:
      value = self.ask_int(question)
      self.write(section, option, str(value))
      return value

  def get_boolean(self, section, option, question=0):
    try:
      return self.config.getboolean(section, option)
    except:
      value = self.ask_boolean(question)
      self.write(section, option, str(value))
      return value
