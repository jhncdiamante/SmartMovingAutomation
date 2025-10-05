from selenium.webdriver.common.by import By
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByDateBooked import BookedOpportunitiesByDateBooked

class BookOpportunitiesByServiceDate(BookedOpportunitiesByDateBooked):
    def _locator(self) -> tuple[By, str]:
        return (By.XPATH,"//a[normalize-space(text())='Book Opportunities by Service Date']")
