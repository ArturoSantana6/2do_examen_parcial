import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Análisis Financiero", layout="centered")
st.title("📊 Análisis Financiero de Empresas")

# Input del usuario
ticker_input = st.text_input("Ticker bursátil (ej. AAPL, MSFT, TSLA):")
buscar = ticker

def validar_ticker(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except:
        return False

def calcular_cagr(df, años):
    final = df["Close"][-1]
    inicio = df["Close"][-252*años]
    return (final / inicio) ** (1 / años) - 1

if buscar and ticker_input:
    if validar_ticker(ticker_input):
        ticker = yf.Ticker(ticker_input)

        # Info básica
        info = ticker.info
        st.header("🔍 Información de la Empresa")
        st.write(f"**Nombre:** {info.get('longName', 'N/A')}")
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Descripción:** {info.get('longBusinessSummary', 'N/A')}")

        # Precios históricos
        hist = ticker.history(period="5y")
        st.header("📈 Precio Histórico")
        st.line_chart(hist["Close"])

        # CAGR
        st.header("📊 Rendimientos Anualizados")
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

        # Volatilidad
        st.header("📉 Volatilidad")
        hist["Daily Returns"] = hist["Close"].pct_change()
        vol = np.std(hist["Daily Returns"]) * np.sqrt(252)
        st.write(f"**Volatilidad anualizada:** {vol:.2%}")
        st.markdown("Este valor representa la volatilidad histórica del activo, medida por la desviación estándar de los rendimientos diarios.")
    else:
        st.error("❌ Ticker inválido. Intenta con otro como AAPL, MSFT, etc.")

