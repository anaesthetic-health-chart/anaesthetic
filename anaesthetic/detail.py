"""
The custom Micro Haem detail view.
"""
from opal.core import detail
from opal.models import UserProfile

class AnaestheticReadings(detail.PatientDetailView):
    order = 1
    name = 'anaesthetic_reading'
    display_name = 'Anaesthetic Readings'
    template   = 'anaesthetic/detail/reading_detail.html'
