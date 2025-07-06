import pandas as pd
import numpy as np
import yfinance as yf
import ta

# ===============================
# 📐 ANÁLISIS FUNDAMENTAL
# ===============================

def analizar_ratios_financieros(tickers):
    """Analiza ratios P/E, P/B, P/S, deuda, ingresos y ganancias con interpretación y sugerencia."""
    resultados = []

    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            pe = info.get('trailingPE', np.nan)
            pb = info.get('priceToBook', np.nan)
            ps = info.get('priceToSalesTrailing12Months', np.nan)
            ingresos = info.get('totalRevenue', np.nan)
            ganancias = info.get('netIncomeToCommon', np.nan)
            deuda_total = info.get('totalDebt', np.nan)
            equity = info.get('totalStockholderEquity', np.nan)
            deuda_a_equity = deuda_total / equity if (pd.notna(deuda_total) and pd.notna(equity) and equity != 0) else np.nan

            pe_interp = interpretar_ratio(pe, 15, 25)
            pb_interp = interpretar_ratio(pb, 1, 3)
            ps_interp = interpretar_ratio(ps, 1, 2)
            deuda_interp = interpretar_deuda(deuda_a_equity)

            sugerencia = sugerir_accion([pe_interp, pb_interp, ps_interp, deuda_interp])

            resultados.append({
                "Ticker": ticker,
                "P/E": pe, "P/E interpretación": pe_interp,
                "P/B": pb, "P/B interpretación": pb_interp,
                "P/S": ps, "P/S interpretación": ps_interp,
                "Ingresos": ingresos,
                "Ganancias": ganancias,
                "Deuda Total": deuda_total,
                "Equity": equity,
                "Deuda/Equity": deuda_a_equity,
                "Deuda interpretación": deuda_interp,
                "Sugerencia": sugerencia
            })
        except Exception as e:
            resultados.append({
                "Ticker": ticker,
                "P/E": None, "P/E interpretación": f"Error: {e}",
                "P/B": None, "P/B interpretación": f"Error: {e}",
                "P/S": None, "P/S interpretación": f"Error: {e}",
                "Ingresos": None,
                "Ganancias": None,
                "Deuda Total": None,
                "Equity": None,
                "Deuda/Equity": None,
                "Deuda interpretación": f"Error: {e}",
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

def interpretar_deuda(deuda_a_equity):
    if pd.isna(deuda_a_equity):
        return "No disponible"
    if deuda_a_equity < 0.5:
        return "Baja deuda"
    elif deuda_a_equity <= 1:
        return "Deuda razonable"
    else:
        return "Alta deuda"

def sugerir_accion(interps):
    # Si alguna interpretación es "Alta deuda" o "Sobrevalorado", sugerir "Evaluar caso a caso"
    if "Alta deuda" in interps or "Sobrevalorado" in interps:
        return "Evaluar caso a caso"
    if all(v == "Infravalorado" or v == "Baja deuda" for v in interps):
        return "Comprar"
    if all(v == "Sobrevalorado" or v == "Alta deuda" for v in interps):
        return "Vender"
    if all(v == "Razonable" or v == "Deuda razonable" for v in interps):
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
                resultados.append({
                    "Ticker": ticker,
                    f"Sugerencia técnica {nombre_intervalo}": "Datos insuficientes"
                })
                continue

            # Asegurarse de que 'Close' sea una Serie 1D
            close_series = df['Close']
            if isinstance(close_series, pd.DataFrame):
                close_series = close_series.squeeze()

            # Indicadores
            rsi = ta.momentum.RSIIndicator(close_series).rsi()
            macd = ta.trend.MACD(close_series).macd_diff()
            sma20 = ta.trend.SMAIndicator(close_series, window=20).sma_indicator()
            sma50 = ta.trend.SMAIndicator(close_series, window=50).sma_indicator()

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
        except Exception as e:
            resultados.append({
                "Ticker": ticker,
                f"RSI {nombre_intervalo}": None,
                f"MACD {nombre_intervalo}": None,
                f"SMA20 > SMA50 {nombre_intervalo}": None,
                f"Sugerencia técnica {nombre_intervalo}": f"Error: {e}"
            })

    return pd.DataFrame(resultados)

def analizar_tecnico_diario(tickers):
    return analizar_tecnico(tickers, "1d", "Diario")

def analizar_tecnico_4h(tickers):
    return analizar_tecnico(tickers, "60m", "4H")

def analizar_tecnico_1h(tickers):
    return analizar_tecnico(tickers, "30m", "1H")

# ===============================
# FUNCIONES DE PRESENTACIÓN Y CONSOLIDACIÓN
# ===============================

def mostrar_resultados_tecnicos(tickers):
    print("=== Análisis Técnico Diario ===")
    print(analizar_tecnico_diario(tickers).to_string(index=False))
    print("\n=== Análisis Técnico 4H ===")
    print(analizar_tecnico_4h(tickers).to_string(index=False))
    print("\n=== Análisis Técnico 1H ===")
    print(analizar_tecnico_1h(tickers).to_string(index=False))

def mostrar_resultados_fundamentales(tickers):
    print("=== Análisis Fundamental ===")
    print(analizar_ratios_financieros(tickers).to_string(index=False))

def analizar_y_mostrar_todo(tickers):
    """Función principal para mostrar análisis fundamental y técnico de una lista de tickers."""
    mostrar_resultados_fundamentales(tickers)
    print("\n")
    mostrar_resultados_tecnicos(tickers)

def exportar_resultados_tecnicos_csv(tickers, archivo_base="tecnico"):
    """Guarda los resultados técnicos en archivos CSV separados por intervalo."""
    diario = analizar_tecnico_diario(tickers)
    cuatroh = analizar_tecnico_4h(tickers)
    unah = analizar_tecnico_1h(tickers)
    diario.to_csv(f"{archivo_base}_diario.csv", index=False)
    cuatroh.to_csv(f"{archivo_base}_4h.csv", index=False)
    unah.to_csv(f"{archivo_base}_1h.csv", index=False)

def exportar_resultados_fundamentales_csv(tickers, archivo="fundamental.csv"):
    """Guarda los resultados fundamentales en un archivo CSV."""
    df = analizar_ratios_financieros(tickers)
    df.to_csv(archivo, index=False)

# ===============================
# USO DESDE LÍNEA DE COMANDOS
# ===============================

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        tickers = sys.argv[1:]
        analizar_y_mostrar_todo(tickers)
        exportar_resultados_tecnicos_csv(tickers)
        exportar_resultados_fundamentales_csv(tickers)
        print("\nResultados exportados a CSV (tecnico_diario.csv, tecnico_4h.csv, tecnico_1h.csv, fundamental.csv)")
    else:
        print("Por favor, ingresa uno o más tickers como argumentos.")
