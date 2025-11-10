Planificación Predictiva de Estrategias de Adelantamiento en Fórmula 1 usando MPC y Modelos Aprendidos

Código del proyecto: OVERTAKE

Integrantes

Alejandro Moreno

Facundo Lella

Descripción

En este proyecto proponemos diseñar y evaluar un Overtake Advisor: un agente de decisión que recomienda cuándo y cómo preparar un adelantamiento en Fórmula 1, considerando diferencias de rendimiento entre equipos, neumáticos, gestión de energía (ERS) y degradación, a partir de modelos aprendidos sobre datos históricos.

El enfoque combina:

Modelo aprendido (Machine Learning supervisado)

A partir de datos públicos de competencias reales (por ejemplo, vía FastF1, que expone información de tiempos de vuelta, telemetría básica, compuestos, paradas y posición en pista). 

Entrenaremos modelos supervisados para estimar:

Pace esperado por vuelta: tiempo de vuelta en función de equipo, compuesto, edad del neumático, fuel aproximado/contexto de carrera.

Degradación: incremento esperado del tiempo de vuelta según vueltas en el stint, compuesto y equipo.

Probabilidad de concretar un adelantamiento: en función de diferencia de ritmo, gap, zona del circuito, compuesto de atacante/defensor.

Estos modelos pueden ser:

Regresión lineal regularizada / regresión polinómica regularizada (para pace y degradación).

Árboles de decisión o Random Forest / Gradient Boosting simples (para probabilidad de adelantamiento).

Regresiones logísticas (para eventos binarios: overtake sí/no).

Control Predictivo Basado en Modelo (MPC)

Usamos estos modelos como “simulador” aproximado del sistema (autos + neumáticos + gaps).

En cada instante, el MPC:

    predice la evolución del gap, ritmo y estado del neumático en un horizonte de H vueltas, bajo distintas decisiones (uso de ERS, ritmo objetivo, vuelta/lugar de intento de adelantamiento),

    optimiza una función de costo que combina:

        tiempo total esperado,

        probabilidad de lograr el adelantamiento,

        penalización por uso excesivo de ERS,

        penalización por degradación y riesgo.

Como salida, el MPC genera un plan de alto nivel, por ejemplo:

ritmo objetivo por vuelta en el horizonte,

porcentaje de ERS a utilizar en cada vuelta/tramo,

vuelta y zona objetivo para el intento de adelantamiento,

probabilidad estimada de éxito del adelantamiento en ese punto.

Así, el Overtake Advisor no solo responde “intentar o no ahora”, sino que propone una secuencia de acciones coherente:

“Subir el ritmo durante N vueltas”

“Gestionar ERS ciertas vueltas”

“Atacar en la vuelta V, en zona Z, con X% de batería, dadas las características del propio auto y del rival”.

Objetivos

Construir un modelo de dinámica de carrera simplificado pero verosímil, específico por equipo/neumático, aprendido de datos.

Implementar un MPC discreto que use ese modelo para planificar estrategias de adelantamiento en un horizonte de varias vueltas.

Comparar el desempeño del MPC frente a:

Estrategias heurísticas (reglas fijas tipo “si DRS y gap < X entonces atacar”).

Un planificador más simple tipo búsqueda (A*) sobre un modelo fijo (opcional como baseline de IA clásica).

Evaluar con métricas cuantitativas la calidad de las estrategias de adelantamiento generadas.

Alcance

Se trabaja con:

Datos históricos de F1 (FastF1 u otra fuente pública) para temporadas recientes.

Un subconjunto acotado de circuitos (por ejemplo: Interlagos, Monza, Bahrain).

Un conjunto limitado de equipos (ej.: Red Bull, Ferrari, Mercedes, McLaren, Alpine), modelados por sus promedios de rendimiento.

El proyecto es una prueba de concepto offline:

No se integra en un simulador de F1 en tiempo real.

No se pretende capturar toda la física ni la complejidad reglamentaria real.

Limitaciones

El modelo aprendido es aproximado:

No considera daños, dirty air complejo, órdenes de equipo, clima cambiante extremo, etc.

El MPC:

Optimiza sobre un horizonte finito y bajo supuestos simplificados.

No garantiza ser óptimo en el mundo real, sino en el modelo.

El análisis se centra en:

“1 vs 1” atacante–defensor directo (sin tráfico múltiple complejo).

Escenarios estáticos de estrategia rival (no se modela un rival también planificador avanzado).

Forma de evaluación (métricas)

La solución se evalúa simulando múltiples escenarios (distintas combinaciones de autos, compuestos, gaps iniciales y pistas) y midiendo:

Tasa de adelantamientos logrados

% de escenarios donde se concreta el overtake dentro del horizonte planificado.

Ganancia neta de tiempo

Diferencia de tiempo total vs. estrategias base:

baseline conservador: no forzar adelantamiento.

baseline greedy: atacar siempre que haya DRS y gap < umbral.

Eficiencia en el uso de recursos

Consumo medio de ERS vs. ganancia lograda.

Degradación extra del neumático inducida por el plan vs. referencia.

Calidad de las predicciones del modelo aprendido

Error en tiempo de vuelta (MAE/RMSE).

Error/calibración de probabilidad de adelantamiento (log-loss, Brier score).

Robustez

Sensibilidad del plan a pequeñas variaciones en datos (ruido en pace, cambios leves en gap).

Estos indicadores permiten mostrar de manera medible el aporte del enfoque MPC + ML frente a estrategias simples.

Justificación

El problema de decidir cómo y cuándo adelantar en F1:

Es un problema de decisión secuencial bajo restricciones:

Recursos limitados (ERS, neumáticos).

Dinámica compleja (gap evoluciona con el ritmo de ambos autos).

Efectos acumulativos (degradación, temperatura).

No basta con una regla fija:

La mejor decisión actual depende de las consecuencias en varias vueltas hacia adelante.

Estrategias ingenuas (greedy) pueden malgastar ERS o degradar neumáticos sin concretar el adelantamiento.

Por eso tiene sentido aplicar técnicas de Inteligencia Artificial:

Aprendizaje Supervisado

Para aprender funciones no triviales a partir de datos reales:

tiempo de vuelta en función de contexto,

probabilidad de overtake según condiciones.

Son modelos típicos de IA:

regresiones regularizadas, árboles, ensembles, etc.

Planificación Óptima / MPC (AI de decisión)

El MPC se comporta como un agente racional:

usa un modelo del entorno (aprendido),

predice consecuencias futuras,

elige la secuencia de controles que optimiza una función de utilidad.

Es análogo a otros enfoques de IA usados en robótica, vehículos autónomos o control inteligente.

Comparación con métodos clásicos de IA

Podemos contrastar con:

un planificador tipo A* en espacio de estados (búsqueda informada),

o reglas heurísticas,

mostrando cómo la combinación Modelo aprendido + MPC captura mejor la naturaleza secuencial y estocástica del problema.

En síntesis, el proyecto no es solo “simular vueltas”, sino:

aprender modelos a partir de datos (componente de aprendizaje),

usar esos modelos para planificar decisiones óptimas (componente de control predictivo / IA),

evaluarlos cuantitativamente frente a alternativas más simples.

Listado de actividades a realizar

Relevamiento y delimitación del problema

Definir claramente el escenario: 1 atacante vs 1 defensor, mismo stint.

Seleccionar circuitos y equipos a considerar.

Definir variables relevantes: equipo, compuesto, edad de goma, gap, DRS, etc.

Obtención y preparación de datos

Descarga de datos históricos con FastF1 (u otra fuente equivalente): tiempos de vuelta, compuestos, stints, posiciones. 
theoehrly.github.io

Limpieza y construcción de dataset:

features por vuelta/stint,

marcadores de eventos de adelantamiento simples (cambio de posición entre vueltas consecutivas).

Modelado de funciones dinámicas (aprendizaje supervisado)

Entrenar y comparar modelos para:

Tiempo de vuelta: regresión lineal regularizada y/o árboles.

Degradación: modelo incremental sobre stint.

Probabilidad de adelantamiento: regresión logística / árbol.

Seleccionar modelos según desempeño (MAE, RMSE, AUC, Brier).

Diseño del entorno simulado

Implementar un simulador simplificado que:

use los modelos aprendidos para predecir:

pace del atacante y defensor,

evolución del gap,

probabilidad de éxito de un intento en cada zona.

permita aplicar decisiones:

ritmo objetivo (modo push/neutral/save),

uso de ERS,

decisión de intentar o no el adelantamiento.

Implementación del MPC

Definir horizonte de planificación (ej. 3–5 vueltas).

Definir función de costo que combine:

tiempo total,

penalización por ERS y degradación,

recompensa por concretar el adelantamiento.

Implementar el algoritmo de optimización (búsqueda en árbol, recocido, o enumeración podada) que calcule el mejor plan sobre ese horizonte.

Integrar el MPC con el simulador (receding horizon: aplicar primera acción, actualizar, replanificar).

Baselines y comparación

Implementar al menos:

Estrategia greedy (reglas simples).

(Opcional) A* como planificador sobre un modelo fijo.

Definir escenarios de prueba (distintos teams gaps/compuestos).

Evaluación experimental

Ejecutar múltiples simulaciones por escenario y estrategia.

Medir métricas definidas:

tasa de overtake,

ganancia neta de tiempo,

uso de ERS,

degradación adicional.

Analizar sensibilidad a ruido y errores del modelo.

Redacción del informe final (posterior al anteproyecto)

Describir formalmente:

modelos de aprendizaje usados,

formulación matemática del MPC,

resultados experimentales,

discusión de limitaciones y posibles mejoras (p.ej. RL, modelos más ricos).

Bibliografía (a completar en el informe final)

Documentación de FastF1. 
theoehrly.github.io

Material de la cátedra de IA I (búsqueda, planificación, aprendizaje).

Referencias introductorias de MPC y control predictivo aplicado a vehículos.