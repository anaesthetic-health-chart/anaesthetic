"""
anaesthetic - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'anaesthetic.schema'
    flow_module   = 'anaesthetic.flow'
    javascripts   = [
        'js/anaesthetic/routes.js',
        'js/anaesthetic/filters.js',
        'js/anaesthetic/controllers/drug_controller.js',
        'js/anaesthetic/services/records/observation_record.js',
        'js/anaesthetic/controllers/newgraph.js',
        'js/anaesthetic/controllers/induction_drug_controller.js',
    ]
    styles = [
        "css/anaesthetic.css",
        "css/anaesthetic_drug_colours.css",
        "css/anaesthetic_drug_colours.scss"

    ]
