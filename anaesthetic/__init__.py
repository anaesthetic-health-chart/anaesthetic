"""
anaesthetic - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'anaesthetic.schema'
    flow_module   = 'anaesthetic.flow'
    javascripts   = [
        'js/anaesthetic/routes.js',
        'js/anaesthetic/controllers/drug_controller.js',
        'js/anaesthetic/controllers/graph_controller.js',
        'js/anaesthetic/services/records/observation_record.js',
        'js/anaesthetic/services/drug_loader.js',
        'js/anaesthetic/graphlib.js',
    ]
    styles = [
        "css/anaesthetic.css"
    ]
