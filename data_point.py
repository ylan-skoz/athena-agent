from datetime import datetime

class dataPoint:

    data: str
    data_type: str
    component: str
    message_emission_date: datetime
    message_reception_date: datetime
    module: str

    def __init__(self, data, data_type, component, message_emission_date, message_reception_date = None, module = None) -> None:
        
        self.data = data
        self.data_type = data_type
        self.component = component
        self.message_emission_date = message_emission_date
        self.message_reception_date = message_reception_date
        self.module = module