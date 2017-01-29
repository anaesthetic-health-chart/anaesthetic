"""
anaesthetic models.
"""
from datetime import datetime
from django.db import models as db_models

from opal.core import fields
from opal import models
from opal.core import lookuplists

class Demographics(models.Demographics): pass
class Location(models.Location): pass
class Allergies(models.Allergies): pass
class Diagnosis(models.Diagnosis): pass
class PastMedicalHistory(models.PastMedicalHistory): pass
class Treatment(models.Treatment): pass
class Investigation(models.Investigation): pass

class GivenDrug(models.PatientSubrecord):
    _title = "Given Drug"
    _sort           = 'datetime'

    route       = db_models.CharField(max_length=255)
    drug_name   = db_models.CharField(max_length=255)
    drug_type   = db_models.CharField(max_length=255)
    rates       = db_models.CharField(max_length=255)
    datetime    = db_models.DateTimeField(blank=True, null=True)


class RemoteAdded(models.PatientSubrecord):
    class Meta:
        abstract = True

    def update_from_dict(self, data, user, force=False):
        data["patient_id"] = 1

        if "datetime" not in data:
            data["datetime"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return super(RemoteAdded, self).update_from_dict(data, user, force=True)

    def set_created_by_id(self, incoming_value, user, *args, **kwargs):
        pass

    def set_updated_by_id(self, incoming_value, user, *args, **kwargs):
        pass


class PatientPhysicalAttributes(models.PatientSubrecord):
    height       = db_models.FloatField(blank=True, null=True)
    weight       = db_models.FloatField(blank=True, null=True)


class Observation(RemoteAdded):
    _sort           = 'datetime'
    _icon           = 'fa fa-line-chart'
    _list_limit     = 1
    _angular_service = 'ObservationRecord'

    bp_systolic  = db_models.FloatField(blank=True, null=True)
    bp_diastolic = db_models.FloatField(blank=True, null=True)
    pulse        = db_models.FloatField(blank=True, null=True)
    resp_rate    = db_models.FloatField(blank=True, null=True)
    sp02         = db_models.FloatField(blank=True, null=True)
    temperature  = db_models.FloatField(blank=True, null=True)
    datetime     = db_models.DateTimeField()

class MaskVent(lookuplists.LookupList): pass
class airway(lookuplists.LookupList): pass
class CormackLehane(lookuplists.LookupList): pass
class Position(lookuplists.LookupList): pass
class Induction_type(lookuplists.LookupList): pass

class Induction(models.EpisodeSubrecord):
    _title = "Induction"
    _is_singleton = True

    MaskVent        = fields.ForeignKeyOrFreeText(MaskVent)
    Airway          = fields.ForeignKeyOrFreeText(airway)
    CormackLehane   = fields.ForeignKeyOrFreeText(CormackLehane)
    Size            = db_models.FloatField(blank=True, null=True)
    Description     = db_models.TextField(blank=True, null=True)
    Propofol_dose   = db_models.FloatField(blank=True, null=True, default="200")
    Atracurium_dose = db_models.FloatField(blank=True, null=True,)
    Fentanyl_dose   = db_models.FloatField(blank=True, null=True, default="100")
    Induction_type  = fields.ForeignKeyOrFreeText(Induction_type)
    Position        = fields.ForeignKeyOrFreeText(Position)

class AnaestheticTechnique(models.PatientSubrecord):
    _title          = "Event"

    Title       = db_models.TextField(blank=True, null=True)
    Description = db_models.TextField(blank=True, null=True)
    datetime    = db_models.DateTimeField(blank=True, null=True)



class Gases(RemoteAdded):
    _title = "Gases"
    inspired_carbon_dioxide = db_models.FloatField(blank=True, null=True)
    expired_carbon_dioxide = db_models.FloatField(blank=True, null=True)
    inspired_oxygen = db_models.FloatField(blank=True, null=True)
    expired_oxygen = db_models.FloatField(blank=True, null=True)
    expired_aa = db_models.FloatField(blank=True, null=True)
    datetime = db_models.DateTimeField()


class Ventilators(RemoteAdded):
    _title = "Ventilation"
    mode = db_models.CharField(max_length=255)
    peak_airway_pressure = db_models.FloatField(blank=True, null=True)
    peep_airway_pressure = db_models.FloatField(blank=True, null=True)
    tidal_volume = db_models.FloatField(blank=True, null=True)
    rate = db_models.IntegerField(blank=True, null=True)
    datetime = db_models.DateTimeField()
