from rest_framework import viewsets
from anaesthetic.lists_of_drugs import all_drugs
from opal.core.views import _build_json_response


class ListOfDrugs(viewsets.ViewSet):
    def list(self, request):
        return _build_json_response(all_drugs)
