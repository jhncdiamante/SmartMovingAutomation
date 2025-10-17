
from src.CRM.SmartMoving.Filters.OfficeCalendarDropdownFilter import OfficeCalendarEventFilter, DefaultFilter

from selenium.webdriver.common.by import By


class LostLeadsAndOpportunitiesSummaryDateFilter(DefaultFilter):

    @property
    def _locator(self):
        return (By.XPATH, "//span[@class='display-value' and normalize-space(text())='By Move Date']")
         




