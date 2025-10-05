
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from src.Chrome.IDriver import IDriver
from selenium.webdriver.common.by import By
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingPercentBySurveyType(InsightsPage):
    def __init__(self, driver: IDriver, calendar_filter: CalendarFilter):
        super().__init__(driver)
        self.calendar_filter = calendar_filter

    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Booking Percent by Survey Type']")

    def _get_total_booked_percentaged(self, booking_type:str) -> float:
        xpath = f"//sm-viper-text-column-template[normalize-space(text())='{booking_type}']/parent::*[1]/following-sibling::*[3]"
        total_booked_percentage = WebDriverWait(self._driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return float(total_booked_percentage.replace("%", "").strip()) / 100


    def get_on_site_survey_total_booked(self):
        return self._get_total_booked_percentaged("On-Site Survey")
        

    def get_no_survey_total_booked_percentage(self) -> float:
        return self._get_total_booked_percentaged("No Survey")
