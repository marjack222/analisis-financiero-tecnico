import pandas as pd
import numpy as np
import yfinance as yf
import ta

# -----------------------------
# Análisis Fundamental
# -----------------------------

def analizar_ratios_financieros(tickers):
    def get_ratios(ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "Ticker": ticker,
                "PERatio": info.get('trailingPE', np.nan),
                "PriceToBookRatio": info.get('priceToBook', np.nan),
                "PriceToSalesRatioTTM": info.get('priceToSalesTrailing12Months', np.nan)
            }
        except:
            return {
                "Ticker": ticker,
                "PERatio": np.nan,
                "PriceToBookRatio": np.nan,
                "PriceToSalesRatioTTM": np.nan
            }

    def interpretar_ratios(pe, pb, ps):
        def val(ratio, low, high):
            if pd.isna(ratio): return "No disponible"
            if ratio < low: return "Infravalorada"
            if ratio <= high: return "Razonable"
            return "Sobrevalorada"
        return val(pe, 15, 25), val(pb, 1, 3), val(ps, 1, 2)

    def sugerencia(pe_i, pb_i, ps_i):
        if pe_i == pb_i == ps_i == "Infravalorada":
            return "Buy"
        if pe_i == pb_i == ps_i == "Sobrevalorada":
            return "Sell"
        if pe_i == pb_i == ps_i == "Razonable":
            return "Hold"
        return "Neutral"

    rows = []
    for t in tickers:
        d = get_ratios(t)
        pe_i, pb_i, ps_i = interpretar_ratios(d["PERatio"], d["PriceToBookRatio"], d["PriceToSalesRatioTTM"])
        d["P/E Interpretación"] = pe_i
        d["P/B Interpretación"] = pb_i
        d["P/S Interpretación"] = ps_i
        d["Sugerencia"] = sugerencia(pe_i, pb_i, ps_i)
        rows.append(d)

    return pd.DataFrame(rows)

def analizar_ingresos_y_ganancias(tickers):
    def get_ingresos(ticker):
        try:
            stock = yf.Ticker(ticker)
            inc = stock.income_stmt
            if inc is None or inc.empty or inc.shape[1] < 2:
                return None
            act = inc.iloc[:, 0]
            ant = inc.iloc[:, 1]
            rev_growth = (act.get("Total Revenue", 0) - ant.get("Total Revenue", 0)) / max(ant.get("Total Revenue", 1), 1)
            inc_growth = (act.get("Net Income", 0) - ant.get("Net Income", 0)) / max(ant.get("Net Income", 1), 1)

            def interpretar(val):
                if val > 0.15: return "Strong growth"
                if val >= 0.05: return "Moderate growth"
                return "Weak growth"

            def sugerencia(rg, ng):
                if rg == ng == "Strong growth": return "Buy"
                if rg == ng == "Moderate growth": return "Hold"
                if rg == ng == "Weak growth": return "Sell"
                return "Neutral"

            rev_int = interpretar(rev_growth)
            inc_int = interpretar(inc_growth)

            return {
                "Ticker": ticker,
                "Revenue Growth": rev_growth,
                "Revenue Interpretación": rev_int,
                "Net Income Growth": inc_growth,
                "Net Income Interpretación": inc_int,
                "Sugerencia": sugerencia(rev_int, inc_int)
            }
        except:
            return None

    rows = []
    for t in tickers:
        r = get_ingresos(t)
        if r:
            rows.append(r)
    return pd.DataFrame(rows)

def analizar_deuda(tickers):
    def get_deuda(ticker):
        try:
            stock = yf.Ticker(ticker)
            bs = stock.balance_sheet
            cf = stock.cashflow
            inc = stock.income_stmt
            if any(df is None or df.empty for df in [bs, cf, inc]):
                return None
            bs, cf, inc = bs.iloc[:, 0], cf.iloc[:, 0], inc.iloc[:, 0]
            ltd = bs.get("Long Term Debt", np.nan)
            ta = bs.get("Total Assets", np.nan)
            eq = bs.get("Total Stockholder Equity", np.nan)
            ocf = cf.get("Operating Cash Flow", np.nan)
            iexp = inc.get("Interest Expense", np.nan)

            r1 = ltd / ta if ta else 0
            r2 = ltd / eq if eq else 0
            r3 = ocf / iexp if iexp else np.inf
            r4 = ltd / ocf if ocf else 0

            score = 10
            if r1 > 0.5: score -= 2
            elif r1 > 0.3: score -= 1
            if r2 > 1: score -= 2
            elif r2 > 0.5: score -= 1
            if r3 < 2: score -= 2
            elif r3 < 5: score -= 1
            if r4 > 5: score -= 2
            elif r4 > 3: score -= 1

            sugerencia = "Buy" if score >= 8 else "Hold" if score >= 5 else "Sell"

            return {
                "Ticker": ticker,
                "debt_to_asset_ratio": r1,
                "debt_to_equity_ratio": r2,
                "interest_coverage_ratio": r3,
                "debt_to_cash_flow_ratio": r4,
                "Score": score,
                "Sugerencia": sugerencia
            }
        except:
            return None

    rows = []
    for t in tickers:
        r = get_deuda(t)
        if r:
            rows.append(r)
    return pd.DataFrame(rows)

# -----------------------------
# Análisis Técnico Diario
# -----------------------------

def analizar_tecnico_diario(tickers):
    def get_indicadores(ticker):
        try:
            df = yf.Ticker(ticker).history(period="1y")
            df['SMA20'] = ta.trend.sma_indicator(df['Close'], window=20)
            df['SMA50'] = ta.trend.sma_indicator(df['Close'], window=50)
            df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
            df['MACD'] = ta.trend.macd(df['Close'])
            df['MACD_Signal'] = ta.trend.macd_signal(df['Close'])

            ult = df.iloc[-1]
            score = 0
            if pd.notna(ult['RSI']) and ult['RSI'] < 30:
                score += 1
            if pd.notna(ult['MACD']) and pd.notna(ult['MACD_Signal']) and ult['MACD'] > ult['MACD_Signal']:
                score += 1
            if pd.notna(ult['SMA20']) and pd.notna(ult['SMA50']) and ult['SMA20'] > ult['SMA50']:
                score += 1

            if score == 3: rec = "compra fuerte"
            elif score == 2: rec = "compra"
            elif score == 1: rec = "mantener"
            else: rec = "venta"

            return {"Ticker": ticker, "Recomendación técnica": rec}
        except:
            return {"Ticker": ticker, "Recomendación técnica": "Error"}

    return pd.DataFrame([get_indicadores(t) for t in tickers])

def analizar_tecnico_4h(tickers):
    return pd.DataFrame([{"Ticker": t, "Recomendación técnica 4H": "No disponible en esta versión"} for t in tickers])

def analizar_tecnico_1h(tickers):
    return pd.DataFrame([{"Ticker": t, "Recomendación técnica 1H": "No disponible en esta versión"} for t in tickers])
