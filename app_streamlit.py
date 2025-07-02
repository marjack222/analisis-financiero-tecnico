import streamlit as st
import pandas as pd

from appdeanalisisfundamentalytecnica2 import (
    analizar_ratios_financieros,
    analizar_ingresos_y_ganancias,
    analizar_deuda,
    analizar_tecnico_diario,
    analizar_tecnico_4h,
    analizar_tecnico_1h,
)

st.set_page_config(layout="wide")
st.title("📈 Análisis Fundamental y Técnico de Acciones")

ticker_input = st.text_input("Ingresá uno o más tickers separados por coma (ej: AAPL, TSLA, MSFT):")
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

st.sidebar.title("Opciones de Análisis")
do_ratios = st.sidebar.checkbox("Ratios Financieros", value=True)
do_ingresos = st.sidebar.checkbox("Ingresos y Ganancias")
do_deuda = st.sidebar.checkbox("Deuda")
do_diario = st.sidebar.checkbox("Análisis Técnico Diario", value=True)
do_4h = st.sidebar.checkbox("Análisis Técnico 4H")
do_1h = st.sidebar.checkbox("Análisis Técnico 1H")

if st.button("🔎 Analizar"):
    if not tickers:
        st.warning("Por favor, ingresá al menos un ticker.")
    else:
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

        if do_diario:
            st.subheader("📊 Análisis Técnico Diario")
            df_d = analizar_tecnico_diario(tickers)
            st.dataframe(df_d)

        if do_4h:
            st.subheader("⏱️ Análisis Técnico 4H")
            df_4h = analizar_tecnico_4h(tickers)
            st.dataframe(df_4h)

        if do_1h:
            st.subheader("⏱️ Análisis Técnico 1H")
            df_1h = analizar_tecnico_1h(tickers)
            st.dataframe(df_1h)
