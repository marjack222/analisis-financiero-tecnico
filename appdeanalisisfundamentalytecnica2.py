import pandas as pd
import numpy as np
import yfinance as yf
import ta

def analizar_ratios_financieros(tickers):
    from appdeanalisisfundamentalytecnica2 import df_ratios_lista_acciones, interpretacion_ratios, sugerencia_ratiosfinancieros
    df = pd.merge(df_ratios_lista_acciones, interpretacion_ratios, on="Ticker")
    df = pd.merge(df, sugerencia_ratiosfinancieros, on="Ticker")
    return df

def analizar_ingresos_y_ganancias(tickers):
    from appdeanalisisfundamentalytecnica2 import df_ingresosyganancias_lista_acciones, interpretacion_ingresos_y_ganancias, sugerencia_ingresosyganancias
    df = pd.merge(df_ingresosyganancias_lista_acciones, interpretacion_ingresos_y_ganancias, on="Ticker")
    df = pd.merge(df, sugerencia_ingresosyganancias, on="Ticker")
    return df

def analizar_deuda(tickers):
    from appdeanalisisfundamentalytecnica2 import df_deuda_lista_acciones_ratios, sugerencia_deuda
    return pd.merge(df_deuda_lista_acciones_ratios, sugerencia_deuda, on="Ticker")

def analizar_tecnico_diario(tickers):
    from appdeanalisisfundamentalytecnica2 import df_it_diaria_recomendation
    return df_it_diaria_recomendation

def analizar_tecnico_4h(tickers):
    from appdeanalisisfundamentalytecnica2 import df_it_4h_recomendation
    return df_it_4h_recomendation

def analizar_tecnico_1h(tickers):
    from appdeanalisisfundamentalytecnica2 import df_it_1h_recomendation
    return df_it_1h_recomendation