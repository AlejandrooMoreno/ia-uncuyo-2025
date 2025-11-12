# **Anteproyecto – Inteligencia Artificial I**

## **Título del proyecto**
**Overtake Advisor: un sistema inteligente de recomendación de adelantamientos en Fórmula 1 mediante aprendizaje por refuerzo**

## **Código del proyecto**
**OVERTAKE**

## **Integrantes**
- Facundo Lella y Alejandro Moreno

---

## **Descripción**

**Overtake Advisor** propone el desarrollo de una prueba de concepto basada en aprendizaje por refuerzo  para determinar cuándo y dónde realizar un adelantamiento en una carrera de Fórmula 1, utilizando datos reales de telemetría obtenidos a través de la librería [FastF1](https://docs.fastf1.dev/).

El objetivo principal es entrenar un agente inteligente capaz de detectar momentos óptimos de adelantamiento considerando el contexto dinámico de la pista (posición del rival, velocidad, distancia, DRS, curva actual, etc.) y maximizar la probabilidad de éxito sin comprometer la carrera.

El sistema actuará como un **asesor virtual**, recomendando en tiempo real si adelantar**, esperar o preparar el adelantamiento en las siguientes curvas o sectores. No se busca implementar un simulador físico ni una interfaz gráfica final, sino demostrar el comportamiento inteligente emergente del modelo entrenado bajo distintas condiciones de carrera.

### **Objetivos**
El proyecto tiene como objetivos desarrollar un agente heurístico basado en reglas fijas y, además, implementar un modelo de aprendizaje por refuerzo utilizando Q-Learning, capaz de adaptarse a estados dinámicos de carrera.

### **Alcance**
Se implementará una simulación reducida en la que el agente será entrenado utilizando datos históricos y escenarios generados a partir de la telemetría obtenida mediante la librería FastF1. 

### **Limitaciones**
El entorno de simulación será discreto y simplificado, dividiendo la pista en sectores y discretizando variables como velocidades y distancias. El modelo no estará diseñado para planificar estrategias completas de carrera, sino únicamente para tomar decisiones locales relacionadas con maniobras de adelantamiento.


### **Métricas**
El rendimiento del agente se evaluará considerando episodios que comprenden entre una a diez vueltas. Se analizará la tasa de adelantamientos exitosos expresada en porcentaje, el tiempo promedio necesario para completar un adelantamiento y el tiempo promedio perdido después de un intento fallido.

---

## **Justificación**

El problema del **momento óptimo para adelantar en F1** es inherentemente **no determinista, dinámico y dependiente del contexto**, por lo que **no puede resolverse eficazmente mediante reglas fijas o algoritmos deterministas**.  
Las decisiones dependen de múltiples factores cambiantes (distancia al rival, energía del DRS, velocidad, ángulo de curva, grip del neumático, etc.) y del resultado de acciones anteriores.

Por ello, se propone el uso de **algoritmos de Inteligencia Artificial basados en Aprendizaje por Refuerzo (RL)**, en los cuales un agente aprende por experiencia directa a maximizar su recompensa acumulada mediante la interacción con un entorno.  
En particular, **Q-Learning** que permite que el agente aprenda una política de decisión sin requerir un modelo exacto del entorno físico, lo que lo hace ideal para escenarios de conducción simulada.

El uso de IA, y no de programación tradicional, se justifica en que **el espacio de estados y acciones es altamente complejo y variable**, y la **estrategia óptima no puede derivarse mediante un conjunto finito de reglas lógicas predefinidas**.

---

## **Listado de actividades**

| Nº | Actividad | Duración estimada |
|----|------------|------------------|
| 1 | Recopilación de bibliografía y simulación F1. | 7 días |
| 2 | Obtención, entendimiento y limpieza de datos de telemetría (FastF1). | 4 días |
| 3 | Definición del entorno de simulación y estados posibles (velocidad, distancia, DRS, sector, etc.). | 3 días |
| 4 | Implementación del entorno simplificado para entrenamiento del agente. | 6 días |
| 5 | Implementación del algoritmo de Q-Learning | 7 días |
| 6 | Diseño de la función de recompensa y parámetros de entrenamiento. | 3 días |
| 7 | Entrenamiento del agente y registro de métricas (recompensa promedio, tasa de éxito). | 3 días |
| 8 | Validación del modelo y análisis de resultados. | 3 días |
| 9 | Redacción del informe final con resultados y conclusiones. | 3 días |

## ** GANTT **
<img width="2800" height="1000" alt="gantt_f1_qlearning" src="https://github.com/user-attachments/assets/e2625c91-cabf-4b78-b4c6-19f5bec50b47" />


## **Adicional**
Como propuesta adicional investigaremos e intentaremos implementar MPC (Model Predictive Control) es una técnica de control que utiliza un modelo del sistema para predecir su comportamiento futuro y optimizar las acciones de control en tiempo real, perfecto para este problema.

---
Referencias

FastF1: API de análisis de datos de Fórmula 1 — https://docs.fastf1.dev

https://medium.com/data-science/reinforcement-learning-for-formula-1-race-strategy-7f29c966472a

Bibliografía y diapositivas otorgadas por la cátedra.


