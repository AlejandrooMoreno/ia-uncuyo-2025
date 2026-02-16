import numpy as np
import random

# --- DEFINICIÓN DE ACCIONES ---
# 0: Overtake   (Ataque total, máximo riesgo y consumo)
# 1: Push       (Ritmo fuerte, consumo alto)
# 2: Maintain   (Ritmo de carrera, gestión equilibrada)
# 3: Lift&Coast (Ahorro de energía, pérdida leve de tiempo)
# 4: Cool Tires (Enfriar gomas, ritmo lento)
ACCIONES = [0, 1, 2, 3, 4]

class Auto:
    def __init__(self, nombre, rendimiento_base):
        self.nombre = nombre
        # Rendimiento: 1.0 es la referencia. +/- 0.01 es mucha diferencia.
        self.rendimiento = rendimiento_base 
        self.bateria = 100.0    # 0-100
        self.neumaticos = 100.0 # 0-100 (Vida útil)
        
    def reset(self):
        self.bateria = 100.0
        self.neumaticos = 100.0

class F1Env:
    def __init__(self, mapa_pista, auto_agente, auto_rival):
        self.track = mapa_pista # Lista de sectores cargada del JSON
        self.agent = auto_agente
        self.rival = auto_rival
        
        # Variables de estado
        self.sector_index = 0
        self.vuelta = 0
        self.gap_segundos = 0.5 
        self.game_over = False

    def reset(self):
        """Reinicia la carrera para un nuevo episodio"""
        self.agent.reset()
        self.rival.reset()
        
        self.sector_index = 0
        self.vuelta = 0
        
        # Iniciamos con gap aleatorio para entrenar variedad de situaciones
        self.gap_segundos = random.uniform(0.2, 1.8)
        self.game_over = False
        
        return self._obtener_estado()

    def step(self, accion):
        """
        Avanza la simulación un sector.
        """
        sector_actual = self.track[self.sector_index]
        limite_fisico = sector_actual['max_speed_kmh'] # Techo de velocidad
        prob_adelantar = sector_actual['prob_adelantar'] # Dificultad del sector (1.0 = Recta, 0.1 = Mónaco)
        tipo_sector = sector_actual['tipo']

        # =========================================
        # 1. FÍSICA DEL AGENTE (TU AUTO)
        # =========================================
        factor_velocidad = 1.0
        gasto_bateria = 0.0
        gasto_goma = 0.0
        recompensa_extra = 0
        
        if accion == 0: # OVERTAKE
            # Lógica de Probabilidad: ¿Cabe el auto aquí?
            dice_roll = random.random()
            
            if dice_roll > prob_adelantar:
                # FALLO: Intentaste pasar donde no se puede
                factor_velocidad = 0.90 # Frenazo por cerrar la puerta
                gasto_bateria = 15.0    # Gastaste energía igual
                gasto_goma = 0.4        # Plano en el neumático por bloquear
                recompensa_extra = -20  # Pequeño castigo pedagógico
            else:
                # ÉXITO: Hay hueco
                factor_velocidad = 1.05 # Boost de velocidad
                gasto_bateria = 15.0
                gasto_goma = 0.25
                
        elif accion == 1: # PUSH
            factor_velocidad = 1.02
            gasto_bateria = 5.0
            gasto_goma = 0.15
        elif accion == 2: # MAINTAIN
            factor_velocidad = 1.00
            gasto_bateria = -2.0    # Recuperación leve
            gasto_goma = 0.10
        elif accion == 3: # LIFT & COAST
            factor_velocidad = 0.95
            gasto_bateria = -10.0   # Recarga fuerte
            gasto_goma = 0.05
        elif accion == 4: # COOL TIRES
            factor_velocidad = 0.90
            gasto_bateria = -5.0
            gasto_goma = -0.10       # Recupera un poco de 'vida' (baja temperatura)

        # Penalización: Si no hay batería, el motor eléctrico corta
        if self.agent.bateria <= 5 and accion < 2:
            factor_velocidad = 0.95 

        # --- FÍSICA DE NEUMÁTICOS MEJORADA (REALISTA) ---
        
        # FASE 1: Degradación Lineal (Desgaste normal)
        # Incluso si la goma está "bien" (entre 100% y 40%), va perdiendo grip.
        # Por cada 10% de desgaste, pierde 0.5% de velocidad (aprox 0.5s en una vuelta de 100s).
        desgaste_total = (100.0 - self.agent.neumaticos)
        penalizacion_lineal = desgaste_total * 0.0005 # Factor pequeño constante
        
        # FASE 2: El Abismo (The Cliff)
        # Si baja del 40%, se suma una penalización extra brutal.
        penalizacion_cliff = 0.0
        if self.agent.neumaticos < 40:
            # Fórmula exponencial: cuanto más baja de 40, más inmanejable es.
            penalizacion_cliff = (40 - self.agent.neumaticos) * 0.003

        # Penalización Total = La suma de ambas
        penalizacion_total_goma = penalizacion_lineal + penalizacion_cliff
        
        # Aplicamos al factor de velocidad
        # Ahora el 'factor_velocidad' (que viene de la acción) se reduce por el estado del neumático
        factor_velocidad_final = factor_velocidad - penalizacion_total_goma
        
        # Velocidad Agente
        vel_agente = limite_fisico * self.agent.rendimiento * factor_velocidad_final

        # =========================================
        # 2. FÍSICA DEL RIVAL (CON DESGASTE REALISTA)
        # =========================================
        # FASE 1: Degradación Lineal (Desgaste normal)
        # Incluso si la goma está "bien" (entre 100% y 40%), va perdiendo grip.
        # Por cada 10% de desgaste, pierde 0.5% de velocidad (aprox 0.5s en una vuelta de 100s).
        desgaste_total = (100.0 - self.rival.neumaticos)
        penalizacion_lineal = desgaste_total * 0.0005 # Factor pequeño constante
        
        # FASE 2: El Abismo (The Cliff)
        # Si baja del 40%, se suma una penalización extra brutal.
        penalizacion_cliff = 0.0
        if self.rival.neumaticos < 40:
            # Fórmula exponencial: cuanto más baja de 40, más inmanejable es.
            penalizacion_cliff = (40 - self.rival.neumaticos) * 0.003

        # Penalización Total = La suma de ambas
        penalizacion_total_goma = penalizacion_lineal + penalizacion_cliff
        
        # Aplicamos al factor de velocidad
        # Ahora el 'factor_velocidad' (que viene de la acción) se reduce por el estado del neumático
        factor_velocidad_final = 1 - penalizacion_total_goma

        vel_rival = limite_fisico * self.rival.rendimiento * factor_velocidad_final

        # El rival gasta goma dependiendo del sector
        desgaste_rival_base = 1.0
        if tipo_sector == 'CURVA':
            desgaste_rival_base = 0.18 # Las curvas gastan más al rival también
        elif tipo_sector == 'FRENADA':
            desgaste_rival_base = 0.12
        else:
            desgaste_rival_base = 0.05 # Rectas gastan poco
            
        self.rival.neumaticos -= desgaste_rival_base

        # =========================================
        # 3. SEGURIDAD Y CÁLCULOS
        # =========================================
        # Safety Check: Salida de pista en curvas
        if vel_agente > limite_fisico * 1.15: 
            self.game_over = True
            return self._obtener_estado(), -500, True, "CRASH"

        # Cálculo de Tiempo (Sectores de 100m aprox)
        dist = 0.1
        t_agente = dist / (max(vel_agente, 10) / 3600)
        t_rival = dist / (max(vel_rival, 10) / 3600)
        
        delta = t_rival - t_agente # Positivo = Recortaste tiempo
        self.gap_segundos -= delta

        # Actualizar recursos (con límites 0-100)
        self.agent.bateria = np.clip(self.agent.bateria - gasto_bateria, 0, 100)
        self.agent.neumaticos = np.clip(self.agent.neumaticos - gasto_goma, 0, 100)
        self.rival.neumaticos = np.clip(self.rival.neumaticos, 0, 100)

        # =========================================
        # 4. SISTEMA DE RECOMPENSAS AVANZADO ("SHAPED REWARD")
        # =========================================
        
        recompensa_total = 0.0

        # A. RECOMPENSA POR RITMO (DELTA)
        # Usamos una escala más agresiva. 
        # Ganar 0.1s es MUY bueno (+10 pts). Perder 0.1s es MUY malo (-10 pts).
        recompensa_total += delta * 100.0 

        # B. RECOMPENSA POR POSICIONAMIENTO (DRS)
        # Incentivamos mantener la presión.
        if 0.0 < self.gap_segundos < 1.0:
            recompensa_total += 2.0 # "Good job, you are in the kill zone"
        
        # D. BONO DE SUPERVIVENCIA
        # Si la batería está crítica y decides ahorrar, te premio.
        if self.agent.bateria < 10.0 and accion == 3: # Lift & Coast
            recompensa_total += 5.0 # "Smart move, recharging"

        # E. PENALIZACIONES DE FÍSICA (Que calculamos arriba)
        recompensa_total += recompensa_extra # (Choques, bloqueadas, intentos fallidos)

        # F. EVENTOS MAYORES
        # 1. ADELANTAMIENTO (El Jackpot)
        if self.gap_segundos <= 0:
            recompensa_total += 2000 # Aumentamos el premio para que sea IRRESISTIBLE
            return self._obtener_estado(), recompensa_total, True, "OVERTAKE"

        # 2. PERDIDA DE CONTACTO (Game Over táctico)
        # Si el rival se va a más de 3 segundos, la carrera está perdida en la práctica.
        if self.gap_segundos > 3.0:
            recompensa_total -= 50 # Castigo fuerte
            # Opcional: self.game_over = True (Para cortar episodios malos rápido)
        
        # 3. CHOQUE (Game Over físico)
        # Ya manejado arriba en la sección de seguridad, pero aseguramos
        if self.game_over and "CRASH" in str(recompensa_extra): 
             # Si ya detectamos choque arriba, la recompensa viene negativa de allá
             pass 

        # G. CASTIGO POR ABANDONO DE NEUMÁTICOS
        # Si llegas al Cliff (<20%), castigo constante por cada metro que avances así.
        if self.agent.neumaticos < 20:
            recompensa_total -= 2.0 # "Box, Box! Tires are dead!".

        # AVANCE
        self.sector_index += 1
        if self.sector_index >= len(self.track):
            self.sector_index = 0
            self.vuelta += 1
            if self.vuelta > 8: # Límite de vueltas para no eternizar
                self.game_over = True
                
        return self._obtener_estado(), recompensa_total, self.game_over, "RACE"

    def _obtener_estado(self):
        """
        Retorna: (gap, bat, goma_mia, goma_rival, sector, delta)
        """
        # 1. GAP (25 Niveles)
        g = self.gap_segundos
        if g < 0: estado_gap = 0 
        elif g >= 2.5: estado_gap = 24 
        elif g >= 1.5: estado_gap = 20 + int((g - 1.5) / 0.25)
        else: estado_gap = int(g / 0.075)

        # 2. BATERÍA (20 Niveles) - Cada 5%
        estado_bat = min(int(self.agent.bateria / 5), 19)

        # 3. MIS NEUMÁTICOS (20 Niveles) - Cada 5%
        estado_goma = min(int(self.agent.neumaticos / 5), 19)

        # 4. NEUMÁTICOS RIVAL (20 Niveles) - Cada 5%
        estado_goma_rival = min(int(self.rival.neumaticos / 5), 19)

        # 5. SECTOR (3 Niveles)
        tipo = self.track[self.sector_index]['tipo']
        if tipo == 'RECTA': estado_sector = 0
        elif tipo == 'CURVA': estado_sector = 1
        else: estado_sector = 2 

        # 6. DELTA RENDIMIENTO (7 Niveles)
        diff = self.agent.rendimiento - self.rival.rendimiento
        if diff < -0.05:   estado_delta = 0 # Muy Inferior
        elif diff < -0.03: estado_delta = 1
        elif diff < -0.01: estado_delta = 2
        elif diff > 0.05:  estado_delta = 6 # Muy Superior
        elif diff > 0.03:  estado_delta = 5
        elif diff > 0.01:  estado_delta = 4
        else:              estado_delta = 3 # Parejo

        return (estado_gap, estado_bat, estado_goma, estado_goma_rival, estado_sector, estado_delta)