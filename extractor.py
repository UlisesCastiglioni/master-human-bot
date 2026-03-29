import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq
from datetime import datetime
import os

print("Iniciando MASTER-HUMAN BOT...")

try:
    # 1. CONEXIÓN A GOOGLE TRENDS (El Miedo en la calle)
    print("Conectando a Google Trends...")
    pytrends = TrendReq(hl='es-AR', tz=180) # Configurado para Argentina
    
    # Palabras clave de pánico social
    palabras_clave = ["crisis", "emigrar", "dolar"]
    pytrends.build_payload(palabras_clave, cat=0, timeframe='today 1-m', geo='AR')
    
    # Obtener el interés a lo largo del tiempo
    datos_trends = pytrends.interest_over_time()
    
    # Calcular el "S-VIX" promedio de pánico de los últimos 30 días
    if not datos_trends.empty:
        # Sumamos el interés de las 3 palabras y sacamos el promedio del último mes
        panico_promedio = (datos_trends['crisis'].mean() + datos_trends['emigrar'].mean() + datos_trends['dolar'].mean()) / 3
        # Normalizamos un poco para que dé un número entre 0 y 100
        s_vix_hoy = round(panico_promedio * 1.5, 2) 
        if s_vix_hoy > 100: s_vix_hoy = 100 # Tope en 100
    else:
        s_vix_hoy = 0
        
    print(f"✅ S-VIX Calculado: {s_vix_hoy}/100")

    # 2. CONEXIÓN A YAHOO FINANCE (El Smart Money)
    print("Conectando a Yahoo Finance...")
    # Buscamos GGAL (Galicia en Wall Street). 
    # Usamos period="5d" para evitar el error de bolsa cerrada los fines de semana.
    bono = yf.Ticker("GGAL")
    historial = bono.history(period="5d")
    
    if not historial.empty:
        # Agarra el precio de cierre del último día disponible
        precio_hoy = historial['Close'].iloc[-1]
        precio_hoy = round(precio_hoy, 2)
        print(f"✅ Precio GGAL (Smart Money) Hoy: ${precio_hoy}")
    else:
        precio_hoy = 0
        print("⚠️ No se encontraron datos de precio hoy.")

    # 3. GUARDAR LOS DATOS (El Historial)
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    # Creamos una fila de Excel (CSV) con los datos
    nuevo_dato = pd.DataFrame([{
        "Fecha": fecha_hoy,
        "S-VIX_Arg": s_vix_hoy,
        "Precio_GGAL": precio_hoy
    }])

    archivo_csv = 'historial_svix.csv'
    # Guardamos. Si el archivo no existe, le pone los títulos arriba (header=True)
    nuevo_dato.to_csv(archivo_csv, mode='a', header=not os.path.exists(archivo_csv), index=False)
    
    print(f"🎯 ¡Datos guardados exitosamente en {archivo_csv}!")

except Exception as e:
    print(f"❌ Error en el sistema: {e}")
    