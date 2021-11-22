import bot
import time

from bot import Bot


class ServicePortalBot(Bot):
  def __init__(self):
    super().__init__("Service-Portal Bot")

    # Pre-setup appointment information for date selection page
    self.config.get_int(
        "service_portal_bot",
        "month",
        "What's the month which I should book? (maximum of 4 months ahead)"
    )

    self.config.get_int(
        "service_portal_bot",
        "year",
        "What's the year which I should book? (maximum of 4 months ahead)"
    )

  def load_services_page(self):
    self.web_driver.page(
        "https://service.berlin.de/dienstleistung/"
    )
    print("Loading services A-Z page")

  def click_selected_service(self):
    if self.config.has("service_portal_bot", "service"):
      selection = self.config.get("service_portal_bot", "service")
    else:
      letter = self.config.ask("What's the first letter of the service?")
      options = self.web_driver.get_contents(
          f"//div[@class='azlist']//h2[@id='dl_{letter.upper()}']/following-sibling::ul[@class='list']//a"
      )

      index = 0
      for option in options:
        print(f"({index}) {option}")
        index += 1

      selection = options[self.config.ask_int("Select the service (index)")]
      self.config.write("service_portal_bot", "service", selection)

    self.web_driver.click(
        f"//div[@class='azlist']//a[contains(text(), '{selection}')]"
    )
    print(
        f"Clicking on \"{selection}\" as for the service selection"
    )

  def click_search_appointments_across_berlin_button(self):
    self.web_driver.click("//a[contains(text(), 'Termin berlinweit suchen')]")
    print(
        f"Clicking on \"Search appointments across Berlin\""
    )

  def __month_to_text(self, month):
    return ["Januar", "Februar", "März", "April", "Mai", "Juni",
            "Juli", "August", "September", "Oktober", "November", "Dezember"
            ][month - 1]

  def __check_captcha(self):
    # https://service.berlin.de/terminvereinbarung/termin/human/
    if "/human" in self.web_driver.current_url():
      self._notify(
          "There's a captcha, I had been caught. I need your support!")
      captcha = self.config.ask("Pss, what's the captcha?")
      self.web_driver.fill("//input[@id='captcha_text']", captcha)
      print(f"Filling \"{captcha}\" as for the captcha")
      self.web_driver.click(
          "//button[@type='submit' and contains(text(), 'Bitte bestätigen')]")
      print(f"Clicking \"Please confirm\" to confirm the captcha")

  def search_calendar(self):
    month = self.config.get_int("service_portal_bot", "month")
    year = self.config.get_int("service_portal_bot", "year")
    self.current_calendar = f"{self.__month_to_text(month)} {year}"

    maximum_next_clicks = 3
    while maximum_next_clicks:
      self.__check_captcha()
      self.web_driver.wait_visibility("//th[@class='month']")

      if self.web_driver.has_element(f"//th[@class='month' and contains(text(), '{self.current_calendar}')]"):
        print(f"Calendar \"{self.current_calendar}\" found")
        return
      else:
        print(
            f"Searching for \"{self.current_calendar}\" calendar, clicking next")
        self.web_driver.click("//th[@class='next']")
        maximum_next_clicks -= 1
        time.sleep(5)
        continue

    raise Exception(f"Calendar \"{self.current_calendar}\" not found")

  def check_available_appointments(self):
    count = 0

    while 1:
      self.__check_captcha()
      self.web_driver.wait_visibility("//th[@class='month']")

      if self.web_driver.has_element(f"//th[@class='month' and contains(text(), '{self.current_calendar}')]/ancestor::table//td[@class='buchbar']/a"):
        self._notify("Hurry up! There's an appointment available")
        self.web_driver.click(
            f"//th[@class='month' and contains(text(), '{self.current_calendar}')]/ancestor::table//td[@class='buchbar']/a")
        print(
            f"Clicking on the first available calendar date for \"{self.current_calendar}\""
        )
        break
      else:
        print(f"({count}) No appointments yet")
        count += 1
        self.web_driver.refresh()

      time.sleep(self.refresh_interval)


def main():
  def __load():
    service_portal_bot = ServicePortalBot()

    # Services A-Z page
    service_portal_bot.load_services_page()
    service_portal_bot.click_selected_service()
    service_portal_bot.click_search_appointments_across_berlin_button()

    # Appointment page
    service_portal_bot.search_calendar()
    service_portal_bot.check_available_appointments()

  bot.loop(__load)


if __name__ == '__main__':
  main()
