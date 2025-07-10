import numpy as np
import pandas as pd
import yfinance as yf

# ----------------- LÓGICA DEL PROGRAMA -----------------

def generar_datos_reales(nombres_empresas, tickers, num_dias):
    data = yf.download(tickers, period=f"{num_dias+1}d", interval="1d", auto_adjust=True)
    if data.empty:
        raise ValueError("No se pudieron obtener datos de los tickers proporcionados.")

    if isinstance(data.columns, pd.MultiIndex):
        data = data['Close']

    tickers_disponibles = [t for t in tickers if t in data.columns]
    nombres_disponibles = [nombres_empresas[i] for i, t in enumerate(tickers) if t in data.columns]

    if not tickers_disponibles:
        raise ValueError("Ninguno de los tickers proporcionó datos válidos.")

    data = data[tickers_disponibles]
    retornos = data.pct_change().dropna()
    dias = [f"Dia {i + 1}" for i in range(len(retornos))]
    retornos.index = dias
    df_retornos = retornos.transpose()
    df_retornos.index = nombres_disponibles

    return df_retornos, dias

def calcular_transiciones(df_retornos, nombres_empresas, dias):
    empresa_max_retornos = df_retornos.idxmax()
    transiciones = {empresa: {e: 0 for e in nombres_empresas} for empresa in nombres_empresas}

    for i in range(len(dias) - 1):
        empresa_actual = empresa_max_retornos[dias[i]]
        empresa_siguiente = empresa_max_retornos[dias[i + 1]]
        transiciones[empresa_actual][empresa_siguiente] += 1

    df_transiciones = pd.DataFrame(transiciones, index=nombres_empresas)
    col_sumas = df_transiciones.sum(axis=0)
    df_transiciones_normalizada = df_transiciones.div(col_sumas, axis=1)

    vector_inicial = np.zeros(len(nombres_empresas))
    empresa_inicial = empresa_max_retornos[dias[0]]
    indice_empresa_inicial = nombres_empresas.index(empresa_inicial)
    vector_inicial[indice_empresa_inicial] = 1

    return df_transiciones_normalizada, vector_inicial
