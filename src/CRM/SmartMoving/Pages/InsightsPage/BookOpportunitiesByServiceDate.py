from selenium.webdriver.common.by import By
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByDateBooked import BookedOpportunitiesByDateBooked

class BookedOpportunitiesByServiceDate(BookedOpportunitiesByDateBooked):
    @property
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Booked Opportunities by Service Date']")
