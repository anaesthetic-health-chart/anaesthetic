"""
anaesthetic models.
"""
from django.db import models as db_models

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
    drug_type = db_models.CharField(max_length=255)
    rates = db_models.CharField(max_length=255)
    rates = db_models.CharField(max_length=255)
    started = db_models.DateTimeField()
    stopped = db_models.DateTimeField()
    one_off = db_models.DateTimeField()


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
    height       = db_models.FloatField(blank=True, null=True)
    weight       = db_models.FloatField(blank=True, null=True)
    datetime = db_models.DateTimeField()


class AnaestheticTechnique(models.PatientSubrecord):
    induction = db_models.TextField(blank=True, null=True)
    maintenance = db_models.TextField(blank=True, null=True)


class Gases(models.PatientSubrecord):
    inspired_carbon_dioxide = db_models.FloatField(blank=True, null=True)
    expired_carbon_dioxide = db_models.FloatField(blank=True, null=True)
    inspired_oxygen = db_models.FloatField(blank=True, null=True)
    expired_oxygens = db_models.FloatField(blank=True, null=True)


class Ventilators(models.PatientSubrecord):
    mode = db_models.CharField(max_length=255)
    peak_airway_pressure = db_models.FloatField(blank=True, null=True)
    mean_airway_pressure = db_models.FloatField(blank=True, null=True)
    rate = db_models.IntegerField(blank=True, null=True)