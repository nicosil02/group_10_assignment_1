"""Dashboard de emergencias y lluvias por departamento.

Correr en local:
    uv run streamlit run app_2.py
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#--------------
# Configuración
#--------------
st.set_page_config(page_title="Emergencias y lluvias", page_icon="🌧️", layout="wide")

# Los archivos se buscan en la carpeta de este archivo, 
# porque Streamlit Cloud corre la app desde la raíz del repositorio.
CARPETA = Path(__file__).parent

# Nombres legibles para las columnas numéricas (se usan en filtros y gráficos)
VARIABLES = {
    "declaratorias": "Declaratorias de emergencia",
    "prorrogas": "Prórrogas",
    "lluvia_total_mm": "Lluvia total (mm)",
    "dias_lluvia_fuerte": "Días con lluvia ≥ 20 mm",
}

#-------------
# Cargar datos
#-------------
# @st.cache_data guarda el resultado: sin esto, el archivo se lee otra vez
# cada vez que alguien mueve un filtro y la app va lentísima.
@st.cache_data
def cargar_tabla():
    datos = pd.read_csv(CARPETA / "dataset.csv", dtype={"ubigeo": str})
    return datos

@st.cache_data
def cargar_mapa():
    """Lee distritos.geojson (Sesión 8) y une sus distritos en departamentos.

    Los 2 primeros dígitos del ubigeo distrital son el ubigeo del departamento:
    140106 (La Victoria, Chiclayo, Lambayeque) → "14" (Lambayeque).
    Todo se trabaja como TEXTO: si el ubigeo fuera número, 010101 sería 10101
    y sus 2 primeros dígitos darían "10" (Huánuco) en vez de "01" (Amazonas).
    """
    distritos = gpd.read_file(CARPETA / "distritos.geojson")
    distritos["ubigeo"] = distritos["ubigeo"].astype(str).str.zfill(6)
    distritos["ubigeo_depto"] = distritos["ubigeo"].str[:2]

    formas = (distritos[["ubigeo_depto", "geometry"]]
              .dissolve(by="ubigeo_depto", as_index=False)
              .rename(columns={"ubigeo_depto": "ubigeo"}))
    # Cuántos distritos dibujan cada departamento (para el hover del mapa)
    conteo = distritos["ubigeo_depto"].value_counts()
    formas["n_distritos"] = formas["ubigeo"].map(conteo)
    # Bordes más simples: el mapa carga más rápido y a esta escala no se nota
    formas["geometry"] = formas.geometry.simplify(0.005, preserve_topology=True)
    return formas, len(distritos)


datos = cargar_tabla()
formas, total_distritos = cargar_mapa()

#--------
# Filtros
#--------
st.sidebar.header("Filtros")

departamentos = sorted(datos["departamento"].unique())
elegidos = st.sidebar.multiselect(
    "Departamento", departamentos, default=departamentos,
    help="Por defecto se muestran los 25 departamentos.",
)

tope_lluvia = int(datos["lluvia_total_mm"].max()) + 1
lluvia_min, lluvia_max = st.sidebar.slider(
    "Lluvia total en la temporada (mm)", 0, tope_lluvia, (0, tope_lluvia), step=50,
)

solo_con_decretos = st.sidebar.checkbox("Solo departamentos con al menos una declaratoria")

variable_mapa = st.sidebar.selectbox(
    "Variable para el mapa", list(VARIABLES), format_func=VARIABLES.get,
)

filtrado = datos[
    datos["departamento"].isin(elegidos)
    & datos["lluvia_total_mm"].between(lluvia_min, lluvia_max)
]
if solo_con_decretos:
    filtrado = filtrado[filtrado["declaratorias"] > 0]

#-------
# Título
#-------
st.title("🌧️ ¿El Estado declara emergencia donde más llueve?")
st.caption(
    "Temporada de lluvias del 1 enero al 31 mayo de 2023 · Decretos supremos de la PCM (gob.pe) "
    "y lluvia diaria en cada capital departamental (Open-Meteo)"
)

if filtrado.empty:
    st.warning("No hay departamentos que cumplan los filtros. Ajusta la selección.")
    st.stop()

#---------
# Métricas
#---------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Departamentos", f"{len(filtrado)}")
c2.metric("Declaratorias", f"{int(filtrado['declaratorias'].sum())}",
          help="Un decreto que menciona 3 departamentos suma 1 a cada uno.")
c3.metric("Prórrogas", f"{int(filtrado['prorrogas'].sum())}")
c4.metric("Lluvia promedio (mm)", f"{filtrado['lluvia_total_mm'].mean():,.0f}")

st.divider()

#---------
# Gráficos
#---------
izq, der = st.columns(2)

with izq:
    if len(filtrado) >= 3 and filtrado["declaratorias"].nunique() > 1:
        r = filtrado["lluvia_total_mm"].corr(filtrado["declaratorias"])
        if r <= 0.1:
            titulo = f"Más lluvia no trae más declaratorias (r = {r:.2f})"
        elif r < 0.5:
            titulo = f"Algo más de declaratorias donde llueve más, pero la relación es débil (r = {r:.2f})"
        else:
            titulo = f"Donde más llueve, más declaratorias (r = {r:.2f})"
    else:
        titulo = "Lluvia vs. declaratorias (se necesitan al menos 3 departamentos para comparar)"

    st.subheader(titulo)
    fig = px.scatter(
        filtrado, x="lluvia_total_mm", y="declaratorias",
        text="departamento", size="dias_lluvia_fuerte", size_max=30,
        color="prorrogas", color_continuous_scale="Blues",
        hover_data={"capital": True, "dias_lluvia_fuerte": True},
        labels=VARIABLES | {"departamento": "Departamento", "capital": "Capital"},
    )
    fig.update_traces(textposition="top center", textfont_size=10)
    fig.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig, width="stretch")
    st.caption("Cada punto es un departamento. El tamaño indica los días con lluvia ≥ 20 mm.")

with der:
    lider = filtrado.sort_values(["declaratorias", "lluvia_total_mm"], ascending=False).iloc[0]
    mas_lluvia = filtrado.loc[filtrado["lluvia_total_mm"].idxmax()]
    if len(filtrado) == 1:
        titulo = (f"{lider['departamento']}: {int(lider['declaratorias'])} declaratorias "
                  f"con {lider['lluvia_total_mm']:.0f} mm de lluvia en su capital")
    elif lider["departamento"] == mas_lluvia["departamento"]:
        titulo = (f"{lider['departamento']} lidera en declaratorias ({int(lider['declaratorias'])}) "
                  f"y también es donde más llovió")
    else:
        titulo = (f"{lider['departamento']} lidera con {int(lider['declaratorias'])} declaratorias "
                  f"y {lider['lluvia_total_mm']:.0f} mm; {mas_lluvia['departamento']}, el más lluvioso, "
                  f"tuvo {int(mas_lluvia['declaratorias'])}")

    st.subheader(titulo)
    por_depto = filtrado.sort_values("declaratorias")
    fig = px.bar(
        por_depto, x="declaratorias", y="departamento", orientation="h",
        color="lluvia_total_mm", color_continuous_scale="Blues",
        labels=VARIABLES | {"departamento": ""},
    )
    fig.update_layout(template="plotly_white", height=450,
                      coloraxis_colorbar_title="Lluvia (mm)")
    st.plotly_chart(fig, width="stretch")
    st.caption("El color es la lluvia total: una barra larga y clara son muchas "
               "declaratorias con poca lluvia en la capital.")

#-----
# Mapa
#-----
# Cruce por ubigeo como TEXTO de 2 dígitos (no por nombre: "Áncash" vs "ANCASH")
cruce = formas.merge(filtrado, on="ubigeo", how="outer", indicator=True)
mapa = cruce[cruce["_merge"] == "both"]
sin_forma = filtrado[~filtrado["ubigeo"].isin(formas["ubigeo"])]

con_valor = filtrado  # el título usa los datos, aunque falte la forma en el mapa
maximo = con_valor.loc[con_valor[variable_mapa].idxmax()]
minimo = con_valor.loc[con_valor[variable_mapa].idxmin()]
if len(con_valor) == 1:
    st.subheader(f"{VARIABLES[variable_mapa]} en {maximo['departamento']}: "
                 f"{maximo[variable_mapa]:,.0f}")
else:
    st.subheader(
        f"{VARIABLES[variable_mapa]}: el valor más alto está en {maximo['departamento']} "
        f"({maximo[variable_mapa]:,.0f}) y el más bajo en {minimo['departamento']} "
        f"({minimo[variable_mapa]:,.0f})"
    )

if not mapa.empty:
    fig = px.choropleth_map(
        mapa,
        geojson=mapa.geometry,
        locations=mapa.index,
        color=variable_mapa,
        color_continuous_scale="Blues" if "lluvia" in variable_mapa else "YlOrRd",
        range_color=(datos[variable_mapa].min(), datos[variable_mapa].max()),
        map_style="carto-positron",
        zoom=4.3,
        center={"lat": -9.2, "lon": -75.0},
        opacity=0.75,
        hover_name="departamento",
        hover_data={"declaratorias": True, "prorrogas": True,
                    "lluvia_total_mm": True, "dias_lluvia_fuerte": True,
                    "n_distritos": True},
        labels=VARIABLES | {"n_distritos": "Distritos en el mapa"},
        height=600,
    )
else:
    fig = go.Figure()
    fig.update_layout(map_style="carto-positron", map_zoom=4.3,
                      map_center={"lat": -9.2, "lon": -75.0}, height=600)

# Los departamentos sin forma no desaparecen: se marcan en su capital
if not sin_forma.empty:
    fig.add_trace(go.Scattermap(
        lat=sin_forma["latitud"], lon=sin_forma["longitud"],
        mode="markers+text", text=sin_forma["departamento"], textposition="top right",
        marker={"size": 12, "color": "gray"},
        name="Sin forma en distritos.geojson",
        hovertext=[f"{d}: {VARIABLES[variable_mapa]} = {v:,.0f} (sin forma en el mapa)"
                   for d, v in zip(sin_forma["departamento"], sin_forma[variable_mapa])],
        hoverinfo="text",
    ))
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0),
                  legend={"x": 0.01, "y": 0.01, "bgcolor": "rgba(255,255,255,0.8)"})
st.plotly_chart(fig, width="stretch")

# Reporte del cruce: qué cruzó y qué no
st.caption(
    f"Cruce por ubigeo (texto de 2 dígitos): {len(mapa)} de {len(filtrado)} departamentos "
    f"seleccionados encontraron forma en distritos.geojson. Ese archivo trae solo "
    f"{total_distritos} distritos (los del ejemplo de dengue de la Sesión 8), así que cada "
    f"departamento se dibuja solo con esos distritos y puede verse incompleto."
)
if not sin_forma.empty:
    st.warning(
        "No cruzaron con el mapa (su ubigeo no aparece en distritos.geojson): "
        + ", ".join(f"{d} ({u})" for d, u in zip(sin_forma["departamento"], sin_forma["ubigeo"]))
        + ". Se muestran como puntos grises en su capital."
    )

#------
# Tabla
#------
st.subheader("Datos por departamento")

tabla = filtrado.copy()
tabla["mm_por_declaratoria"] = (
    tabla["lluvia_total_mm"] / tabla["declaratorias"].replace(0, pd.NA)
).astype("Float64").round(1)

st.dataframe(
    tabla.sort_values("declaratorias", ascending=False)[
        ["ubigeo", "departamento", "capital", "declaratorias", "prorrogas",
         "lluvia_total_mm", "dias_lluvia_fuerte", "mm_por_declaratoria"]
    ],
    width="stretch",
    hide_index=True,
    column_config={
        "lluvia_total_mm": st.column_config.NumberColumn("Lluvia total (mm)", format="%.1f"),
        "dias_lluvia_fuerte": "Días ≥ 20 mm",
        "mm_por_declaratoria": st.column_config.NumberColumn(
            "mm por declaratoria", help="Vacío si el departamento no tuvo declaratorias."),
    },
)

st.download_button(
    "Descargar datos filtrados (CSV)",
    tabla.to_csv(index=False).encode("utf-8-sig"),
    "lluvias_emergencias_2023.csv",
    "text/csv",
)