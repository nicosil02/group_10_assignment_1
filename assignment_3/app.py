"""Dashboard: ¿El Estado declara emergencia donde más llueve? (ene-may 2023).

Correr en local, desde la carpeta assignment_3/:
    uv run streamlit run app.py
"""

import unicodedata
from pathlib import Path

import geopandas as gpd
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------------- configuracion
st.set_page_config(page_title="Lluvias y emergencias", page_icon="🌧️", layout="wide")

# Streamlit Cloud corre la app desde la raíz del repositorio, no desde esta
# carpeta: por eso las rutas se arman a partir de donde vive este archivo.
CARPETA = Path(__file__).parent


def normalizar(texto):
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.split())


# ------------------------------------------------------------------ carga datos
# Sin @st.cache_data el archivo se volvería a leer cada vez que se mueve un filtro.
@st.cache_data
def cargar():
    # El ubigeo se lee como texto: como número, "01" se vuelve 1 y el mapa no cruza.
    datos = pd.read_csv(CARPETA / "datos" / "dataset.csv", dtype={"ubigeo": str})

    # El GeoJSON solo trae el nombre (ANCASH, JUNIN...). Le pegamos el ubigeo
    # con una llave sin tildes y luego todo cruza por ubigeo.
    formas = gpd.read_file(CARPETA / "datos" / "departamentos_peru.geojson")
    llaves = datos[["ubigeo", "departamento"]].copy()
    llaves["llave"] = llaves["departamento"].apply(normalizar)
    formas["llave"] = formas["departamento"].apply(normalizar)
    formas = formas[["llave", "geometry"]].merge(llaves[["llave", "ubigeo"]], on="llave")
    formas = formas.merge(datos, on="ubigeo")
    return datos, formas


datos, formas = cargar()

# ----------------------------------------------------------------------- filtros
st.sidebar.header("Filtros")

departamentos = sorted(datos["departamento"].unique())
elegidos = st.sidebar.multiselect("Departamento", departamentos, default=departamentos)

lluvia_minima = st.sidebar.slider(
    "Lluvia acumulada mínima (mm)", 0, int(datos["lluvia_total_mm"].max()), 0, step=50
)

variables = {
    "Lluvia acumulada (mm)": "lluvia_total_mm",
    "Días con lluvia fuerte (≥ 20 mm)": "dias_lluvia_fuerte",
    "Declaratorias de emergencia": "declaratorias",
    "Prórrogas": "prorrogas",
}
nombre_variable = st.sidebar.selectbox("Variable del mapa", list(variables))
variable = variables[nombre_variable]

filtrado = datos[
    datos["departamento"].isin(elegidos) & (datos["lluvia_total_mm"] >= lluvia_minima)
]

# ------------------------------------------------------------------------ titulo
st.title("🌧️ ¿El Estado declara emergencia donde más llueve?")
st.caption(
    "Temporada 1 de enero – 31 de mayo de 2023 · Fuente: decretos supremos de la PCM "
    "(gob.pe) y lluvia diaria de Open-Meteo en la capital de cada departamento · Grupo 10"
)

if filtrado.empty:
    st.warning("Ningún departamento cumple los filtros. Ajusta la selección.")
    st.stop()

# ---------------------------------------------------------------------- metricas
c1, c2, c3, c4 = st.columns(4)
c1.metric("Departamentos", len(filtrado))
c2.metric("Declaratorias", int(filtrado["declaratorias"].sum()))
c3.metric("Lluvia promedio", f"{filtrado['lluvia_total_mm'].mean():,.0f} mm")
c4.metric(
    "Con al menos una declaratoria",
    f"{(filtrado['declaratorias'] > 0).mean():.0%}",
)

st.divider()

# ---------------------------------------------------------------------- graficos
izq, der = st.columns(2)

with izq:
    st.subheader("Declaratorias por departamento")
    fig = px.bar(
        filtrado.sort_values("declaratorias"),
        x="declaratorias", y="departamento", orientation="h",
        color="lluvia_total_mm", color_continuous_scale="Blues",
        labels={"declaratorias": "Declaratorias", "departamento": "",
                "lluvia_total_mm": "Lluvia (mm)"},
    )
    fig.update_layout(template="plotly_white", height=500)
    st.plotly_chart(fig, width="stretch")
    st.caption("El color es la lluvia: las barras más largas no son las más azules.")

with der:
    st.subheader("Lluvia vs. declaratorias")
    fig = px.scatter(
        filtrado, x="lluvia_total_mm", y="declaratorias",
        size="dias_lluvia_fuerte", size_max=30, hover_name="departamento",
        labels={"lluvia_total_mm": "Lluvia acumulada (mm)",
                "declaratorias": "Declaratorias",
                "dias_lluvia_fuerte": "Días ≥ 20 mm"},
    )
    fig.update_layout(template="plotly_white", height=500)
    st.plotly_chart(fig, width="stretch")
    st.caption(f"Correlación en la selección: {filtrado['lluvia_total_mm'].corr(filtrado['declaratorias']):.2f}")

# -------------------------------------------------------------------------- mapa
st.subheader(f"Mapa: {nombre_variable.lower()}")

formas_filtradas = formas[formas["ubigeo"].isin(filtrado["ubigeo"])]

fig = px.choropleth_map(
    formas_filtradas,
    geojson=formas_filtradas.geometry,
    locations=formas_filtradas.index,
    color=variable,
    color_continuous_scale="Reds" if variable in ("declaratorias", "prorrogas") else "Blues",
    map_style="carto-positron",
    zoom=4.3,
    center={"lat": -9.2, "lon": -75.0},
    opacity=0.75,
    hover_name="departamento",
    hover_data={"lluvia_total_mm": True, "dias_lluvia_fuerte": True,
                "declaratorias": True, "prorrogas": True},
    labels={"lluvia_total_mm": "Lluvia (mm)", "dias_lluvia_fuerte": "Días ≥ 20 mm",
            "declaratorias": "Declaratorias", "prorrogas": "Prórrogas"},
    height=600,
)
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, width="stretch")

# ------------------------------------------------------------------------- tabla
st.subheader("Datos por departamento")

tabla = filtrado.copy()
tabla["declaratorias_por_100mm"] = (tabla["declaratorias"] / tabla["lluvia_total_mm"] * 100).round(2)

st.dataframe(
    tabla.sort_values("declaratorias", ascending=False)[
        ["ubigeo", "departamento", "capital", "lluvia_total_mm", "dias_lluvia_fuerte",
         "declaratorias", "prorrogas", "declaratorias_por_100mm"]
    ],
    width="stretch",
    hide_index=True,
)

st.download_button(
    "Descargar datos filtrados (CSV)",
    tabla.to_csv(index=False).encode("utf-8"),
    "lluvias_emergencias_filtrado.csv",
    "text/csv",
)
