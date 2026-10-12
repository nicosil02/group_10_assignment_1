# 🌧️ ¿El Estado declara emergencia donde más llueve? – Dashboard 2023

**Grupo 10** · Fundamentos de Python · Assignment 3

🔗 **App publicada:** [[Por completar](https://assignment3g10.streamlit.app/)]

Dashboard en Streamlit que compara, para los 25 departamentos del Perú, cuántas **declaratorias de Estado de Emergencia por lluvias** emitió la PCM entre el 1 de enero y el 31 de mayo de 2023 con **cuánto llovió** en cada departamento en ese mismo periodo. Tiene filtros por departamento y por rango de lluvia, métricas que cambian con la selección, un gráfico de dispersión, un gráfico de barras, un mapa departamental y la tabla de datos descargable.

## 1. Pregunta

**¿El Estado declara emergencia donde más llueve?** Es decir: en la temporada de lluvias 2023, ¿los departamentos con más lluvia son los que recibieron más declaratorias de emergencia?

## 2. Datos

| Archivo | Contenido | Fuente |
|---|---|---|
| `dataset.csv` | 25 filas, una por departamento: `ubigeo`, `departamento`, `capital`, `latitud`, `longitud`, `lluvia_total_mm`, `dias_lluvia_fuerte`, `declaratorias`, `prorrogas` | Construida en el Assignment 2 |
| `distritos.geojson` | 475 distritos con su `ubigeo` de 6 dígitos. La app los une en departamentos usando los 2 primeros dígitos | Material de la Sesión 8 |

¿Cómo se construyó `dataset.csv` (es la `tabla_final.csv` del Assignment 2)?:

- **Decretos:** scraping con Selenium del buscador de normas de [gob.pe](https://www.gob.pe/busquedas) (PCM, *"estado de emergencia precipitaciones"*, enero–mayo 2023). Nos quedamos con las normas de lluvias y contamos los departamentos que menciona cada título, una vez por decreto.
- **Lluvia:** API histórica de [Open-Meteo](https://open-meteo.com/). Es la lluvia diaria en la **capital** de cada departamento: `lluvia_total_mm` es la suma de la temporada y `dias_lluvia_fuerte` son los días con 20 mm o más.
- **Cruce:** por `ubigeo` del INEI (texto de 2 dígitos), no por nombre.

**Ojo con el mapa:** `distritos.geojson` es el archivo del ejemplo de dengue y no trae todos los distritos del Perú. Al cruzar por ubigeo como texto, **21 de los 25 departamentos** encontraron forma. **Apurímac (03), Arequipa (04), Huancavelica (09) y Tacna (23)** no tienen ningún distrito en el archivo, así que la app los reporta en un aviso debajo del mapa y los marca como puntos grises en su capital. Los demás departamentos se dibujan solo con los distritos que trae el archivo, por eso algunos se ven incompletos.

## 3. Hallazgos

1. **No: más lluvia no significa más declaratorias.** Los tres departamentos con más declaratorias fueron **Lima (7)**, **Áncash (6)** y **Ayacucho y La Libertad (5 cada uno)**. Los tres con más lluvia fueron **Loreto (1 605 mm)**, **Ucayali (1 316 mm)** y **Madre de Dios (1 248 mm)**: no coincide ninguno. La correlación entre lluvia total y declaratorias es incluso **ligeramente negativa (r = −0.24)**.
2. **Los casos extremos están en lados opuestos del país.** **Madre de Dios** tuvo 23 días de lluvia fuerte y **ninguna** declaratoria; **Loreto**, 26 días y solo una. En cambio, en **Lima** se midieron apenas 55.5 mm en la capital y tuvo **7** declaratorias. En 2023, con el ciclón Yaku, poca lluvia en la costa bastó para activar quebradas y huaicos en zonas que no están preparadas para ella, mientras que en la Amazonía mucha lluvia es lo normal de la temporada.

## 4. Limitaciones

- **La lluvia se mide en un solo punto por departamento (la capital).** En Lima se usa la ciudad de Lima, en la costa, pero las declaratorias cubren distritos de varias provincias del departamento, incluidas zonas andinas donde la lluvia puede ser muy distinta. Lima y Callao tienen exactamente el mismo valor (55.5 mm), probablemente porque caen en la misma celda de la grilla de Open-Meteo.
- **Una declaratoria no mide el tamaño de la emergencia.** Un decreto suma 1 a cada departamento que menciona, ya sea un distrito o veinte, y uno que nombra 16 departamentos pesa lo mismo para cada uno.
- **La emergencia depende del daño, no solo de la lluvia.** Influyen la vulnerabilidad (viviendas en quebradas, falta de drenaje), la población expuesta y la capacidad del gobierno regional para pedir la declaratoria. Nada de eso está en los datos.
- **La clasificación de los decretos se hizo por texto del título.** Una norma cuyo título no menciona lluvias queda fuera. Revisamos los casos dudosos y corregimos a mano el DS 036-2023-PCM, pero puede quedar algún error.
- **El mapa es incompleto:** `distritos.geojson` no cubre Apurímac, Arequipa, Huancavelica ni Tacna, y de los otros departamentos solo trae algunos distritos. El mapa sirve para ubicar los valores, no para ver la extensión real de cada departamento.
- **Es una sola temporada (2023)**, atípica por el ciclón Yaku y El Niño costero, así que los resultados no se pueden generalizar a otros años.

## Cómo correrla en local

```bash
cd assignment_3
uv run streamlit run app.py
```

Archivos necesarios en la misma carpeta: `app.py`, `dataset.csv`, `distritos.geojson` y `requirements.txt`.
