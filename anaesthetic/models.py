"""
anaesthetic models.
"""
from django.db import models as db_models
from opal.core.lookuplists import LookupList

from opal import models

class Demographics(models.Demographics): pass
class Location(models.Location): pass
class Allergies(models.Allergies): pass
class Diagnosis(models.Diagnosis): pass
class PastMedicalHistory(models.PastMedicalHistory): pass
class Treatment(models.Treatment): pass
class Investigation(models.Investigation): pass


class GivenDrug(models.PatientSubrecord):
    DRUG_TYPES = [
        "induction_agent",
        "opiat"
    ]

    route = db_models.CharField(max_length=255)
    drug_name = db_models.CharField(max_length=255)
    drug_type = db_models.CharField(max_length=255)
    rates = db_models.CharField(max_length=255)
    rates = db_models.CharField(max_length=255)
    started = db_models.DateTimeField(blank=True, null=True)
    stopped = db_models.DateTimeField(blank=True, null=True)
    one_off = db_models.DateTimeField(blank=True, null=True)

class PatientPhysicalAttributes(models.PatientSubrecord):
    height       = db_models.FloatField(blank=True, null=True)
    weight       = db_models.FloatField(blank=True, null=True)


class Observation(models.PatientSubrecord):
    _sort           = 'datetime'
    _icon           = 'fa fa-line-chart'
    _list_limit     = 1

    bp_systolic  = db_models.FloatField(blank=True, null=True)
    bp_diastolic = db_models.FloatField(blank=True, null=True)
    pulse        = db_models.FloatField(blank=True, null=True)
    resp_rate    = db_models.FloatField(blank=True, null=True)
    sp02         = db_models.FloatField(blank=True, null=True)
    temperature  = db_models.FloatField(blank=True, null=True)
    datetime = db_models.DateTimeField()

    def update_from_dict(self, data, user, force=False):
        data["episode_id"] = 1
        return super(Observation, self).update_from_dict(data, user, force=True)


class AnaestheticTechnique(models.PatientSubrecord):
    _title = "Anaesthetic Technique"
    _is_singleton = True
    induction = db_models.TextField(blank=True, null=True)
    maintenance = db_models.TextField(blank=True, null=True)


class Gases(models.PatientSubrecord):
    _title = "Gases"
    inspired_carbon_dioxide = db_models.FloatField(blank=True, null=True)
    expired_carbon_dioxide = db_models.FloatField(blank=True, null=True)
    inspired_oxygen = db_models.FloatField(blank=True, null=True)
    expired_oxygen = db_models.FloatField(blank=True, null=True)
    datetime = db_models.DateTimeField()


class Ventilators(models.PatientSubrecord):
    _title = "Ventilators"
    mode = db_models.CharField(max_length=255)
    peak_airway_pressure = db_models.FloatField(blank=True, null=True)
    peep_airway_pressure = db_models.FloatField(blank=True, null=True)
    rate = db_models.IntegerField(blank=True, null=True)
    datetime = db_models.DateTimeField()
