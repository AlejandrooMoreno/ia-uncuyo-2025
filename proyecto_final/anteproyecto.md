# **Planificación Predictiva de Estrategias de Adelantamiento en Fórmula 1 usando MPC y Modelos Aprendidos**

**Código del proyecto:** `OVERTAKE`  

**Integrantes:**  
- **Alejandro Moreno**  
- **Facundo Lella**

---

## Descripción

En este proyecto proponemos diseñar y evaluar un **Overtake Advisor**: un agente que recomienda **cuándo** y **cómo** intentar un adelantamiento en un escenario de Fórmula 1, utilizando:

- **Modelos predictivos aprendidos** (aprendizaje supervisado clásico) para estimar:
  - tiempos de vuelta,
  - degradación de neumáticos,
  - efecto del uso de energía (ERS),
  - probabilidad de éxito de un intento de adelantamiento,
  - impacto relativo entre distintos equipos (ej. McLaren vs Mercedes vs Ferrari, etc.).
- Un esquema de **Control Predictivo Basado en Modelo (MPC)** como **planificador**, que:
  - simula la evolución del duelo atacante–defensor en un **horizonte de varias vueltas**, y
  - selecciona la secuencia óptima de decisiones (ritmo, uso de ERS, vuelta y zona para el intento).

El sistema no se limita a decidir “intentar o no intentar ahora”, sino que genera una **planificación detallada**, por ejemplo:

- ritmo objetivo por vuelta (time targets),
- porcentaje de batería a utilizar en cada vuelta,
- degradación esperada del neumático,
- vuelta y punto de la pista recomendados para el adelantamiento,
- probabilidad estimada de concretar el sobrepaso bajo ese plan.

La propuesta es construir una **prueba de concepto medible**, no una herramienta de ingeniería lista para pista real. Vamos a trabajar con:
- **datos históricos** y/o **datos simulados realistas** basados en información pública (tiempos de vuelta, compuestos, stints, zonas DRS, etc.),
- escenarios simplificados donde se comparan **distintas políticas de decisión**.

---

## Objetivos

### Objetivo general

Desarrollar y evaluar un agente de recomendación de adelantamientos en Fórmula 1 basado en **Model Predictive Control (MPC)** apoyado en **modelos de predicción aprendidos**, analizando su desempeño frente a estrategias más simples.

### Objetivos específicos

1. **Modelar el duelo atacante–defensor** como un sistema dinámico con:
   - variables de estado: gap, ritmo relativo, compuesto, edad de neumático, energía disponible, zona de pista, equipo de cada auto, etc.
   - entradas de control del atacante: uso de ERS, agresividad/ritmo por vuelta, decisión de intento de adelantamiento.
2. **Entrenar modelos supervisados** (a partir de datos históricos o simulados) para:
   - predecir tiempo de vuelta en función de compuesto, edad del neumático, nivel de push/ERS y características del auto/equipo,
   - estimar probabilidad de éxito de un adelantamiento dado el contexto (gap, DRS, diferencia de ritmo, equipos involucrados).
3. **Diseñar un esquema de MPC** que:
   - use los modelos aprendidos como “modelo del entorno”,
   - explore distintas secuencias de decisiones en un horizonte de varias vueltas,
   - seleccione la que maximiza una función de rendimiento.
4. **Comparar cuantitativamente** el MPC contra:
   - estrategias estáticas (ej. siempre intentar si hay DRS y gap < X),
   - reglas heurísticas simples (basadas sólo en gap y compuesto).
5. **Analizar limitaciones**, sensibilidad a errores de modelo y posibles extensiones (por ejemplo, integración con aprendizaje por refuerzo en trabajos futuros).

---

## Alcance

El proyecto se enfoca en:

- Un **escenario 1 vs 1** (un atacante y un defensor).
- Datos a nivel:
  - tiempos de vuelta,
  - stints (compuesto + vueltas),
  - diferencias promedio entre equipos,
  - información básica de pista: longitud, zonas DRS, sectores.
- Modelos supervisados relativamente simples (por ejemplo, **regresión lineal regularizada**, **árboles de decisión** o **Random Forest** según el caso) para capturar:
  - relación entre ritmo y degradación,
  - impacto del uso de ERS,
  - diferencias de performance entre equipos.
- Un MPC formulado en forma discretizada (por vueltas o sectores), apto para ser implementado y resuelto dentro del alcance de la materia.

No se busca modelar:
- dinámica completa del vehículo (aerodinámica detallada, simulación física compleja),
- múltiples autos simultáneos en tráfico denso,
- toda la estrategia integral de carrera (stops, safety car, clima, etc.).

Es una **prueba de concepto controlada**, centrada en **cómo la combinación “modelo aprendido + MPC” puede planificar un adelantamiento mejor que reglas simples**.

---

## Limitaciones

- **Datos incompletos o ruidosos:** los modelos dependerán de la calidad de los datos históricos o simulados (telemetría pública, tiempos por vuelta, etc.).
- **Simplificaciones fuertes:** se aproximan efectos complejos (slipstream, DRS, degradación, temperatura) con modelos simples.
- **Escenario restringido:** sólo dos autos (atacante/defensor) y horizonte corto de vueltas; no se cubren todas las situaciones de carrera reales.
- **No hay garantía de validez absoluta en el mundo real:** es un entorno de evaluación académica.

---

## Forma de evaluación (métricas)

La performance del enfoque se medirá comparando **MPC + modelos aprendidos** vs. políticas base:

1. **Tasa de adelantamientos exitosos**:
   - porcentaje de planes que terminan en un adelantamiento concreto dentro del horizonte.
2. **Tiempo total de duelo**:
   - tiempo acumulado hasta el adelantamiento o fin del horizonte;
   - comparación con políticas heurísticas.
3. **Uso de recursos**:
   - consumo total de ERS,
   - degradación estimada del neumático.
4. **Eficiencia de intentos**:
   - cantidad de intentos fallidos vs. exitosos.
5. **Consistencia entre escenarios**:
   - robustez del MPC ante cambios en:
     - diferencia de rendimiento entre equipos,
     - compuesto,
     - edad de la goma,
     - configuraciones de pista.

El objetivo es demostrar que el MPC, apoyado en modelos aprendidos, **planifica adelantamientos más eficientes y realistas** que estrategias simplistas, bajo las mismas condiciones iniciales.

---

## Justificación (¿Por qué IA?)

Un enfoque puramente “hardcodeado” o determinista es insuficiente porque:

- La dinámica del problema es **compleja, multivariable y estocástica**:
  - depende de la interacción entre autos, de la pista, neumáticos, energía, etc.
- Las relaciones entre:
  - ritmo ↔ desgaste ↔ ERS ↔ probabilidad de adelantamiento  
  no son triviales ni lineales; es razonable **aprenderlas a partir de datos**.
- El MPC necesita un **modelo del entorno** para simular futuros posibles:
  - usar **modelos de aprendizaje supervisado** para aproximar este entorno encaja directamente con técnicas vistas en la materia.
- El esquema completo combina dos componentes de IA:
  1. **Aprendizaje supervisado** para ajustar modelos de:
     - tiempo de vuelta,
     - degradación,
     - probabilidad de adelantamiento.
  2. **Planificación/optimización sobre modelo** (MPC) para decidir la mejor secuencia de acciones bajo restricciones.

Así, el proyecto no es sólo simulación, sino una **aplicación integrada de aprendizaje automático + toma de decisiones inteligente**, alineada con los contenidos de **Inteligencia Artificial I**.

---

## Listado de actividades

1. **Relevamiento y preparación de datos**
   - Identificar fuentes (datos públicos de F1, librerías como FastF1, etc.).
   - Extraer:
     - tiempos de vuelta,
     - compuestos utilizados,
     - duración de stints,
     - diferencias promedio entre equipos,
     - información básica de cada pista (sectores, zonas DRS).
   - Generar, si es necesario, **escenarios simulados** calibrados con esos datos.

2. **Definición del modelo dinámico simplificado**
   - Definir variables de estado (gap, pace relativo, ERS, compuesto, edad de neumático, etc.).
   - Definir variables de control (uso de ERS por vuelta, target de tiempo, decisión de intento).
   - Especificar ecuaciones aproximadas que relacionan estado, control y evolución del sistema.

3. **Entrenamiento de modelos supervisados**
   - Ajustar:
     - modelo de **tiempo de vuelta** (ej. regresión lineal regularizada / árboles),
     - modelo de **degradación de neumático**,
     - modelo de **probabilidad de adelantamiento** según contexto (gap, DRS, equipos).
   - Evaluar cada modelo con métricas estándar (MAE/RMSE, accuracy/calibración para probabilidad).

4. **Formulación del MPC**
   - Definir el **horizonte de planificación** (ej. 3–5 vueltas).
   - Definir la **función objetivo**:
     - maximizar probabilidad de adelantamiento,
     - minimizar tiempo total,
     - penalizar consumo excesivo de ERS y degradación.
   - Incluir restricciones:
     - límite de ERS disponible,
     - límites razonables de ritmo,
     - condiciones para un intento válido (DRS, gap, etc.).

5. **Implementación del MPC**
   - Implementar el algoritmo que:
     - simula múltiples secuencias de control usando los modelos aprendidos,
     - evalúa su costo/beneficio,
     - selecciona el plan de control óptimo para el horizonte.
   - Generar como salida:
     - plan de uso de ERS,
     - tiempos objetivo por vuelta,
     - vuelta y ubicación recomendada para el intento,
     - probabilidad estimada de éxito.

6. **Definición de políticas base (baselines)**
   - Ejemplos:
     - política “intentar siempre con DRS si gap < X”,
     - política de uso fijo de ERS,
     - otras reglas simples.

7. **Experimentación y evaluación**
   - Ejecutar múltiples escenarios:
     - distintos equipos (diferentes performances),
     - distintos compuestos y edades,
     - diferentes gaps iniciales.
   - Comparar:
     - tasa de adelantamientos,
     - eficiencia en uso de recursos,
     - tiempos de duelo.
   - Analizar sensibilidad del MPC ante errores en los modelos aprendidos.

8. **Redacción del informe final**
   - Describir:
     - modelo del problema,
     - modelos aprendidos,
     - formulación del MPC,
     - resultados experimentales,
     - limitaciones y líneas futuras (ej. RL, modelos más ricos).

---

## Bibliografía inicial (a ampliar en el informe final)

- Documentación de FastF1 (telemetría y datos históricos de F1).  
  `https://theoehrly.github.io/Fast-F1/`
- Material de la cátedra de **Inteligencia Artificial I** (búsqueda, planificación, aprendizaje supervisado).

---
