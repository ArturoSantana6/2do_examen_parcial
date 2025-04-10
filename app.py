import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Análisis Financiero con Streamlit", layout="centered")
st.title("📊 Análisis Financiero de Empresas")
st.markdown("Ingresa el **ticker bursátil** de una empresa para ver su análisis financiero.")

ticker_input = st.text_input("Ticker (ejemplo: AAPL para Apple)", value="")

def validar_ticker(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except:
        return False

if ticker_input:
    if validar_ticker(ticker_input):
        ticker = yf.Ticker(ticker_input)
    else:
        st.error("❌ Ticker inválido. Por favor revisa el símbolo e intenta de nuevo.")

        st.header("🔍 Información de la Empresa")
        info = ticker.info
        st.write(f"**Nombre:** {info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Descripción:** {info.get('longBusinessSummary', 'N/A')}")

        st.header("📈 Precio Histórico de Cierre Ajustado")
        hist = ticker.history(period="5y")
        st.markdown("Gráfica de los últimos 5 años (precios ajustados).")
        st.line_chart(hist["Close"])

        st.header("📊 Rendimientos Anualizados (CAGR)")
        def calcular_cagr(df, años):
            final = df["Close"][-1]
            inicio = df["Close"][-252*años]
            return (final / inicio) ** (1 / años) - 1

        cagr_1y = calcular_cagr(hist, 1)
        cagr_3y = calcular_cagr(hist, 3)
        cagr_5y = calcular_cagr(hist, 5)

        df_cagr = pd.DataFrame({
            "Periodo": ["1 año", "3 años", "5 años"],
            "CAGR (%)": [f"{c*100:.2f}%" for c in [cagr_1y, cagr_3y, cagr_5y]]
        })

        st.markdown("El rendimiento anualizado se calculó usando la fórmula de CAGR:")
        st.latex(r'''CAGR = \left(\frac{Valor\ Final}{Valor\ Inicial}\right)^{\frac{1}{n}} - 1''')
        st.dataframe(df_cagr)

        st.header("📉 Volatilidad Anualizada")
        hist["Daily Returns"] = hist["Close"].pct_change()
        volatilidad = np.std(hist["Daily Returns"]) * np.sqrt(252)
        st.write(f"**Volatilidad histórica anualizada:** {volatilidad:.2%}")
        st.markdown("Este valor representa la volatilidad histórica del activo, calculada como la desviación estándar de los rendimientos diarios.")

st.sidebar.title("🧭 Navegación")
st.sidebar.markdown("""
1. Ingresa un ticker válido (ej: AAPL, MSFT, TSLA)
2. Visualiza los datos fundamentales
3. Revisa los rendimientos y riesgos
""")
