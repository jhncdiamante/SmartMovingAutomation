from src.CRM.SmartMoving.Pages.InsightsPage.BookingPercentBySurveyType import BookingPercentBySurveyType
from src.CRM.SmartMoving.Pages.InsightsPage.CompletedMoves import CompletedMoves
from src.CRM.SmartMoving.Pages.SmartMovingPage import SmartMovingPage
from src.CRM.SmartMoving.Pages.InsightsPage.OutstandingBalances import OutstandingBalances
from src.Chrome.IDriver import IDriver
from src.CRM.SmartMoving.Pages.InsightsPage.SalespersonPerformance import SalespersonPerformance

from src.CRM.SmartMoving.Pages.InsightsPage.AccountingJobRevenue import AccountingJobRevenue
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByDateBooked import BookedOpportunitiesByDateBooked
from src.CRM.SmartMoving.Pages.InsightsPage.BookOpportunitiesByServiceDate import BookedOpportunitiesByServiceDate
from src.CRM.SmartMoving.Pages.InsightsPage.LostLeadsAndOpportunitiesSummary import LostLeadsAndOpportunitiesSummary
from src.CRM.SmartMoving.Pages.InsightsPage.AccountingStorageRevenue import AccountingStorageRevenue
from src.CRM.SmartMoving.Pages.InsightsPage.EstimateAccuracySummary import EstimateAccuracySummary

class Insights(SmartMovingPage):
    def __init__(
        self,
        route: str,
        driver: IDriver,
        accounting_job_revenue: AccountingJobRevenue,
        booked_opportunities_by_date_booked: BookedOpportunitiesByDateBooked,
        booking_percent_by_survey_type: BookingPercentBySurveyType,
        accounting_storage_revenue: AccountingStorageRevenue,
        booked_opportunities_by_service_date: BookedOpportunitiesByServiceDate,
        outstanding_balances: OutstandingBalances,
        salesperson_performance: SalespersonPerformance,
        lost_leads_and_opportunities_summary: LostLeadsAndOpportunitiesSummary,
        estimate_accuracy_summary: EstimateAccuracySummary,
        completed_moves: CompletedMoves
    ):
        super().__init__(route, driver)

        self.accounting_job_revenue = accounting_job_revenue
        self.booked_opportunities_by_date_booked = booked_opportunities_by_date_booked
        self.booked_opportunities_by_service_date = booked_opportunities_by_service_date

        self.booking_percent_by_survey_type = booking_percent_by_survey_type
        self.accounting_storage_revenue = accounting_storage_revenue
        self.outstanding_balances = outstanding_balances
        self.salesperson_performance = salesperson_performance
        self.lost_leads_and_opportunities_summary = lost_leads_and_opportunities_summary
        self.estimate_accuracy_summary = estimate_accuracy_summary
        self.completed_moves = completed_moves
