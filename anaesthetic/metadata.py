from django.conf import settings
from opal.core import metadata

class DrugTypes(metadata.Metadata):
    slug = 'drug_type'

    @classmethod
    def to_dict(klass, *args, **kwargs):
        return {"drug_type": dict(
            antiemetic_drug=["dexametasone", "ondansetron", "granisetron", "cyclizine", "metoclopramide"],
            induction_agent_drug=["propofol", "thiopentone", "etomidate", "ketamine"],
            hypnotic_drug=["midazolam, diazepam, lorazepam"],
            hypnotic_antagonist_drug=["flumazenil"],
            neuromuscular_blocking_drug=["atracurium", "mivacurium", "cisatracurium", "rocuronium", "vecuronium", ],
            neuromuscular_blocking_drug_antagonist=["neostigmine with glycopyrrolate", "sugammadex", "neostigmine"],
            depolarizing_neuromuscular_blocking_drug=["suxamethonium"],
            opioid_drug=["morphine", "fentanyl", "remifentanil", "alfentanil",],
            opioid_antagonist=["naloxone"],
            vasopressor_drug=["metaraminol", "phenylephrine", "noradrenaline", "adrenaline", "ephedrine"],
            local_anaesthetics_drug=["bupivicaine", "lidocaine", "levobupivicaine", "prilocaine"],
            anticholinergic_drug=["glycopyrrolate", "atropine"],
            other_drug_agents=["cefuroxime", "metronidazole", "gentamicin", "co-amoxiclav"],
        )}
