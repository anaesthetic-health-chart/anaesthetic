from pathway.pathways import PagePathway, Step


class DrugPathway(PagePathway):
    display_name = "Induction Drugs"
    slug = "induction_drugs"
    steps = (Step(
        template_url="templates/pathways/induction_drugs.html",
        display_name="blah",
        icon="fa fa icon",
        step_controller="InductionDrugController"
    ),)
