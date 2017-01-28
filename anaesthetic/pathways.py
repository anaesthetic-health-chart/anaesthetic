from pathway.pathways import PagePathway, Step


class DrugPathway(PagePathway):
    display_name = "Induction Drugs"
    slug = "induction_drugs"
    Step(
        template_url="templates/pathways/induction_form.html",
        display_name="blah",
        icon="fa fa icon",
        step_controller="InductionDrugController"
    )
