"""
anaesthetic - Our OPAL Application
"""
from opal.core import application

class Application(application.OpalApplication):
    schema_module = 'anaesthetic.schema'
    flow_module   = 'anaesthetic.flow'
    javascripts   = [
        'js/anaesthetic/routes.js',
    ]
    styles = [
        "css/anaesthetic.css"
    ]
    angular_module_deps = [
        'js/anaesthetic/graphlib.js'
    ]
