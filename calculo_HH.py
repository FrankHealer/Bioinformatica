import os
import pandas as pd
import numpy as np

# ==========================================
# 1. CONFIGURACIÓN DE CARPETAS Y ARCHIVOS### Aqui agregue los nombres de las bases de datos guardadas previamente (Coordenadas, Altitud, Nasa Power)
# ==========================================
carpeta_nasa = 'Datos_Agroclimaticos_General'
carpeta_salida = 'Resultados_Huella_Hidrica'
archivo_coordenadas = 'Coordenadas_finales.xlsx'
archivo_rendimiento = 'Rendimiento_Maiz.xlsx' 

os.makedirs(carpeta_salida, exist_ok=True)

# ==========================================
# 2. FUNCIONES MATEMÁTICAS FAO-56
# ==========================================
def calcular_fao56_diario(df_nasa, altitud, latitud):
    J = df_nasa['DOY']
    phi = np.radians(latitud)
    
    Tmax = df_nasa['T2M_MAX']
    Tmin = df_nasa['T2M_MIN']
    Tmean = (Tmax + Tmin) / 2
    HR = df_nasa['RH2M']
    Ux = df_nasa['WS2M']
    Rs = df_nasa['ALLSKY_SFC_SW_DWN']
    Pef = df_nasa['PRECTOTCORR']

    # Presión atmosférica y Psicrometría
    P_atm = 101.3 * ((293 - 0.0065 * altitud) / 293) ** 5.26
    gamma = 0.000665 * P_atm
    
    e_s_Tmax = 0.6108 * np.exp((17.27 * Tmax) / (Tmax + 237.3))
    e_s_Tmin = 0.6108 * np.exp((17.27 * Tmin) / (Tmin + 237.3))
    es = (e_s_Tmax + e_s_Tmin) / 2
    ea = es * (HR / 100)
    
    delta = (4098 * 0.6108 * np.exp((17.27 * Tmean) / (Tmean + 237.3))) / ((Tmean + 237.3) ** 2)

    # Radiación Neta
    Rns = 0.77 * Rs 
    
    dr = 1 + 0.033 * np.cos(2 * np.pi * J / 365)
    delta_sun = 0.409 * np.sin(2 * np.pi * J / 365 - 1.39)
    ws = np.arccos(np.clip(-np.tan(phi) * np.tan(delta_sun), -1, 1))
    Ra = (24 * 60 / np.pi) * 0.0820 * dr * (ws * np.sin(phi) * np.sin(delta_sun) + np.cos(phi) * np.cos(delta_sun) * np.sin(ws))
    
    Rso = (0.75 + 2e-5 * altitud) * Ra
    Rs_Rso = np.clip(Rs / Rso, 0.3, 1.0)
    
    Tmax_K = Tmax + 273.16
    Tmin_K = Tmin + 273.16
    sigma = 4.903e-9
    Rnl = sigma * ((Tmax_K**4 + Tmin_K**4) / 2) * (0.34 - 0.14 * np.sqrt(ea)) * (1.35 * Rs_Rso - 0.35)
    
    Rn = Rns - Rnl

    # Ecuación Penman-Monteith (ET0) ###  Una vez calculados todas las variables se realiza el calculo
    ET0 = (0.408 * delta * Rn + gamma * (900 / (Tmean + 273)) * Ux * (es - ea)) / (delta + gamma * (1 + 0.34 * Ux))
    
    return Tmean, es, ea, delta, P_atm, gamma, Rns, Rnl, Rn, ET0, Pef

# ==========================================
# 3. PROCESAMIENTO PRINCIPAL
# ==========================================
print("🧠 Iniciando el motor de cálculo FAO-56. Generando clon exacto del ejecutable...")

df_coords = pd.read_excel(archivo_coordenadas, skiprows=4)
df_rendimiento = pd.read_excel(archivo_rendimiento)
resumen_maestro = []

# Arreglos de Kc y Décadas (Etapas del cultivo)
kc_array = np.zeros(161)
kc_array[0:30] = 0.3                           
kc_array[30:70] = np.linspace(0.3, 1.2, 40)    
kc_array[70:120] = 1.2                         
kc_array[120:161] = np.linspace(1.2, 0.6, 41)

decada_array = np.zeros(161, dtype=int)
decada_array[0:30] = 1
decada_array[30:70] = 2
decada_array[70:120] = 3
decada_array[120:161] = 4

for index, row in df_rendimiento.iterrows():
    municipio = row['Municipio']
    
    datos_mun = df_coords[df_coords['Municipio'] == municipio]
    if datos_mun.empty: continue
    
    col_altitud = [col for col in datos_mun.columns if 'levaci' in col or 'altitud' in col.lower()][0]
    col_latitud = [col for col in datos_mun.columns if 'Latitud' in col][0]
    
    altitud = datos_mun[col_altitud].values[0]
    latitud = datos_mun[col_latitud].values[0]
    
    municipio_limpio = "".join(x for x in municipio if x.isalnum() or x in " _-")
    ruta_mun_nasa = os.path.join(carpeta_nasa, municipio_limpio)
    ruta_mun_salida = os.path.join(carpeta_salida, municipio_limpio)
    
    for anio in range(2010, 2025):
        if str(anio) not in df_rendimiento.columns and anio not in df_rendimiento.columns: continue
        rendimiento_ton = row[anio] if anio in row else row[str(anio)]
        if pd.isna(rendimiento_ton) or rendimiento_ton == 0: continue 
            
        archivo_nasa = f"{municipio_limpio}-FAO56-{anio}.CSV"
        ruta_csv_nasa = os.path.join(ruta_mun_nasa, archivo_nasa)
        if not os.path.exists(ruta_csv_nasa): continue
            
        try:
            with open(ruta_csv_nasa, 'r') as f: lineas = f.readlines()
            salto_lineas = next(i for i, linea in enumerate(lineas) if "YEAR" in linea)
            df_clima = pd.read_csv(ruta_csv_nasa, skiprows=salto_lineas).head(161).copy()
            
            # Cálculos FAO-56
            Tmean, es, ea, delta, P_atm, gamma, Rns, Rnl, Rn, ET0, Pef = calcular_fao56_diario(df_clima, altitud, latitud)
            
            # CONSTRUIR LA TABLA IDÉNTICA AL EJECUTABLE
            df_clon = pd.DataFrame()
            df_clon['Día'] = df_clima['DOY']
            df_clon['Tmax'] = df_clima['T2M_MAX']
            df_clon['Tmin'] = df_clima['T2M_MIN']
            df_clon['HR'] = df_clima['RH2M']
            df_clon['Ux'] = df_clima['WS2M']
            df_clon['Rs'] = df_clima['ALLSKY_SFC_SW_DWN']
            df_clon['Pef'] = Pef
            df_clon['Tmean'] = Tmean
            df_clon['es'] = es
            df_clon['ea'] = ea
            df_clon['delta'] = delta
            df_clon['P'] = P_atm
            df_clon['gamma'] = gamma
            df_clon['Rns'] = Rns
            df_clon['Rnl'] = Rnl
            df_clon['Rn'] = Rn
            df_clon['ET0'] = ET0
            df_clon['Kc'] = kc_array
            df_clon['ETc'] = ET0 * kc_array
            df_clon['decada'] = decada_array
            df_clon['ETverde'] = np.minimum(df_clon['ETc'], df_clon['Pef'])
            df_clon['ETazul'] = np.maximum(df_clon['ETc'] - df_clon['ETverde'], 0)
            
            et_verde_total = df_clon['ETverde'].sum()
            et_azul_total = df_clon['ETazul'].sum()
            uso_verde_m3_ha = et_verde_total * 10
            uso_azul_m3_ha = et_azul_total * 10
            hh_verde = uso_verde_m3_ha / rendimiento_ton
            hh_azul = uso_azul_m3_ha / rendimiento_ton
            
            os.makedirs(ruta_mun_salida, exist_ok=True)
            nombre_salida = f"{municipio_limpio}-FAO56-{anio}-HH.xlsx"
            ruta_excel_salida = os.path.join(ruta_mun_salida, nombre_salida)
            
            df_resumen = pd.DataFrame({
                'Parámetro': ['ETverde total (mm)', 'ETazul total (mm)', 'Uso de agua verde (m3/ha)', 'Uso de agua azul (m3/ha)', 'Huella Hídrica Verde (m3/ton)', 'Huella Hídrica Azul (m3/ton)', 'Rendimiento (Ton/ha)'],
                'Valor': [round(et_verde_total, 2), round(et_azul_total, 2), round(uso_verde_m3_ha, 2), round(uso_azul_m3_ha, 2), round(hh_verde, 2), round(hh_azul, 2), rendimiento_ton]
            })
            
            with pd.ExcelWriter(ruta_excel_salida) as writer:
                # Se nombra "Sheet1" para emular exactamente al software original
                df_clon.to_excel(writer, sheet_name='Sheet1', index=False)
                df_resumen.to_excel(writer, sheet_name='Resultados_Pantalla', index=False)
                
            resumen_maestro.append({
                'Municipio': municipio, 'Año': anio, 'Rendimiento_Ton_Ha': rendimiento_ton,
                'HH_Verde_m3_ton': round(hh_verde, 2), 'HH_Azul_m3_ton': round(hh_azul, 2),
                'Uso_Agua_Verde_m3_ha': round(uso_verde_m3_ha, 2), 'Uso_Agua_Azul_m3_ha': round(uso_azul_m3_ha, 2)
            })
            print(f"✅ Clon creado: {municipio} - {anio}")
            
        except Exception as e:
            print(f"❌ Error procesando {municipio} {anio}: {e}")

df_maestro = pd.DataFrame(resumen_maestro)
df_maestro.to_excel("MATRIZ_MAESTRA_HUELLA_HIDRICA.xlsx", index=False)
print("\n🎉 ¡PROCESO TERMINADO PERFECTAMENTE! 🎉")
