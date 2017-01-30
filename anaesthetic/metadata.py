from django.conf import settings
from opal.core import metadata

class DrugTypes(metadata.Metadata):
    slug = 'drug_type'

    @classmethod
    def to_dict(klass, *args, **kwargs):
        return {
                "drug_type": {
                    "Antiemetic drug": [
                        "Dexametasone", "Ondansetron", "Granisetron", "Cyclizine", "Metoclopramide"
                    ],
                    "Induction agent drug": [
                        "Propofol", "Thiopentone", "Etomidate", "Ketamine"
                    ],
                    "Hypnotic drug": [
                        "Midazolam", "Diazepam", "Lorazepam"
                        ],
                    "Hypnotic antagonist drug": [
                        "Flumazenil"
                        ],
                    "Neuromuscular blocking drug": [
                        "Atracurium", "Mivacurium", "Cisatracurium", "Rocuronium", "Vecuronium"
                    ],
                    "Neuromuscular blocking drug antagonist": [
                        "Neostigmine with glycopyrrolate", "Sugammadex", "Neostigmine"
                    ],
                    "Depolarizing neuromuscular blocking drug": ["Suxamethonium"],
                    "Opioid drug": [
                        "Morphine", "Fentanyl", "Remifentanil", "Alfentanil",
                    ],
                    "Opioid antagonist": ["Naloxone"],
                    "Vasopressor drug": [
                        "Metaraminol", "Phenylephrine", "Noradrenaline", "Adrenaline", "Ephedrine"
                    ],
                    "Local anaesthetics drug": [
                        "Bupivicaine", "Lidocaine", "Levobupivicaine", "Prilocaine"
                    ],
                    "Anticholinergic drug": ["Glycopyrrolate", "Atropine"],
                    "Other drug agents": [
                        "Cefuroxime", "Metronidazole", "Gentamicin", "Co-amoxiclav"
                    ],
            }
        }
