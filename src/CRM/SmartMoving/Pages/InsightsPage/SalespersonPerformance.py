from src.CRM.SmartMoving.Filters.SidePanelFilter import SidePanelFilter
from src.CRM.SmartMoving.Pages.InsightsPage.InsightsPage import InsightsPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.CRM.SmartMoving.Filters.SalespersonPerformanceDateTypeFilter import SalespersonPerformanceDateTypeFilter
from src.CRM.SmartMoving.Filters.CalendarFilter import CalendarFilter
from selenium.common.exceptions import TimeoutException
import time
import requests
from datetime import date, timedelta
from src.CRM.SmartMoving.API import extract_auth_token
from src.CRM.SmartMoving.API import SALESPERSON_PERFORMANCE_PAGE_API_URL


class SalespersonPerformance(InsightsPage):
    def __init__(self, driver, calendar_filter: CalendarFilter, date_type_filter: SalespersonPerformanceDateTypeFilter,
    side_panel_filter: SidePanelFilter):
        super().__init__(driver)

        self.calendar_filter = calendar_filter
        self.date_type_filter = date_type_filter
        self.side_panel_filter = side_panel_filter

    def _get_lead_info(self, xpath: str) -> int:
        self._logger.info("Attempting to get leads info...")
        try:
            leads_info = WebDriverWait(self._driver, self.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return int(leads_info.text.strip())
        except TimeoutException:
            self._logger.warning("Failed to get leads info under 60 seconds.")
        except ValueError:
            self._logger.warning(f"Unable to convert {leads_info.text} to int.")


    def get_bad_leads(self) -> int | None:
        return self._get_lead_info("//span[normalize-space(text())='Bad']/following-sibling::h2/span[1]")


    def get_leads_received(self) -> int:
        return self._get_lead_info("//span[normalize-space(text())='Leads Received']/following-sibling::h2")


    def get_total_leads_received_prior_year(self) -> int | None:
        """Fetch total bad leads count for the same week last year via API."""
        auth_token = extract_auth_token(self._driver)
        try:
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            try:
                last_year_start = start_of_week.replace(year=start_of_week.year - 1)
                last_year_end = end_of_week.replace(year=end_of_week.year - 1)
            except ValueError:
                last_year_start = (start_of_week - timedelta(days=1)).replace(year=start_of_week.year - 1)
                last_year_end = (end_of_week - timedelta(days=1)).replace(year=end_of_week.year - 1)

            start_iso = f"{last_year_start.isoformat()}T00:00:00.000+08:00"
            end_iso = f"{last_year_end.isoformat()}T23:59:59.999+08:00"
                        
            payload = {
                "parameters": [
                    {
                        "filterType": "DateRanges",
                        "selectedMode": "CreatedAtUtc",
                        "modes": [
                            {"id": "ServiceDate", "isDefault": True, "name": "Move Date"},
                            {"id": "CreatedAtUtc", "isDefault": False, "name": "Lead Received Date"}
                        ]
                    },
                    {
                        "filterType": "DateRange",
                        "dateFilterType": "ServiceDate",
                        "quickFilter": None,
                        "startDateUtc": start_iso,
                        "endDateUtc": end_iso,
                        "allowMultipleDays": True
                    },
                    {"filterType": "Branch", "filterMode": "AnyOf", "branchIds": []},
                    {"filterType": "ReferralSource", "filterMode": "AnyOf", "referralSourceIds": []},
                    {"filterType": "SalesPerson", "filterMode": "AnyOf", "salesPersonIds": []}
                ]
            }


            self._logger.info(f"PAYLOAD: {payload}")

            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://app.smartmoving.com",
                "Referer": "https://app.smartmoving.com/",
            }

            self._logger.info(f"Requesting prior-year data for {last_year_start} – {last_year_end}...")
            response = requests.post(f"{SALESPERSON_PERFORMANCE_PAGE_API_URL}/visualizations", headers=headers, json=payload, timeout=30)

            if response.status_code != 200:
                self._logger.warning(f"API request failed ({response.status_code}): {response.text}")
                return None

            data = response.json()
            primary_values = [item["primaryValue"] for item in data if "primaryValue" in item]
            value = primary_values[1]
            self._logger.info(f"Last year total leads received: {primary_values[0]}")
            self._logger.info(f"Last year total bad leads count: {primary_values[1]}")
            return float(primary_values[0] - primary_values[1])
        except Exception as e:
            self._logger.warning(f"Error fetching last year total bad leads count: {e}")
            return None

        