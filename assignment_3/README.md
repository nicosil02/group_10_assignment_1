# Assignment 3 - Grupo 10

**Dashboard:** _(enlace pendiente de despliegue)_

## Integrantes

| Nombre              | GitHub                                      |
|---------------------|----------------------------------------------|
| Nicolas Silva        | [@nicosil02](https://github.com/nicosil02)   |
| Marco Virú           | [@marcovirulucas](https://github.com/marcovirulucas)     |
| Estefanny Mejía      | [@estefmej](https://github.com/estefmej)     |
| Luz Supo             | [@lsupo](https://github.com/lsupo)     |

## Estructura

```
assignment_3/
├── visualizacion.ipynb   ← Parte 1: gráficos con Plotly
├── mapas.ipynb           ← Parte 2: mapas con Geopandas y Folium
├── app.py                ← Parte 3: dashboard en Streamlit
├── requirements.txt
├── README.md
└── datos/
    ├── dataset.csv                  ← tabla_final.csv del Assignment 2
    └── departamentos_peru.geojson   ← fronteras departamentales (sesión 7)
```

## 1. Pregunta

**¿El Estado declara emergencia donde más llueve?** Comparamos, para cada uno de los 25 departamentos, la lluvia de la temporada del 1 de enero al 31 de mayo de 2023 con el número de decretos de estado de emergencia por lluvias que lo mencionan.

## 2. Datos

Usamos la Opción B, nuestra `tabla_final.csv` del Assignment 2 (aquí `datos/dataset.csv`), con 25 filas y una por departamento.

- **Declaratorias y prórrogas:** decretos supremos de la PCM publicados en gob.pe, extraídos con Selenium y BeautifulSoup.
- **Lluvia:** API histórica de Open-Meteo. `lluvia_total_mm` es la lluvia acumulada en la capital del departamento y `dias_lluvia_fuerte` cuenta los días con 20 mm o más.
- **Fronteras:** `departamentos_peru.geojson` del curso (sesión 7). No trae ubigeo, así que se lo agregamos por nombre y luego cruzamos todo por `ubigeo` como texto de 2 dígitos.

## 3. Hallazgos

1. **No, al menos no en 2023.** La correlación entre lluvia y declaratorias es negativa (−0.24). Lima recibió 55 mm en su capital y es el departamento con más declaratorias (7). Madre de Dios recibió 1,248 mm y no tuvo ninguna.
2. **La lluvia está en la selva y las emergencias en la costa y la sierra.** Los cinco departamentos más lluviosos son Loreto, Ucayali, Madre de Dios, Áncash y San Martín. Los de más declaratorias son Lima, Áncash, Ayacucho, La Libertad y Arequipa. En 2023 hubo El Niño costero y el ciclón Yaku, y en zonas secas poca lluvia basta para causar huaicos e inundaciones.

## 4. Limitaciones

- La lluvia se mide en **un solo punto** (la capital), que no representa a todo el departamento. Por ejemplo, la sierra de Lima llueve mucho más que la ciudad.
- Contamos **decretos**, no su tamaño. Un decreto para 3 distritos pesa lo mismo que uno para 200.
- Identificamos los departamentos por su nombre en el título del decreto, así que pueden faltar los que solo aparecen en los anexos.
- Es una sola temporada y una comparación descriptiva, sin relación causal.

## Cómo correrlo

```bash
cd assignment_3
uv run streamlit run app.py
```
