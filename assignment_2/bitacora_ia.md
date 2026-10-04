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
