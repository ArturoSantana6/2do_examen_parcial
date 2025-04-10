mport streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go

st.set_page_config(page_title="Análisis Financiero Profesional", layout="wide")
st.title("📊 Análisis Financiero de Empresas - Nivel Profesional")
st.markdown("Ingresa un **ticker bursátil válido** para analizar el comportamiento de una empresa del mercado.")

with st.sidebar:
    st.image("https://img.icons8.com/color/96/graph.png", width=50)
    st.header("🔎 Instrucciones")
    st.markdown("1. Ingresa un símbolo como `AAPL`, `MSFT`, `TSLA`.")
    st.markdown("2. Visualiza datos financieros y métricas clave.")
    ticker_input = st.text_input("Ticker:", value="", max_chars=10)
    buscar = st.button("🔍 Buscar")

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
        info = ticker.info
        hist = ticker.history(period="5y")

        # Datos fundamentales
        st.header("🏢 Información de la Empresa")
        st.markdown(f"**Nombre:** {info.get('longName', 'N/A')}")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
        st.markdown(f"**Descripción:** {info.get('longBusinessSummary', 'No disponible')}")

        # Gráfica de precios con Plotly
        st.header("📈 Precio Histórico de Cierre Ajustado (5 años)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Precio cierre'))
        fig.update_layout(title=f'Histórico de precios - {ticker_input.upper()}', xaxis_title='Fecha', yaxis_title='Precio (USD)')
        st.plotly_chart(fig, use_container_width=True)

        # Rendimientos CAGR
        st.header("📊 Rendimientos Anualizados (CAGR)")
        cagr_1y = calcular_cagr(hist, 1)
        cagr_3y = calcular_cagr(hist, 3)
        cagr_5y = calcular_cagr(hist, 5)

        df_cagr = pd.DataFrame({
            "Periodo": ["1 año", "3 años", "5 años"],
            "CAGR (%)": [f"{c*100:.2f}%" for c in [cagr_1y, cagr_3y, cagr_5y]]
        })

        st.markdown("**Fórmula usada:**")
        st.latex(r"CAGR = \left(\frac{Precio_{final}}{Precio_{inicial}}\right)^{\frac{1}{n}} - 1")
ight)^{rac{1}{n}} - 1")
        st.dataframe(df_cagr)

        # Volatilidad histórica
        st.header("📉 Volatilidad Anualizada (Riesgo)")
        hist["Daily Returns"] = hist["Close"].pct_change()
        vol = np.std(hist["Daily Returns"]) * np.sqrt(252)
        st.metric("Volatilidad Anualizada", f"{vol:.2%}")
        st.markdown("Este valor representa la variabilidad de los retornos diarios, anualizada con √252.")

    else:
        st.error("❌ Ticker inválido. Intenta con otro símbolo como AAPL, MSFT, etc.")

