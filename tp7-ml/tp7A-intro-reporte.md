1-
    a-
    El flexible: mejor.
    Con muchos datos y pocos predictores, un método flexible puede bajar el sesgo sin que la varianza se dispare. Suelen ganar modelos más complejos bien ajustados por CV.

    b-
    Flexible: peor.
    Con más variables que observaciones, los métodos flexibles tienen varianza altísima y sobreajustan con facilidad.

    c-
    Flexible: mejor.
    Si la verdad subyacente es muy no lineal, los métodos inflexibles sufren alto sesgo. La flexibilidad permite capturar la estructura y reducir sesgo (con control de complejidad).

    d-
    Flexible: peor.
    Con mucho ruido, los modelos flexibles tienden a perseguir el ruido (sobreajuste), inflando la varianza y empeorando el error de prueba. 

2-
    a-
    Tipo: Regresión (el salario es cuantitativo).
    Interés principal: Inferencia (entender qué factores afectan el salario).
    n: 500 empresas.
    p: 3 predictores: ganancias, número de empleados, industria (categórica; se codifica con dummies).

    b-
    Tipo: Clasificación (éxito/fracaso es cualitativo).
    Interés principal: Predicción (anticipar si el nuevo producto será éxito o fracaso).
    n: 20 productos históricos.
    p: 13 predictores = precio + presupuesto de marketing + precio de la competencia + otras 10 variables.

    c-
    Tipo: Regresión (la respuesta es un porcentaje continuo).
    Interés principal: Predicción (pronosticar el cambio del tipo de cambio).
    n: ≈52 observaciones (semanas de 2021).
    p: 3 predictores: % cambio en mercado estadounidense, británico y alemán.

3-
Ventajas de un enfoque muy flexible:
    Menor sesgo: puede aproximar funciones complejas y reducir error sistemático.
    Alto potencial predictivo: si hay muchos datos y buena validación, suele lograr menor error de prueba.
    Adaptabilidad: permite incorporar features ricas.
    Automatización de especificación: no requiere definir a mano la forma funcional.

Desventajas de un enfoque muy flexible:
    Mayor varianza / sobreajuste: si n es limitado, el modelo puede “memorizar” ruido.
    Menor interpretabilidad: cuesta responder ¿por qué?; difícil comunicar efectos marginales.
    Mayor costo computacional y tuning: necesita hiperparámetros (profundidad, k, λ, número de árboles) y validación cuidadosa.
    Menor robustez fuera del soporte: peor extrapolación; se descompone lejos de los datos.
    Riesgo de inestabilidad: pequeñas variaciones en datos pueden cambiar la predicción.

Ventajas de un enfoque menos flexible
    Más interpretable: coeficientes, efectos marginales, intervalos.
    Menor varianza: más estable con pocos datos o ruido alto.
    Rápido y simple de sintonizar: menos hiperparámetros, menor costo computacional.
    Mejor extrapolación local: la linealidad da un comportamiento más predecible fuera de la muestra.
    Regularización y diagnóstico claros: se entienden bien supuestos y violaciones (multicolinealidad, heterocedasticidad, etc.).

Desventajas de un enfoque menos flexible
    Mayor sesgo: si la verdad es no lineal, el modelo simple no alcanza.
    Tope de rendimiento predictivo: aun con muchos datos, puede quedarse corto por subajuste.

¿Cuándo preferir más flexibilidad?
    Relación altamente no lineal o con interacciones importantes.
    Muestras grandes (n grande) y p moderado, o buen control de complejidad (regularización, early stopping).
    Objetivo: predicción.
    Bajo ruido (o buen preprocesamiento) y posibilidad de validación cruzada sólida.
    Dispones de cómputo y tiempo para tuning y calibración.

¿Cuándo preferir menos flexibilidad?
    Inferencia es prioritaria (cuantificar efectos, contrastar hipótesis).
    n pequeño, ruido alto o p≫n sin fuerte regularización previa. Se busca estabilidad.
    Recursos limitados (tiempo/cómputo) o necesidad de modelos robustos y reproducibles rápidamente.
    Riesgo regulatorio/operativo: se exige auditabilidad y transparencia.
    Se requiere extrapolar o fijar políticas con reglas simples.

4-
Paramétrico
    Supone una forma funcional fija para f(X) con un número finito de parámetros θ (tamaño fijo, no crece con n).
    Tareas: (1) elegir la forma (modelo), (2) ajustar θ (MLE, mínimos cuadrados, ERM), (3) validar/regularizar.

No paramétrico:
    Evita asumir una forma cerrada para f; permite que la complejidad crezca con los datos.
    Aprende f “desde los datos” con mayor flexibilidad; requiere hiperparámetros que controlan suavizado/variancia.

Ventajas del enfoque paramétrico:
    Datos-eficiente: con n pequeño suele rendir mejor (menos varianza).
    Interpretabilidad: coeficientes, efectos marginales, intervalos; fácil comunicar e inferir.
    Cómputo y despliegue: entrenar y predecir es rápido; footprint bajo.
    Extrapolación controlada: la forma (lineal, logística) define un comportamiento fuera del soporte.

Desventajas del enfoque paramétrico:
    Riesgo de mala especificación: si la verdadera relación es no lineal -> alto sesgo.
    Rigidez: para capturar no linealidades hay que ingenierizar features (polinomios, interacciones, splines) o pasar a semiparamétricos.

Ventajas del enfoque no paramétrico:
    Bajo sesgo potencial: puede capturar no linealidades e interacciones complejas sin preespecificarlas.
    Alto techo predictivo: con buen tuning/validación y muchos datos, puede lograr menor error de prueba.
    Automatiza la forma de f: menos “manualidad” para conjeturar transformaciones.

Desventajas del enfoque no paramétrico:
    Mayor varianza / sobreajuste: necesita más datos; sensible a hiperparámetros (profundidad, k, bandwidth, número de árboles…).
    Menor interpretabilidad: cuesta explicar “el porqué”; suele requerir explicadores pos-hoc (SHAP, PDP).
    Costo computacional: entrenamiento y/o predicción más pesados; escalado menos trivial.
    Extrapolación pobre: muchos métodos son locales y se degradan fuera del soporte observado.

5-
    a-
    obs 1: d=3
    obs 2: d=2
    obs 3: d=3,162
    obs 4: d=2,236
    obs 5: d=1,414
    obs 6: d=1,732

    b-
    Como el más cercano es la Obs 5 (Verde) entonces la predicción es verde.

    c-
    Como dos de los 3 más cercanos son Rojos, entonces la predicción es rojo.

    d-
    Conviene un K pequeño (modelo más flexible): sigue mejor contornos no lineales (bajo sesgo). Un K grande promedia sobre regiones amplias, suaviza demasiado y eleva el sesgo, perdiendo la forma no lineal del límite. Por eso, para fronteras muy no lineales, mejor K chico.