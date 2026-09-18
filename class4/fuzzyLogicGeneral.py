# ============================================================
# fuzzyLogicGeneral.py
# Librería General de Lógica Difusa

# ============================================================

# MicroPython functools, se define reduce manualmente
try:
    from functools import reduce
except ImportError:
    def reduce(f, lst):
        result = lst[0]
        for item in lst[1:]:
            result = f(result, item)
        return result

# Resolución de la discretización para el cálculo del centroide
# Mayor precisión = cálculo más lento pero más exacto
# Recomendado: 20 para Pico W, 100 para PC
PRECISION = 20


# ============================================================
# FUNCIÓN AUXILIAR: Ecuación de línea entre dos puntos
# Retorna [pendiente m, intercepto b] de y = mx + b
# ============================================================
def lineEquation(p1, p2):
    """
    Calcula la ecuación de la recta entre dos puntos.
    p1, p2: [x, y]
    Retorna: [m, b] donde y = m*x + b
    """
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    b = p1[1] - m * p1[0]
    return [m, b]


# ============================================================
# CLASE BASE: Funciones de Membresía
# ============================================================
class MembershipFunctions:
    """
    Clase base que implementa las funciones de membresía
    más comunes en lógica difusa:
      - trimf  : triangular
      - tramfL : trapezoidal izquierda (abierta a la izquierda)
      - tramfR : trapezoidal derecha  (abierta a la derecha)
    
    Cada función tiene versión de ENTRADA (_i) y SALIDA (_o).
    Las entradas reciben un valor x y retornan su grado [0,1].
    Las salidas generan la curva discreta para el centroide.
    """

    # ----------------------------------------------------------
    # FUNCIONES DE ENTRADA (fuzzificación)
    # ----------------------------------------------------------

    def trimf_i(self, points, eqVals, x):
        """
        Función triangular de entrada.
        points: [a, b, c]  → a=inicio, b=pico, c=fin
        eqVals: [[m0,b0],[m1,b1]] ecuaciones de los lados
        x: valor a evaluar
        Retorna: grado de membresía en [0, 1]
        """
        a, b, c = points
        if x >= a and x < b:
            return eqVals[0][1] + x * eqVals[0][0]  #pendiente subida
        elif x >= b and x <= c:
            return eqVals[1][1] + x * eqVals[1][0]   # pendiente de bajada
        else:
            return 0

    def tramfL_i(self, points, eqVal, x):
     #   Trapezoidal abierta a la IZQUIERDA
     #   points: [a, b, c]  → a=donde empieza la bajada, b=donde llega a 0, c=límite derecho
     #  Retorna: 1 si x <= a, rampa descendente entre a y b, 0 si x > b
        a, b, c = points
        if x >= a and x <= b:
            return eqVal[1] + x * eqVal[0]
        elif x >= points[0] - (b - a) and x < a:  # zona plana izquierda
            return 1
        else:
            return 0

    def tramfR_i(self, points, eqVal, x):
        """
        Trapezoidal abierta a la DERECHA (para conjuntos 'MUY POSITIVO').
        points: [a, b, c]  → a=inicio, b=donde sube a 1, c=límite derecho
        Retorna: rampa ascendente entre a y b, 1 si x >= b
        """
        a, b, c = points
        if x >= a and x <= b:
            return eqVal[1] + x * eqVal[0]
        elif x > b and x <= c:
            return 1
        else:
            return 0

    # ----------------------------------------------------------
    # FUNCIONES DE SALIDA (para defuzzificación)
    # Generan lista discreta de la curva truncada
    # ----------------------------------------------------------

    def trimf_o(self, points, eqVals, x_start, x_end):
        """
        Genera la curva triangular discreta para la salida.
        x_start, x_end: rango del universo de salida
        Retorna: lista con los valores de membresía discretizados
        """
        step = (x_end - x_start) / PRECISION
        a, b, c = points
        graph = []
        x = x_start
        while x <= x_end:
            if x >= a and x < b:
                graph.append(eqVals[0][1] + x * eqVals[0][0])
            elif x >= b and x <= c:
                graph.append(eqVals[1][1] + x * eqVals[1][0])
            else:
                graph.append(0)
            x += step
        return graph

    def tramfL_o(self, points, eqVal, x_start, x_end):
        """
        Genera la curva trapezoidal izquierda discreta para la salida.
        """
        step = (x_end - x_start) / PRECISION
        a, b, _ = points
        graph = []
        x = x_start
        while x <= x_end:
            if x >= a and x <= b:
                graph.append(eqVal[1] + x * eqVal[0])
            elif x < a:
                graph.append(1)
            else:
                graph.append(0)
            x += step
        return graph

    def tramfR_o(self, points, eqVal, x_start, x_end):
        """
        Genera la curva trapezoidal derecha discreta para la salida.
        """
        step = (x_end - x_start) / PRECISION
        a, b, _ = points
        graph = []
        x = x_start
        while x <= x_end:
            if x >= a and x <= b:
                graph.append(eqVal[1] + x * eqVal[0])
            elif x > b:
                graph.append(1)
            else:
                graph.append(0)
            x += step
        return graph


# ============================================================
# CLASE: Conjunto Difuso
# Encapsula un conjunto (ej: "temperatura ALTA")
# ============================================================
class FuzzySet:
    """
    Representa un conjunto difuso individual.
    
    Parámetros:
      name   : nombre del conjunto (ej: "ALTA", "MEDIA")
      shape  : tipo de función → 'tri', 'trapL', 'trapR'
      points : [a, b, c] puntos clave de la función
    
    Ejemplo:
      temp_alta = FuzzySet("ALTA", "trapR", [25, 35, 50])
    """

    SHAPES = ['tri', 'trapL', 'trapR']

    def __init__(self, name, shape, points):
        assert shape in self.SHAPES, f"Forma '{shape}' no válida. Usa: {self.SHAPES}"
        assert len(points) == 3, "Se requieren exactamente 3 puntos [a, b, c]"
        self.name = name
        self.shape = shape
        self.points = points
        self.mf = MembershipFunctions()

        # Pre-calcular ecuaciones de recta
        a, b, c = points
        if shape == 'tri':
            self.eqVals = [
                lineEquation([a, 0], [b, 1]),
                lineEquation([b, 1], [c, 0])
            ]
        elif shape == 'trapL':
            self.eqVals = lineEquation([a, 1], [b, 0])
        elif shape == 'trapR':
            self.eqVals = lineEquation([a, 0], [b, 1])

    def evaluate(self, x):
        """Evalúa el grado de membresía para el valor x."""
        if self.shape == 'tri':
            return self.mf.trimf_i(self.points, self.eqVals, x)
        elif self.shape == 'trapL':
            return self.mf.tramfL_i(self.points, self.eqVals, x)
        elif self.shape == 'trapR':
            return self.mf.tramfR_i(self.points, self.eqVals, x)

    def output_curve(self, x_start, x_end):
        """Genera la curva discreta para defuzzificación."""
        if self.shape == 'tri':
            return self.mf.trimf_o(self.points, self.eqVals, x_start, x_end)
        elif self.shape == 'trapL':
            return self.mf.tramfL_o(self.points, self.eqVals, x_start, x_end)
        elif self.shape == 'trapR':
            return self.mf.tramfR_o(self.points, self.eqVals, x_start, x_end)


# ============================================================
# CLASE: Variable Difusa
# Agrupa varios conjuntos difusos para una variable
# ============================================================
class FuzzyVariable:
    """
    Representa una variable lingüística (ej: temperatura, velocidad).
    Contiene múltiples conjuntos difusos.
    
    Ejemplo:
      temperatura = FuzzyVariable("Temperatura", 0, 100)
      temperatura.add_set(FuzzySet("FRIA",  "trapL", [0,  10, 20]))
      temperatura.add_set(FuzzySet("MEDIA", "tri",   [15, 25, 35]))
      temperatura.add_set(FuzzySet("ALTA",  "trapR", [30, 40, 50]))
    """

    def __init__(self, name, min_val, max_val):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.sets = {}   # dict: nombre → FuzzySet

    def add_set(self, fuzzy_set):
        """Agrega un conjunto difuso a la variable."""
        self.sets[fuzzy_set.name] = fuzzy_set

    def fuzzify(self, x):
        """
        Fuzzifica el valor x.
        Retorna: dict {nombre_conjunto: grado_membresía}
        """
        return {name: fs.evaluate(x) for name, fs in self.sets.items()}

    def output_curves(self):
        """
        Genera todas las curvas discretas de salida.
        Retorna: dict {nombre_conjunto: lista_curva}
        """
        return {
            name: fs.output_curve(self.min_val, self.max_val)
            for name, fs in self.sets.items()
        }


# ============================================================
# FUNCIÓN: Defuzzificación por Centroide
# ============================================================
def centroid(rules_outputs, x_start, x_end):
    """
    Calcula el centroide (centro de gravedad) del área resultante.
    
    rules_outputs : lista de listas (curva discreta por cada regla activada)
    x_start       : inicio del universo de salida
    x_end         : fin del universo de salida
    
    Retorna: valor numérico defuzzificado
    """
    n = len(rules_outputs[0])
    step = (x_end - x_start) / PRECISION

    # Agregar por máximo (operador OR entre reglas)
    total = [
        reduce(lambda a, b: max(a, b), [rules_outputs[i][j] for i in range(len(rules_outputs))])
        for j in range(n)
    ]

    num = sum(total[k] * (x_start + step * k) for k in range(n))
    den = sum(total)

    if den == 0:
        return (x_start + x_end) / 2  # valor neutro si no hay activación
    return num / den


# ============================================================
# CLASE: Controlador Difuso General (Mamdani)
# ============================================================
class FuzzyController:
    """
    Controlador difuso genérico tipo Mamdani.
    
    Uso básico:
      1. Crear variables de entrada y salida con FuzzyVariable
      2. Agregar conjuntos difusos con add_set()
      3. Crear el controlador y agregar variables
      4. Definir reglas como lista de tuplas
      5. Llamar a compute() con los valores de entrada
    
    Ejemplo mínimo (temperatura → velocidad_ventilador):
    
      temp = FuzzyVariable("Temperatura", 0, 50)
      temp.add_set(FuzzySet("BAJA",  "trapL", [0,  15, 25]))
      temp.add_set(FuzzySet("MEDIA", "tri",   [20, 30, 40]))
      temp.add_set(FuzzySet("ALTA",  "trapR", [35, 45, 50]))
    
      fan = FuzzyVariable("Ventilador", 0, 100)
      fan.add_set(FuzzySet("LENTO",  "trapL", [0,  20, 40]))
      fan.add_set(FuzzySet("MEDIO",  "tri",   [30, 50, 70]))
      fan.add_set(FuzzySet("RAPIDO", "trapR", [60, 80, 100]))
    
      ctrl = FuzzyController()
      ctrl.add_input("temp", temp)
      ctrl.add_output("fan", fan)
    
      reglas = [
          ({"temp": "BAJA"},  {"fan": "LENTO"}),
          ({"temp": "MEDIA"}, {"fan": "MEDIO"}),
          ({"temp": "ALTA"},  {"fan": "RAPIDO"}),
      ]
      ctrl.add_rules(reglas)
    
      resultado = ctrl.compute({"temp": 38})
      print(resultado["fan"])  # ej: 82.3
    """

    def __init__(self):
        self.inputs = {}   # nombre → FuzzyVariable
        self.outputs = {}  # nombre → FuzzyVariable
        self.rules = []    # lista de (antecedente_dict, consecuente_dict)

    def add_input(self, name, variable):
        """Agrega una variable de entrada."""
        self.inputs[name] = variable

    def add_output(self, name, variable):
        """Agrega una variable de salida."""
        self.outputs[name] = variable

    def add_rules(self, rules):
        """
        Agrega reglas difusas.
        rules: lista de tuplas (antecedente, consecuente)
          antecedente : dict {nombre_var_entrada: nombre_conjunto}
          consecuente : dict {nombre_var_salida: nombre_conjunto}
        
        Para reglas con AND entre varias entradas, se usa el mínimo.
        """
        self.rules = rules

    def compute(self, input_values, operator='min'):
        """
        Ejecuta el controlador difuso.
        
        input_values : dict {nombre_variable: valor_numérico}
        operator     : 'min' (AND) o 'prod' para el antecedente
        
        Retorna: dict {nombre_variable_salida: valor_defuzzificado}
        """
        # 1. Fuzzificar todas las entradas
        memberships = {}
        for var_name, value in input_values.items():
            memberships[var_name] = self.inputs[var_name].fuzzify(value)

        # 2. Pre-generar curvas de salida
        output_curves = {}
        for out_name, out_var in self.outputs.items():
            output_curves[out_name] = out_var.output_curves()

        # 3. Evaluar reglas y acumular consecuentes
        activated = {out_name: [] for out_name in self.outputs}

        for antecedent, consequent in self.rules:
            # Calcular fuerza del antecedente (AND = mínimo)
            strengths = []
            for var_name, set_name in antecedent.items():
                strengths.append(memberships[var_name].get(set_name, 0))

            if operator == 'min':
                firing = min(strengths) if strengths else 0
            else:  # producto
                firing = 1
                for s in strengths:
                    firing *= s

            if firing == 0:
                continue

            # Truncar curvas de salida con la fuerza de activación
            for out_name, set_name in consequent.items():
                curve = output_curves[out_name].get(set_name, [])
                truncated = [min(firing, v) for v in curve]
                activated[out_name].append(truncated)

        # 4. Defuzzificar por centroide
        result = {}
        for out_name, curves in activated.items():
            out_var = self.outputs[out_name]
            if not curves:
                result[out_name] = (out_var.min_val + out_var.max_val) / 2
            else:
                result[out_name] = centroid(curves, out_var.min_val, out_var.max_val)

        return result
