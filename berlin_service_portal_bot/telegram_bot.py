import requests

class TelegramBot:
  def __init__(self, token, chat):
    self.token = token
    self.chat = chat

  def send_photo(self, photo_path):
    with open(photo_path, 'rb') as stream:
      requests.post("https://api.telegram.org/bot" + self.token + "/sendPhoto",
                    params={'chat_id': self.chat}, files={'photo': stream})

  def send_text(self, text):
    requests.get("https://api.telegram.org/bot" + self.token + "/sendMessage",
                 params={'chat_id': self.chat, 'parse_mode': 'Markdown', 'text': text})
