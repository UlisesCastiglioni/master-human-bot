import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq
from datetime import datetime
import os
import time

print("Iniciando MASTER-HUMAN BOT V3.0 (Global Quant)...")

try:
    # 1. S-VIX ARGENTINA
    print("Extrayendo S-VIX Argentina...")
    pytrends_arg = TrendReq(hl='es-AR', tz=180)
    pytrends_arg.build_payload(["crisis", "emigrar", "dolar"], cat=0, timeframe='today 1-m', geo='AR')
    d_arg = pytrends_arg.interest_over_time()
    s_vix_arg = round(((d_arg['crisis'].mean() + d_arg['emigrar'].mean() + d_arg['dolar'].mean()) / 3) * 1.5, 2) if not d_arg.empty else 0
    s_vix_arg = min(s_vix_arg, 100)
    time.sleep(3)

    # 2. S-VIX USA
    print("Extrayendo S-VIX USA...")
    pytrends_usa = TrendReq(hl='en-US', tz=300)
    pytrends_usa.build_payload(["inflation", "layoffs", "crash"], cat=0, timeframe='today 1-m', geo='US')
    d_usa = pytrends_usa.interest_over_time()
    s_vix_usa = round(((d_usa['inflation'].mean() + d_usa['layoffs'].mean() + d_usa['crash'].mean()) / 3) * 1.5, 2) if not d_usa.empty else 0
    s_vix_usa = min(s_vix_usa, 100)
    time.sleep(3)

    # 3. S-VIX GLOBAL
    print("Extrayendo S-VIX Global...")
    pytrends_global = TrendReq(hl='en-US', tz=360)
    pytrends_global.build_payload(["recession", "war", "crash"], cat=0, timeframe='today 1-m')
    d_global = pytrends_global.interest_over_time()
    s_vix_global = round(((d_global['recession'].mean() + d_global['war'].mean() + d_global['crash'].mean()) / 3) * 1.5, 2) if not d_global.empty else 0
    s_vix_global = min(s_vix_global, 100)

    # 4. DATOS FINANCIEROS (Sectores y Macro)
    print("Extrayendo Wall Street...")
    def get_price(ticker):
        data = yf.Ticker(ticker).history(period="5d")
        return round(data['Close'].iloc[-1], 2) if not data.empty else 0

    # Sectores ARG
    arg_bancos = get_price("GGAL")
    arg_energia = get_price("YPF")
    arg_regulados = get_price("EDN")

    # Sectores USA
    usa_tech = get_price("QQQ") # Tecnología Globalista
    usa_defensa = get_price("ITA") # Cobertura de Guerra
    usa_energia = get_price("XLE") # Economía Real/Tradicional

    # Macro
    vix_mercado = get_price("^VIX")
    precio_btc = get_price("BTC-USD")

    # 5. GUARDAR DATOS (12 Columnas exactas)
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    nuevo_dato = pd.DataFrame([{
        "Fecha": fecha_hoy,
        "SVIX_Arg": s_vix_arg,
        "SVIX_USA": s_vix_usa,
        "SVIX_Global": s_vix_global,
        "VIX_Mercado": vix_mercado,
        "Precio_BTC": precio_btc,
        "Arg_Bancos": arg_bancos,
        "Arg_Energia": arg_energia,
        "Arg_Regulados": arg_regulados,
        "USA_Tech": usa_tech,
        "USA_Defensa": usa_defensa,
        "USA_Energia": usa_energia
    }])

    archivo_csv = 'historial_svix.csv'
    nuevo_dato.to_csv(archivo_csv, mode='a', header=not os.path.exists(archivo_csv), index=False)
    print("🎯 ¡ÉXITO! Robot Quant V3 actualizado y datos guardados.")

except Exception as e:
    print(f"❌ Error crítico: {e}")

4. Apretá el botón verde **"Commit changes"** dos veces.

**Paso 3: Forzar el Escaneo Inicial**
1. En GitHub, andá a la pestaña **"Actions"** arriba.
2. Clic en "Ejecutar MASTER-HUMAN Bot Diario" a la izquierda.
3. Clic en **"Run workflow"** a la derecha y esperá a que el circulito amarillo se ponga verde.
