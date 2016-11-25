"""
Defining OPAL PatientLists
"""
from opal import core
from opal.models import Episode
from opal.core.patient_lists import TaggedPatientList
from anaesthetic import models

class AllPatientsList(core.patient_lists.PatientList):
    display_name = 'All Patients'

    schema = [
        models.Demographics,
        models.Diagnosis,
        models.Treatment
    ]

    def get_queryset(self):
        return Episode.objects.all()

class Theatre1(TaggedPatientList):
    display_name = "Theatre 1"
    tag = "Theatre_1"

class Theatre2(TaggedPatientList):
    display_name = "Theatre 2"
    tag = "Theatre_2"
