import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análisis de Fauna Silvestre - Medellín", layout="wide")

st.title("Análisis de Fauna Silvestre (2017–2025)")
st.write("Aplicación interactiva para explorar la base de datos de fauna silvestre atendida en Medellín.")

# --- CARGA DE ARCHIVO ---
st.sidebar.header("Carga de datos")
uploaded_file = st.sidebar.file_uploader("Sube el archivo Excel de fauna", type=["xlsx"])

if uploaded_file is None:
    st.info("👉 Sube el archivo Excel para comenzar el análisis.")
    st.stop()

# --- LECTURA Y CACHEO DE DATOS ---
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    return df

df = load_data(uploaded_file)

st.success(f"Datos cargados correctamente. Registros: {len(df)}")

# --- FILTROS BÁSICOS ---
st.sidebar.header("Filtros")

# Filtro por año (asumiendo columna 'AÑOREMISION')
if "AÑOREMISION" in df.columns:
    years = sorted(df["AÑOREMISION"].dropna().unique())
    year_selected = st.sidebar.multiselect("Año de remisión", years, default=years)
    df = df[df["AÑOREMISION"].isin(year_selected)]

# Filtro por municipio (asumiendo 'MUNICIPIO PROCEDENCIA')
if "MUNICIPIO PROCEDENCIA" in df.columns:
    municipios = sorted(df["MUNICIPIO PROCEDENCIA"].dropna().unique())
    municipio_selected = st.sidebar.multiselect("Municipio de procedencia", municipios, default=["MEDELLIN"] if "MEDELLIN" in municipios else municipios)
    df = df[df["MUNICIPIO PROCEDENCIA"].isin(municipio_selected)]

# --- VISTA GENERAL ---
st.subheader("Vista general de los datos filtrados")
st.write(f"Registros luego de filtros: **{len(df)}**")
st.dataframe(df.head(50))

# --- ESTADÍSTICAS CLAVE ---
st.subheader("Estadísticas básicas")

col1, col2, col3 = st.columns(3)

# 1. Casos de maltrato (TIPO ENTREGA contiene 'MALTRATO')
if "TIPO ENTREGA" in df.columns:
    maltrato_df = df[df["TIPO ENTREGA"].astype(str).str.contains("MALTRATO", case=False, na=False)]
    col1.metric("Casos de maltrato", len(maltrato_df))
else:
    col1.write("No se encontró la columna 'TIPO ENTREGA'.")

# 2. Tráfico de fauna (TIPO ENTREGA contiene 'TRAF')
if "TIPO ENTREGA" in df.columns:
    trafico_df = df[df["TIPO ENTREGA"].astype(str).str.contains("TRAF", case=False, na=False)]
    col2.metric("Casos de tráfico de fauna", len(trafico_df))

# 3. Total de casos (filtrados)
col3.metric("Total de casos (filtro aplicado)", len(df))

# --- DISTRIBUCIÓN POR CLASE (aves, reptiles, etc.) ---
if "CLASE" in df.columns:
    st.subheader("Distribución por clase (AVES, REPTILIA, MAMMALIA, etc.)")
    clase_counts = df["CLASE"].value_counts().reset_index()
    clase_counts.columns = ["CLASE", "CASOS"]
    st.bar_chart(clase_counts.set_index("CLASE"))
    st.dataframe(clase_counts)
else:
    st.info("No se encontró la columna 'CLASE' para hacer la distribución por categorías.")

# --- DISTRIBUCIÓN POR MUNICIPIO / COMUNA (si estuviera) ---
if "MUNICIPIO PROCEDENCIA" in df.columns:
    st.subheader("Casos por municipio de procedencia")
    mun_counts = df["MUNICIPIO PROCEDENCIA"].value_counts().reset_index()
    mun_counts.columns = ["MUNICIPIO", "CASOS"]
    st.bar_chart(mun_counts.set_index("MUNICIPIO"))
    st.dataframe(mun_counts)
