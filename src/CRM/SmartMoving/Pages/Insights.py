from src.CRM.Page import IPage

class Insights(IPage):
    def __init__(self):
        self.route = "https://app.smartmoving.com/reports/smart-insights/lists"
