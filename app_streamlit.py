
import streamlit as st
import pandas as pd
from appdeanalisisfundamentalytecnica2 import (
    analizar_ratios_financieros, analizar_ingresos_y_ganancias,
    analizar_deuda, analizar_tecnico_diario, analizar_tecnico_4h,
    analizar_tecnico_1h
)

st.set_page_config(page_title="Análisis Fundamental y Técnico", layout="wide")
st.title("📊 Análisis Fundamental y Técnico de Acciones")

# Entrada de tickers
tickers_input = st.text_input("📥 Ingresá uno o más tickers separados por coma (ej: AAPL, MSFT, TSLA):")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

# Selección de tipo de análisis
st.sidebar.title("🔧 Opciones de análisis")
do_ratios = st.sidebar.checkbox("Ratios Financieros", value=True)
do_ingresos = st.sidebar.checkbox("Ingresos y Ganancias")
do_deuda = st.sidebar.checkbox("Deuda")
do_tec_d = st.sidebar.checkbox("Técnico Diario")
do_tec_4h = st.sidebar.checkbox("Técnico 4H")
do_tec_1h = st.sidebar.checkbox("Técnico 1H")

# Botón de análisis
if st.button("🔎 Analizar") and tickers:
    if do_ratios:
        st.subheader("📐 Ratios Financieros")
        df_ratios = analizar_ratios_financieros(tickers)
        st.dataframe(df_ratios)
    if do_ingresos:
        st.subheader("📈 Ingresos y Ganancias")
        df_ingresos = analizar_ingresos_y_ganancias(tickers)
        st.dataframe(df_ingresos)
    if do_deuda:
        st.subheader("💰 Análisis de Deuda")
        df_deuda = analizar_deuda(tickers)
        st.dataframe(df_deuda)
    if do_tec_d:
        st.subheader("📊 Análisis Técnico Diario")
        df_d = analizar_tecnico_diario(tickers)
        st.dataframe(df_d)
    if do_tec_4h:
        st.subheader("⏱️ Análisis Técnico 4 Horas")
        df_4h = analizar_tecnico_4h(tickers)
        st.dataframe(df_4h)
    if do_tec_1h:
        st.subheader("⏱️ Análisis Técnico 1 Hora")
        df_1h = analizar_tecnico_1h(tickers)
        st.dataframe(df_1h)

st.markdown("---")
st.markdown("⚙️ Esta aplicación corre localmente usando tu lógica actual. Podés exportarla a Streamlit Cloud más adelante.")
