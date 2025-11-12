i) Preprocesamiento
Se parseó la fecha de última modificación y se generaron variables temporales (año, mes, día, etc.) y una medida continua de días transcurridos.
Se transformaron variables ordinales (altura, diámetro) a valores numéricos.
Se crearon variables geométricas/espaciales simples usando latitud, longitud y combinaciones con medidas del árbol.
Las variables categóricas nominales (como especie y sección) se codificaron con one-hot encoding.
Se eliminaron columnas originales redundantes (fecha sin procesar, categorías originales) y se estandarizaron las variables numéricas (media 0, desvío 1).

ii) Resultados en validación
Se usó validación cruzada estratificada (5 folds) con AUC ROC como métrica.
Se reporta el AUC promedio sobre los folds como estimación del desempeño del modelo.
Fold 1 AUC: 0.7519
Fold 2 AUC: 0.7348
Fold 3 AUC: 0.7380
Fold 4 AUC: 0.7553
Fold 5 AUC: 0.7534
Mean CV AUC: 0.7467 (+/- 0.0085)
Train AUC: 0.7493

iii) Resultados en Kaggle
0.74638

iv) Descripción del algoritmo
Se utilizó una regresión logística binaria con regularización L2.
El modelo toma cada árbol, lo representa como un vector de variables numéricas (medidas, codificación de especie, ubicación, etc.) y calcula un puntaje lineal: z=w⋅x+b
donde w son los pesos del modelo, x las características del árbol y b un término independiente. Ese puntaje no se usa directamente como decisión, sino que se pasa por la función sigmoide:

P(y=1∣x)=σ(z)=1/(1+e^-z)
	​
que lo transforma en una probabilidad entre 0 y 1 de que el árbol pertenezca a la clase “inclinación peligrosa”.

Para ajustar los parámetros w y b, el algoritmo minimiza la pérdida logística (log-loss), que penaliza más fuerte las predicciones muy seguras pero incorrectas. Sobre esa función de pérdida se agrega un término de regularización L2 sobre los pesos (λ∥w∥^2), que evita que el modelo dependa en exceso de alguna variable individual y ayuda a reducir el sobreajuste. La optimización se resuelve numéricamente usando el método L-BFGS-B, que aprovecha el gradiente de la función de costo para encontrar eficientemente los parámetros que mejor explican los datos de entrenamiento.

En la práctica, esto significa que el modelo aprende cuánto “pesa” cada característica en el riesgo de inclinación peligrosa, de forma global y suavizada, y produce como salida probabilidades calibradas que luego se utilizan directamente para la evaluación en la competencia.