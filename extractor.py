import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq
from datetime import datetime
import os
import time

print("Iniciando MASTER-HUMAN BOT V4.0 (Escudo Anti-Crash)...")

s_vix_arg = 0
s_vix_usa = 0
s_vix_global = 0

# BLOQUE 1: GOOGLE TRENDS (Con tolerancia a fallos)
try:
    print("Extrayendo Google Trends...")
    pytrends_arg = TrendReq(hl='es-AR', tz=180, retries=3, backoff_factor=0.5)
    pytrends_arg.build_payload(["crisis", "emigrar", "dolar"], cat=0, timeframe='today 1-m', geo='AR')
    d_arg = pytrends_arg.interest_over_time()
    if not d_arg.empty:
        s_vix_arg = min(round(((d_arg['crisis'].mean() + d_arg['emigrar'].mean() + d_arg['dolar'].mean()) / 3) * 1.5, 2), 100)
    time.sleep(2)

    pytrends_usa = TrendReq(hl='en-US', tz=300, retries=3, backoff_factor=0.5)
    pytrends_usa.build_payload(["inflation", "layoffs", "crash"], cat=0, timeframe='today 1-m', geo='US')
    d_usa = pytrends_usa.interest_over_time()
    if not d_usa.empty:
        s_vix_usa = min(round(((d_usa['inflation'].mean() + d_usa['layoffs'].mean() + d_usa['crash'].mean()) / 3) * 1.5, 2), 100)
    time.sleep(2)

    pytrends_global = TrendReq(hl='en-US', tz=360, retries=3, backoff_factor=0.5)
    pytrends_global.build_payload(["recession", "war", "crash"], cat=0, timeframe='today 1-m')
    d_global = pytrends_global.interest_over_time()
    if not d_global.empty:
        s_vix_global = min(round(((d_global['recession'].mean() + d_global['war'].mean() + d_global['crash'].mean()) / 3) * 1.5, 2), 100)
        
except Exception as e:
    print(f"⚠️ Aviso: Google Trends bloqueó la conexión hoy. Se usará 0 en S-VIX. Error: {e}")

# BLOQUE 2: YAHOO FINANCE Y GUARDADO (Siempre se ejecuta aunque Google falle)
try:
    print("Extrayendo Wall Street...")
    def get_price(ticker):
        try:
            data = yf.Ticker(ticker).history(period="5d")
            return round(data['Close'].iloc[-1], 2) if not data.empty else 0
        except:
            return 0

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nuevo_dato = pd.DataFrame([{
        "Fecha": fecha_hoy,
        "SVIX_Arg": s_vix_arg,
        "SVIX_USA": s_vix_usa,
        "SVIX_Global": s_vix_global,
        "VIX_Mercado": get_price("^VIX"),
        "Precio_BTC": get_price("BTC-USD"),
        "Arg_Bancos": get_price("GGAL"),
        "Arg_Energia": get_price("YPF"),
        "Arg_Regulados": get_price("EDN"),
        "USA_Tech": get_price("QQQ"),
        "USA_Defensa": get_price("ITA"),
        "USA_Energia": get_price("XLE")
    }])

    archivo_csv = 'historial_svix.csv'
    nuevo_dato.to_csv(archivo_csv, mode='a', header=not os.path.exists(archivo_csv), index=False)
    print("🎯 ¡ÉXITO! Archivo guardado correctamente.")

except Exception as e:
    print(f"❌ Error crítico en Finanzas: {e}")
