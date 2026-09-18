from fuzzyLogicGeneral import FuzzyController, FuzzyVariable, FuzzySet


# ============================================================
# EJEMPLOS
# ============================================================

def Control_temperatura_humedad():
    """
    Control difuso para temperatura y humedad.
    Entradas : temperatura (°C), humedad (%)
    Salida   : potencia del sistema de climatización (0-100%)
    """
    # --- Variable: Temperatura ---
    temp = FuzzyVariable("Temperatura", 0, 50)  
    temp.add_set(FuzzySet("FRIA",    "trapL", [0,  10, 20]))
    temp.add_set(FuzzySet("FRESCA",  "tri",   [15, 20, 27]))
    temp.add_set(FuzzySet("COMODA",  "tri",   [22, 26, 30]))
    temp.add_set(FuzzySet("CALIDA",  "tri",   [27, 32, 38]))
    temp.add_set(FuzzySet("CALIENTE","trapR", [35, 42, 50]))

    # --- Variable: Humedad ---
    hum = FuzzyVariable("Humedad", 0, 100)
    hum.add_set(FuzzySet("SECA",    "trapL", [0,  20, 35]))
    hum.add_set(FuzzySet("NORMAL",  "tri",   [30, 50, 70]))
    hum.add_set(FuzzySet("HUMEDA",  "trapR", [65, 80, 100]))

    # --- Variable de Salida: Potencia del climatizador ---
    clima = FuzzyVariable("Climatizador", 0, 100)
    clima.add_set(FuzzySet("APAGADO",   "trapL", [0,  5,  15]))
    clima.add_set(FuzzySet("BAJO",      "tri",   [10, 25, 40]))
    clima.add_set(FuzzySet("MEDIO",     "tri",   [35, 50, 65]))
    clima.add_set(FuzzySet("ALTO",      "tri",   [60, 75, 90]))
    clima.add_set(FuzzySet("MAX",       "trapR", [85, 95, 100]))

    # --- Controlador ---
    ctrl = FuzzyController()
    ctrl.add_input("temp", temp)
    ctrl.add_input("hum", hum)
    ctrl.add_output("clima", clima)

    # --- Reglas ---  SI TEMPRERATURA ES A1 Y HUMEDAD A2 ENTONCES CLIMA ES B1
    reglas = [
        # Temperatura fría
        ({"temp": "FRIA",     "hum": "SECA"},    {"clima": "APAGADO"}),
        ({"temp": "FRIA",     "hum": "NORMAL"},  {"clima": "APAGADO"}),
        ({"temp": "FRIA",     "hum": "HUMEDA"},  {"clima": "BAJO"}),
        # Temperatura fresca
        ({"temp": "FRESCA",   "hum": "SECA"},    {"clima": "APAGADO"}),
        ({"temp": "FRESCA",   "hum": "NORMAL"},  {"clima": "BAJO"}),
        ({"temp": "FRESCA",   "hum": "HUMEDA"},  {"clima": "MEDIO"}),
        # Temperatura cómoda
        ({"temp": "COMODA",   "hum": "SECA"},    {"clima": "BAJO"}),
        ({"temp": "COMODA",   "hum": "NORMAL"},  {"clima": "MEDIO"}),
        ({"temp": "COMODA",   "hum": "HUMEDA"},  {"clima": "MEDIO"}),
        # Temperatura cálida
        ({"temp": "CALIDA",   "hum": "SECA"},    {"clima": "MEDIO"}),
        ({"temp": "CALIDA",   "hum": "NORMAL"},  {"clima": "ALTO"}),
        ({"temp": "CALIDA",   "hum": "HUMEDA"},  {"clima": "ALTO"}),
        # Temperatura caliente
        ({"temp": "CALIENTE", "hum": "SECA"},    {"clima": "ALTO"}),
        ({"temp": "CALIENTE", "hum": "NORMAL"},  {"clima": "MAX"}),
        ({"temp": "CALIENTE", "hum": "HUMEDA"},  {"clima": "MAX"}),
    ]
    ctrl.add_rules(reglas)
    return ctrl


# ============================================================
# PROGRAMA PRINCIPAL - Demostración
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  DEMOSTRACIÓN: Librería General de Lógica Difusa")
    print("=" * 55)

    # --- Ejemplo 1: Temperatura y Humedad ---
    print("\n[1] Control de Temperatura y Humedad")
    ctrl_clima = Control_temperatura_humedad()
    casos = [
        {"temp": 15, "hum": 40},   # fresco y normal
        {"temp": 26, "hum": 50},   # cómodo y normal
        {"temp": 38, "hum": 75},   # caliente y húmedo
        {"temp": 10, "hum": 20},   # frío y seco
    ]
    for caso in casos:
        res = ctrl_clima.compute(caso)
        print(f"  Temp={caso['temp']}°C, Hum={caso['hum']}%"
              f"  →  Climatizador: {res['clima']:.1f}%")



