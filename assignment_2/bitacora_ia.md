# Bitácora de IA – Grupo 10

Momentos en los que la IA nos dio algo incorrecto, incompleto o que no funcionó, y cómo lo corregimos.

---

## Momento 1 – Parte 1: el filtro de la búsqueda no bastaba para quedarse solo con la PCM

**1. ¿Qué se le pidió a la IA?**
Que escribiera el código con Selenium para recorrer la búsqueda de gob.pe mes por mes (enero a mayo de 2023) y extraer de cada `<article>` el número, la fecha, el título y el enlace.

**2. ¿Qué respondió?**
Un código que abría la URL con `institucion[]=pcm` y guardaba todos los resultados. Según la IA, como la URL ya filtraba por PCM, todos los resultados iban a ser de la PCM y no hacía falta filtrar nada más.

**3. ¿Qué estaba mal y cómo nos dimos cuenta?**
Al revisar los enlaces vimos que el buscador también devolvía normas de **otras instituciones**: cuatro resoluciones del Tribunal de Contrataciones (`/institucion/oece/...`, por ejemplo la Resolución N.° 0209-2023-TCE-S1) y dos **Directivas de 2015** (005 y 004-2015-PCM/SGRD), que no son de nuestra temporada. Nos dimos cuenta al imprimir la tabla y ver números de norma que no empezaban con "Decreto Supremo".

**4. ¿Cómo se corrigió?**
Agregamos el filtro pedido en el enunciado: nos quedamos solo con los enlaces que contienen `/institucion/pcm/` (se eliminaron 4 normas, quedaron 49). Las dos directivas de 2015 quedaron fuera después, porque sus títulos no mencionan lluvias ni precipitaciones (`es_lluvia = False`).

---

## Momento 2 – Parte 1: el título completo del DS 036-2023-PCM salió incorrecto

**1. ¿Qué se le pidió a la IA?**
Una función con `requests` + `BeautifulSoup` para entrar a la página de cada norma y sacar el título completo, ya que en la búsqueda los títulos venían cortados con "...".

**2. ¿Qué respondió?**
La función `titulo_completo()`, que toma el texto de `<div class="description">` y le quita el texto del botón de descarga. La IA dijo que ese `div` siempre tenía el título de la norma.

**3. ¿Qué estaba mal y cómo nos dimos cuenta?**
Funcionó para casi todas las normas, pero no para el **DS 036-2023-PCM**: su página solo dice *"Declaratoria de Estado de Emergencia"* más texto del PDF, sin el lugar ni el motivo. Por eso el decreto quedaba con `es_lluvia = False` y se perdía del análisis, aunque sí era un decreto por lluvias. Lo detectamos al revisar uno por uno los decretos clasificados como `"otro"`.

**4. ¿Cómo se corrigió?**
Abrimos el PDF de la norma, copiamos el título real de la primera página (declaratoria en Ancón, Pucusana, Punta Hermosa, Punta Negra, San Bartolo y Santa María del Mar, Lima, *por impacto de daños ante intensas precipitaciones pluviales*) y lo corregimos a mano en el notebook antes de clasificar. Con eso el decreto pasó a `es_lluvia = True`.

---

## Momento 3 – Parte 1: contar departamentos con `in` contaba mal (Ica dentro de Huancavelica)

**1. ¿Qué se le pidió a la IA?**
Que identificara qué departamentos menciona cada decreto.

**2. ¿Qué respondió?**
Una primera versión que pasaba el título a minúsculas y buscaba cada departamento con `in` (`"ica" in titulo.lower()`).

**3. ¿Qué estaba mal y cómo nos dimos cuenta?**
`"huancavelica"` termina en `"ica"`, así que cualquier decreto que mencionara Huancavelica también sumaba una declaratoria a **Ica**. Lo vimos con el **DS 008-2023-PCM**, que nombra Huancavelica pero no Ica, y aun así aparecía Ica en la lista. Además, algunos títulos escriben "Ancash", "Junin" o "San Martin" sin tilde y esos no se detectaban.

**4. ¿Cómo se corrigió?**
Cambiamos a `re.search(r"\b" + departamento + r"\b", titulo)` sobre el **título original** (con mayúsculas), como pide el enunciado, e hicimos que las vocales con tilde aceptaran las dos formas (`Á` → `[ÁA]`). Lo probamos con casos de control: "Huancavelica" → solo Huancavelica; "provincia de Ica del departamento de Ica" → Ica una sola vez; "Ancash, Junin y San Martin" → los tres.

---

## Momento 4 – Parte 2: la tabla de Wikipedia no tenía 25 filas y Lima tenía una capital rara

**1. ¿Qué se le pidió a la IA?**
Leer con `pd.read_html` la tabla de departamentos y capitales de Wikipedia.

**2. ¿Qué respondió?**
Un código que tomaba `tablas[1]` con las columnas `Departamento` y `Capital` y lo daba por terminado, diciendo que ahí estaban los 25 departamentos.

**3. ¿Qué estaba mal y cómo nos dimos cuenta?**
Al hacer la verificación pedida (`len(capitales)`), salieron **24 filas**: faltaba el **Callao**, que en Wikipedia está en otra tabla (provincias de régimen especial). Además, la capital de Lima aparecía como **"Huacho (de facto)"**, un texto que la API de geocodificación no iba a encontrar y que no es la ciudad que queríamos medir.

**4. ¿Cómo se corrigió?**
Agregamos el Callao a mano con los datos de `tablas[3]` (capital: Callao) y reemplazamos "Huacho (de facto)" por **Lima**. Después volvimos a verificar: 25 filas. En la geocodificación también tuvimos que normalizar `admin1` (venía como "Departamento de Cusco", "Ancash" sin tilde, "Provincia Constitucional del Callao") para poder comprobar que cada capital estaba en su departamento; con eso, 0 filas sin coincidir.

**Momento 1 – Parte 1: el DS 036-2023-PCM quedaba fuera de las normas de lluvias**

**1. ¿Qué se le pidió a la IA?**
Que leyera el título completo de cada norma con requests y BeautifulSoup desde div.description y que quitara el texto extra del final ("DS N° ... PDF ... Descargar").

**2. ¿Qué respondió?**
En python
def limpiar_titulo(texto):
    texto = re.sub(r"\s+", " ", texto).strip()
    limpio = PATRON_EXTRA.sub("", texto).strip()
    return limpio if len(limpio) >= 40 else texto

**3. ¿Qué estaba mal y cómo nos dimos cuenta?**
3. El código asumía que div.description siempre trae el título real de la norma. En el DS 036-2023-PCM solo traía:

Declaratoria de Estado de Emergencia DS N° 036-2023-PCM.pdf PDF 1.5 MB Descargar

Como el texto limpio era muy corto, la función devolvía el texto sin limpiar. Ese título no menciona lluvias, así que el decreto quedaba con es_lluvia = False, motivo = "otro" y sin departamento: se perdía un decreto de lluvias.

Nos dimos cuenta al revisar las filas con motivo = "otro" (paso 10). Era el único título que no decía ni dónde ni por qué se declaraba la emergencia. Abrimos el PDF y su título real es "...distritos de Ancón, Pucusana, Punta Hermosa, Punta Negra, San Bartolo y Santa María del Mar de la provincia y departamento de Lima, por impacto de daños ante intensas precipitaciones pluviales". Además, el considerando menciona el ciclón Yaku.

**4. ¿Cómo se corrigió?**
Agregamos una celda de corrección manual antes de la clasificación, donde reemplazamos el titulo_completo del DS 036 por el título copiado del PDF. Al volver a correr, el decreto quedó como declara, impacto de daños y departamento Lima. Dejamos explicada la corrección en el notebook.

**Momento 2 – Parte 1: la primera corrección que propuso la IA estaba incompleta**

**1. ¿Qué se le pidió a la IA?**
1. Cómo corregir el DS 036 si al revisar el PDF resultaba ser de lluvias.

**2. ¿Qué respondió?**
En python
# Corrección manual: la página del DS 036 no trae el título real (revisado en el PDF)
fila = decretos["numero"].str.contains("036-2023-PCM")
decretos.loc[fila, "es_lluvia"] = True

**3. ¿Qué estaba mal y cómo nos dimos cuenta?**
Cambiar solo es_lluvia hacía que el decreto pasara el filtro del paso 11, pero tipo, motivo y los departamentos también se calculan a partir del título. Con el título vacío, el DS 036 habría quedado con motivo = "otro" y sin departamento, así que no habría sumado ninguna declaratoria a Lima en decretos_por_departamento.csv. Nos dimos cuenta al revisar qué columnas dependían del título después de abrir el PDF.

**4. ¿Cómo se corrigió?**
En vez de cambiar una sola columna, reemplazamos el título antes de la clasificación (ver Entrada 1). Así las columnas es_lluvia, tipo, motivo y departamentos se recalculan solas con el mismo código que usan las demás normas.


**Momento 3 – Parte 1: el filtro por PCM dejaba pasar directivas de 2015**

**1. ¿Qué se le pidió a la IA?**
Que quitara las normas de otras instituciones, quedándonos solo con las que tienen /institucion/pcm/ en el enlace (paso 8).

**2. ¿Qué respondió?**
En python
es_pcm = decretos["enlace"].str.contains("/institucion/pcm/", na=False)
decretos = decretos[es_pcm].reset_index(drop=True)

**3. ¿Qué estaba mal y cómo nos dimos cuenta?**
 El filtro por institución funciona, pero no basta para quedarse solo con los decretos de la temporada. Al revisar las normas con motivo = "otro" aparecieron dos Directivas de 2015 (Directiva N.° 005-2015-PCM/SGRD y N.° 004-2015-PCM/SGRD, sobre simulacros por el Fenómeno El Niño). Son de la PCM, así que pasaron el filtro, pero no son decretos de emergencia de 2023. El buscador las devolvió porque su texto incluye "declarados en Estado de Emergencia".

**4. ¿Cómo se corrigió?**
Comprobamos que estas directivas no mencionan lluvias ni precipitaciones, así que el filtro es_lluvia del paso 11 las elimina. Lo verificamos con otros["es_lluvia"].value_counts(): de las 28 normas con motivo = "otro", 26 son False y solo 2 son de lluvias (DS 043 y DS 065). Dejamos anotado en el notebook que el filtro por institución no garantiza que todas las normas sean decretos de la temporada.