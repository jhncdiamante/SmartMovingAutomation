
from turtle import setup

from selenium.common.exceptions import TimeoutException, WebDriverException
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Drivers.IDriver import IDriver
from selenium.webdriver.common.by import By
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingPercentBySurveyType(InsightsPage):
    DEFAULT_TIMEOUT = 60

    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter

    @property
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Booking Percent by Survey Type']")

    def _get_total_booked_percentage(self, booking_type:str) -> float:
        xpath = f"//tr[.//td[.//text()[normalize-space(.)='{booking_type}']]]/td[4]"

        try:
            total_booked_percentage = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            self._logger.info(f"Extracted total booked_percentage: {total_booked_percentage.text}.")
        except TimeoutException:
            self._logger.warning(f"Failed to get total booked percentaged for {booking_type}.")
            return
        except WebDriverException as e:
            self._logger.warning(f"Failed to get total booked percentage due to error {e}")
            return

        try:
            return float(total_booked_percentage.text.replace("%", "").strip()) / 100
        except ValueError:
            self._logger.warning(f"Unable to convert {total_booked_percentage.text} to float.")


    def get_on_site_survey_total_booked_percentage(self) -> float or None:
        return self._get_total_booked_percentage("On-Site Survey")
        

    def get_no_survey_total_booked_percentage(self) -> float or None:
        return self._get_total_booked_percentage("No Survey")


