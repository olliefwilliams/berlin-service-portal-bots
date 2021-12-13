import requests

class TelegramBot:


  def __init__(self, token, chat):
    self.token = token
    self.chat = chat
    self.base_url = f"https://api.telegram.org/bot{self.token}/"


  def send_photo(self, photo_path, caption=""):
    with open(photo_path, 'rb') as stream:
      return requests.post(self.base_url + "sendPhoto",
                    params={'chat_id': self.chat, 'caption': caption}, files={'photo': stream})

  def send_text(self, text):
    return requests.get(self.base_url + "sendMessage",
                 params={'chat_id': self.chat, 'parse_mode': 'Markdown', 'text': text})

  def get_updates(self):
    return requests.get(self.base_url + "getUpdates")