from opal.core import detail
from opal.models import UserProfile

class AnaestheticReadings(detail.PatientDetailView):
    order = 1
    name = 'anaesthetic_reading'
    display_name = 'Anaesthetic Chart'
    # title = 'Anaesthetic Readings'
    template   = 'anaesthetic/detail/reading_detail.html'

class PreopAssessment(detail.PatientDetailView):
    name    = 'preop_assessment'
    display_name    = 'Pre Op Assessment'
    template        = 'anaesthetic/detail/preopassessment.html'
