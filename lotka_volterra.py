import antimony

def get_antimony_model():
    return """
    model lotka_volterra
    J1: prey -> prey + prey; alpha * prey
    J2: prey + predator -> predator + predator; beta * prey * predator
    J3: predator -> ; gamma_ * predator

    prey = 10
    predator = 5

    alpha = 1.1
    beta = 0.4
    gamma_ = 0.4
    end
    """

def get_sbml_model():
    antimony.clearPreviousLoads()
    antimony.freeAll()
    code = antimony.loadAntimonyString(get_antimony_model())
    if code >= 0:
        mid = antimony.getMainModuleName()
        sbml_model = antimony.getSBMLString(mid)
        return sbml_model
    raise Exception("Error in loading antimony model", code)

# Write SBML to file
sbml_str = get_sbml_model()
with open("lotka_volterra.xml", "w") as f:
    f.write(sbml_str)

print("Lotka-Volterra model written to lotka_volterra.xml")
