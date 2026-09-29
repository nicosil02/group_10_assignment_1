  # Assignment 2 - Grupo 10

  **Pregunta del trabajo:** *¿El Estado declara emergencia donde más llueve?*
  **Temporada asignada:** 1 de enero – 31 de mayo de **2023**

  ## Integrantes

  | Nombre              | GitHub                                      |
  |---------------------|----------------------------------------------|
  | Nicolas Silva        | [@nicosil02](https://github.com/nicosil02)   |
  | Marco Virú           | [@marcovirulucas](https://github.com/marcovirulucas)     |
  | Estefanny Mejía      | [@estefmej](https://github.com/estefmej)     |
  | Luz Supo             | [@lsupo](https://github.com/lsupo)     |

  ## Estructura del repositorio

  ```
  assignment_2/
  │
  ├── scraping_emergencias.ipynb
  ├── api_lluvias.ipynb
  ├── cruce_analisis.ipynb
  ├── bitacora_ia.md
  └── datos/
      ├── decretos_lluvias.csv
      ├── decretos_por_departamento.csv
      ├── lluvias_por_departamento.csv
      ├── ubigeos.csv
      └── tabla_final.csv
  ```

  ## Instrucciones del trabajo

  ### Parte 1 – Scraping de decretos de emergencia (`scraping_emergencias.ipynb`)

  Extraer con **Selenium** los decretos de emergencia de la PCM desde el buscador de gob.pe:

  ```text
  https://www.gob.pe/busquedas?contenido[]=normas&institucion[]=pcm&term=estado%20de%20emergencia%20precipitaciones&sort_by=recent&desde=DD-MM-AAAA&hasta=DD-MM-AAAA
  ```

  - Descargar e imprimir `robots.txt`, y explicar qué prohíbe y por qué conviene hacer pausas.
  - Abrir la búsqueda mes por mes usando `WebDriverWait`, con al menos 2 segundos entre páginas.
  - De cada `<article>`, extraer el número de la norma, la fecha de publicación, el título y el enlace.
  - **Verificación:** imprimir una tabla con `mes`, `resultados_totales` y `resultados_extraidos`. Los dos números deben coincidir.
  - Eliminar las normas repetidas y quedarse solo con los enlaces que contienen `/institucion/pcm/`.
  - Obtener el título completo de cada norma con `requests` + `BeautifulSoup`, con 1 segundo entre páginas.
  - Crear las columnas `es_lluvia`, `tipo` (`declara` / `prorroga` / `otro`) y `motivo` (`peligro inminente` / `impacto de daños` / `otro`).
  - Identificar los departamentos que menciona cada decreto con `re.search(r"\b" + departamento + r"\b", titulo)`, sin contar de más (por ejemplo, *Ica* dentro de *Huancavelica*) ni contar dos veces el mismo departamento.
  - Guardar `decretos_lluvias.csv` y `decretos_por_departamento.csv`.

  ### Parte 2 – API de lluvias (`api_lluvias.ipynb`)

  Obtener la lluvia de la capital de cada departamento con la API gratuita de **Open-Meteo**:

  - Leer la tabla de departamentos y capitales de Wikipedia con `requests` + `pd.read_html`.
  - **Verificación:** la tabla debe tener 25 filas (24 departamentos + Callao) y las capitales deben estar limpias (por ejemplo, Lima).
  - Obtener la latitud y longitud de cada capital con la API de geocodificación:
    ```text
    https://geocoding-api.open-meteo.com/v1/search?name=Chachapoyas&count=10&language=es
    ```
  - **Verificación:** todos los resultados deben estar en el Perú (`country_code == "PE"`) y en el departamento correcto (`admin1`).
  - Pedir la lluvia diaria de la temporada con la API histórica, con al menos 1 segundo entre pedidos:
    ```text
    https://archive-api.open-meteo.com/v1/archive?latitude=...&longitude=...&start_date=2023-01-01&end_date=2023-05-31&daily=precipitation_sum&timezone=America/Lima
    ```
  - Calcular `lluvia_total_mm` y `dias_lluvia_fuerte` (días con 20 mm o más).
  - **Verificación:** contar los días sin dato (`None`) y explicar qué se hizo con ellos.
  - Guardar `lluvias_por_departamento.csv`.

  ### Parte 3 – Cruce por ubigeo y análisis (`cruce_analisis.ipynb`)

  - Crear `ubigeos.csv` con los ubigeos departamentales oficiales del INEI (`01` Amazonas … `25` Ucayali).
  - Leerlo con y sin `dtype={"ubigeo": str}`, y explicar por qué importa la diferencia.
  - Agregar el `ubigeo` a las dos tablas y corregir los nombres de departamento que no coincidan.
  - Cruzar las tablas **por `ubigeo`** (no por nombre).
  - **Verificación:** la tabla final debe tener 25 filas, con **0** en los departamentos sin declaratorias.
  - Guardar `tabla_final.csv`, con el `ubigeo` como texto de 2 dígitos.
  - Hacer dos gráficos con **Plotly**:
    - un gráfico de dispersión de `lluvia_total_mm` vs `declaratorias`, con el nombre de cada departamento;
    - un gráfico de barras con los 10 departamentos con más declaratorias.
  - Responder:
    1. ¿Cuáles fueron los 3 departamentos con más declaratorias? ¿Coinciden con los 3 donde más llovió?
    2. ¿Hay departamentos con mucha lluvia y pocas declaratorias, o al revés? ¿Por qué?
    3. ¿Qué porcentaje de las declaratorias fue por *peligro inminente* y qué porcentaje por *impacto de daños*?
    4. Tres limitaciones del análisis.
    5. Conclusión (5 a 8 líneas).

  ### Parte 4 – Bitácora de IA (`bitacora_ia.md`)

  Registrar al menos **3 momentos** en que la IA dio algo incorrecto, incompleto o que no funcionó. Al menos uno debe ser de la Parte 1 y otro de la Parte 2. Para cada uno:

  1. ¿Qué se le pidió a la IA?
  2. ¿Qué respondió?
  3. ¿Qué estaba mal y cómo nos dimos cuenta?
  4. ¿Cómo se corrigió?
