from fuzzyLogicGeneral import FuzzyController, FuzzyVariable, FuzzySet

def ejemplo_balanceo_grua():
  angulo = FuzzyVariable("Angulo", -30, 30)
  angulo.add_set(FuzzySet("GN", "trapL", [-30, -20, -10]))
  
  angulo.add_set(FuzzySet("GN", "trapL", [-30, -20, -10]))
  angulo.add_set(FuzzySet("MN", "tri", [-15, -8, -3]))
  angulo.add_set(FuzzySet("PN", "tri", [-5, -2, 0]))
  angulo.add_set(FuzzySet("CE", "tri", [-3, 0, 3]))
  angulo.add_set(FuzzySet("PP", "tri", [0, 2, 5]))
  angulo.add_set(FuzzySet("MP", "tri", [3, 8, 15]))
  angulo.add_set(FuzzySet("GP", "trapR", [10, 20, 30]))
  
  velocidad = FuzzyVariable("Velocidad", -100, 100)
  velocidad.add_set(FuzzySet("VGN", "trapL", [-100, -70, -40]))
  velocidad.add_set(FuzzySet("VMN", "tri", [-100, -70, -40]))
  velocidad.add_set(FuzzySet("VPN", "trapL", [-100, -70, -40]))
  velocidad.add_set(FuzzySet("VCE", "trapL", [-100, -70, -40]))
  velocidad.add_set(FuzzySet("VGN", "trapL", [-100, -70, -40]))
  velocidad.add_set(FuzzySet("VGN", "trapL", [-100, -70, -40]))
  velocidad.add_set(FuzzySet("VGN", "trapL", [-100, -70, -40]))
  velocidad.add_set(FuzzySet("VGN", "trapL", [-100, -70, -40]))
 