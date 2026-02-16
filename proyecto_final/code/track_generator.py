import fastf1
import numpy as np
import os

# 1. Configuración de Cache (Obligatorio para que FastF1 vaya rápido)
# Crea una carpeta llamada 'cache' en el mismo lugar que este script
if not os.path.exists('cache'):
    os.makedirs('cache')
fastf1.Cache.enable_cache('cache') 

def generar_mapa_circuito(year, gp, driver, n_sectores=50):
    print(f"--- Descargando datos de {gp} {year} para {driver} ---")
    
    # Cargamos la sesión de Clasificación (Q) porque es donde van más rápido
    session = fastf1.get_session(year, gp, 'Q')
    session.load()
    
    # Seleccionamos la vuelta más rápida del piloto
    lap = session.laps.pick_driver(driver).pick_fastest()
    telemetry = lap.get_telemetry()
    
    # Datos totales de la vuelta
    distancia_total = telemetry['Distance'].max()
    longitud_sector = distancia_total / n_sectores
    
    mapa_circuito = []

    print(f"Analizando vuelta de {distancia_total:.2f}m en {n_sectores} sectores...")
    
    for i in range(n_sectores):
        # Definir inicio y fin del sector en metros
        inicio = i * longitud_sector
        fin = (i + 1) * longitud_sector
        
        # Filtrar los datos de telemetría que caen DENTRO de este sector
        mask = (telemetry['Distance'] >= inicio) & (telemetry['Distance'] < fin)
        datos_sector = telemetry.loc[mask]
        
        if datos_sector.empty:
            continue

        # --- ANÁLISIS FÍSICO DEL SECTOR ---
        
        # 1. Velocidad Máxima posible en este tramo (Límite físico)
        max_speed = datos_sector['Speed'].max()
        
        # 2. Promedios para determinar el TIPO de sector
        avg_throttle = datos_sector['Throttle'].mean()
        avg_brake = datos_sector['Brake'].mean()
        
        # Lógica de Clasificación (Heurística simple)
        tipo_sector = "CURVA" # Por defecto
        dificultad = 0.5      # 1.0 = Muy fácil pasar, 0.1 = Imposible
        
        if avg_throttle > 90:
            tipo_sector = "RECTA"
            dificultad = 1.0 # Ancho y rápido
        elif avg_brake > 0 and avg_throttle < 20:
            tipo_sector = "FRENADA"
            dificultad = 0.8 # Buen lugar para intentar un 'dive bomb'
        else:
            tipo_sector = "CURVA"
            dificultad = 0.2 # Difícil pasar en curva media
            
        # 3. Detección de DRS (Si el DRS está activado en alguna parte del sector)
        # FastF1: DRS column codes (10, 12, 14 mean active usually)
        # Simplificación: Si DRS > 8, está abierto.
        drs_active = datos_sector['DRS'].max() > 8 
        
        # Crear el diccionario (Objeto) del sector
        sector_info = {
            "id": i,
            "distancia_inicio": int(inicio),
            "tipo": tipo_sector,
            "max_speed_kmh": int(max_speed),
            "drs": bool(drs_active),
            "prob_adelantar": dificultad
        }
        
        mapa_circuito.append(sector_info)

    return mapa_circuito

# --- PRUEBA DEL SCRIPT ---
if __name__ == "__main__":
    # Usamos la pole de piastri en 2025 como referencia
    mapa = generar_mapa_circuito(2025, 'Bahrain', 'PIA', n_sectores=50)
    
    print("\n--- MAPA GENERADO EXITOSAMENTE ---")
    print(f"{'SEC':<4} {'TIPO':<10} {'VEL_MAX':<10} {'DRS':<5} {'ADELANTAR'}")
    print("-" * 50)
    
    for s in mapa:
        drs_mark = "SI" if s['drs'] else ""
        print(f"{s['id']:<4} {s['tipo']:<10} {s['max_speed_kmh']:<10} {drs_mark:<5} {s['prob_adelantar']}")

    # Opcional: Guardar esto en un archivo JSON para usarlo luego
    import json
    with open('mapa_bahrain.json', 'w') as f:
        json.dump(mapa, f, indent=4)
    print("\nMapa guardado en 'mapa_bahrain.json'")