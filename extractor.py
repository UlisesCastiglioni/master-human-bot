import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq
from datetime import datetime
import os
import time

print("Iniciando MASTER-HUMAN BOT V2.0...")

try:
    # 1. TENDENCIAS ARGENTINA (El Miedo Local)
    print("Extrayendo S-VIX Argentina...")
    pytrends_arg = TrendReq(hl='es-AR', tz=180)
    pytrends_arg.build_payload(["crisis", "emigrar", "dolar"], cat=0, timeframe='today 1-m', geo='AR')
    datos_arg = pytrends_arg.interest_over_time()
    
    s_vix_arg = 0
    if not datos_arg.empty:
        s_vix_arg = round(((datos_arg['crisis'].mean() + datos_arg['emigrar'].mean() + datos_arg['dolar'].mean()) / 3) * 1.5, 2)
        s_vix_arg = min(s_vix_arg, 100) # Tope 100

    # Pausa de 3 segundos para que Google no nos bloquee por pedir datos muy rápido
    time.sleep(3)

    # 2. TENDENCIAS GLOBALES (El Miedo Mundial)
    print("Extrayendo S-VIX Global...")
    pytrends_global = TrendReq(hl='en-US', tz=360)
    # Buscamos en inglés en todo el mundo
    pytrends_global.build_payload(["recession", "war", "crash"], cat=0, timeframe='today 1-m')
    datos_global = pytrends_global.interest_over_time()
    
    s_vix_global = 0
    if not datos_global.empty:
        s_vix_global = round(((datos_global['recession'].mean() + datos_global['war'].mean() + datos_global['crash'].mean()) / 3) * 1.5, 2)
        s_vix_global = min(s_vix_global, 100) # Tope 100

    # 3. DATOS FINANCIEROS (Yahoo Finance)
    print("Extrayendo Smart Money y Cripto...")
    
    # GGAL (Smart Money Argentina)
    ggal = yf.Ticker("GGAL").history(period="5d")
    precio_ggal = round(ggal['Close'].iloc[-1], 2) if not ggal.empty else 0

    # VIX (Volatilidad S&P 500 - Pánico de Inversores)
    vix = yf.Ticker("^VIX").history(period="5d")
    precio_vix = round(vix['Close'].iloc[-1], 2) if not vix.empty else 0

    # BITCOIN (El refugio Anti-Estado)
    btc = yf.Ticker("BTC-USD").history(period="5d")
    precio_btc = round(btc['Close'].iloc[-1], 2) if not btc.empty else 0

    # 4. GUARDAR LOS DATOS (El Historial)
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    nuevo_dato = pd.DataFrame([{
        "Fecha": fecha_hoy,
        "S-VIX_Arg": s_vix_arg,
        "S-VIX_Global": s_vix_global,
        "VIX_Mercado": precio_vix,
        "Precio_GGAL": precio_ggal,
        "Precio_BTC": precio_btc
    }])

    archivo_csv = 'historial_svix.csv'
    nuevo_dato.to_csv(archivo_csv, mode='a', header=not os.path.exists(archivo_csv), index=False)
    
    print(f"🎯 ¡ÉXITO! Datos V2.0 guardados en {archivo_csv}")
    print(f"Resumen: SVIX_AR({s_vix_arg}) | SVIX_GL({s_vix_global}) | BTC(${precio_btc})")

except Exception as e:
    print(f"❌ Error crítico en el sistema: {e}")
