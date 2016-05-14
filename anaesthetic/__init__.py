"""
anaesthetic - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'anaesthetic.schema'
    flow_module   = 'anaesthetic.flow'
    javascripts   = [
        'js/anaesthetic/routes.js',
        'js/opal/controllers/discharge.js'
    ]
    styles = [
        "css/anaesthetic.css"
    ]
