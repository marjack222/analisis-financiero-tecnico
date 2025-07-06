
import pandas as pd
import numpy as np
import yfinance as yf
import ta

# ===============================
# 📐 ANÁLISIS FUNDAMENTAL
# ===============================

def analizar_ratios_financieros(tickers):
    """Analiza ratios P/E, P/B y P/S con interpretación y sugerencia."""
    resultados = []

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            pe = info.get('trailingPE', np.nan)
            pb = info.get('priceToBook', np.nan)
            ps = info.get('priceToSalesTrailing12Months', np.nan)

            pe_interp = interpretar_ratio(pe, 15, 25)
            pb_interp = interpretar_ratio(pb, 1, 3)
            ps_interp = interpretar_ratio(ps, 1, 2)

            sugerencia = sugerir_accion([pe_interp, pb_interp, ps_interp])

            resultados.append({
                "Ticker": ticker,
                "P/E": pe, "P/E interpretación": pe_interp,
                "P/B": pb, "P/B interpretación": pb_interp,
                "P/S": ps, "P/S interpretación": ps_interp,
                "Sugerencia": sugerencia
            })
        except Exception as e:
            resultados.append({
                "Ticker": ticker,
                "P/E": None, "P/E interpretación": "Error",
                "P/B": None, "P/B interpretación": "Error",
                "P/S": None, "P/S interpretación": "Error",
                "Sugerencia": "Error"
            })

    return pd.DataFrame(resultados)

def interpretar_ratio(valor, bajo, alto):
    if pd.isna(valor):
        return "No disponible"
    if valor < bajo:
        return "Infravalorado"
    if valor <= alto:
        return "Razonable"
    return "Sobrevalorado"

def sugerir_accion(interps):
    if all(v == "Infravalorado" for v in interps):
        return "Comprar"
    if all(v == "Sobrevalorado" for v in interps):
        return "Vender"
    if all(v == "Razonable" for v in interps):
        return "Mantener"
    return "Evaluar caso a caso"

# ===============================
# 📊 ANÁLISIS TÉCNICO
# ===============================

def analizar_tecnico(tickers, intervalo, nombre_intervalo):
    """Calcula RSI, MACD, cruces de medias y sugiere una acción"""
    resultados = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period="60d", interval=intervalo, progress=False)
            if df.empty or len(df) < 50:
                resultados.append({"Ticker": ticker, f"Sugerencia técnica {nombre_intervalo}": "Datos insuficientes"})
                continue

            # Indicadores
            rsi = ta.momentum.RSIIndicator(df['Close']).rsi()
            macd = ta.trend.MACD(df['Close']).macd_diff()
            sma20 = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
            sma50 = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()

            # Últimos valores
            ult_rsi = rsi.iloc[-1]
            ult_macd = macd.iloc[-1]
            ult_sma20 = sma20.iloc[-1]
            ult_sma50 = sma50.iloc[-1]

            # Score técnico
            score = 0
            if pd.notna(ult_rsi) and ult_rsi < 30: score += 1
            if pd.notna(ult_macd) and ult_macd > 0: score += 1
            if pd.notna(ult_sma20) and pd.notna(ult_sma50) and ult_sma20 > ult_sma50: score += 1

            if score == 3:
                recomendacion = "Compra fuerte"
            elif score == 2:
                recomendacion = "Comprar"
            elif score == 1:
                recomendacion = "Mantener"
            else:
                recomendacion = "Vender"

            resultados.append({
                "Ticker": ticker,
                f"RSI {nombre_intervalo}": round(ult_rsi, 2),
                f"MACD {nombre_intervalo}": round(ult_macd, 2),
                f"SMA20 > SMA50 {nombre_intervalo}": ult_sma20 > ult_sma50,
                f"Sugerencia técnica {nombre_intervalo}": recomendacion
            })
        except:
            resultados.append({
                "Ticker": ticker,
                f"RSI {nombre_intervalo}": None,
                f"MACD {nombre_intervalo}": None,
                f"SMA20 > SMA50 {nombre_intervalo}": None,
                f"Sugerencia técnica {nombre_intervalo}": "Error"
            })

    return pd.DataFrame(resultados)

def analizar_tecnico_diario(tickers):
    return analizar_tecnico(tickers, "1d", "Diario")

def analizar_tecnico_4h(tickers):
    return analizar_tecnico(tickers, "60m", "4H")

def analizar_tecnico_1h(tickers):
    return analizar_tecnico(tickers, "30m", "1H")
