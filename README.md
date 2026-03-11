# ⚽ Reporte Analítico: Sistema de Análisis de Resultados Históricos de Fútbol

¡Bienvenidos! Este repositorio contiene el proyecto de la **Fase 4**, donde desarrollé una aplicación full-stack interactiva orientada al **Análisis de Datos (Data Science)**. 

Para demostrar la capacidad técnica y analítica del sistema, seleccioné una base de datos histórica de resultados de fútbol internacional. A continuación, presento el informe técnico y el **Análisis Exploratorio de Datos (EDA)** real generado por mi aplicación sobre este dataset.

---

## 📖 1. Introducción al Dataset y Contexto

El dataset elegido contiene un registro exhaustivo de partidos de fútbol internacional. Fue procesado en el backend mediante un motor construido en `Python` con `Pandas` y expuesto a través de una API en `FastAPI`. 

Al subir el archivo CSV al Dashboard, el sistema perfiló automáticamente la base de datos arrojando la siguiente radiografía general:

*   **Volumen de Datos:** El archivo contiene un total exacto de **49.071** registros (partidos) y **9** variables estructuradas (columnas).
*   **Limpieza de Datos:** Tras el análisis automatizado, se confirmó una calidad de datos del 100%, con **0 valores nulos** y **0 filas duplicadas**, lo que garantizó un análisis estadístico muy preciso.

---

## 📊 2. Análisis Exploratorio de Datos (EDA) y Hallazgos Reales

Gracias al perfilado matemático de Pandas en el backend web, pudimos extraer estadísticas tanto descriptivas (numéricas) como de frecuencias (categóricas) de las variables de nuestro interés.

### 2.1 Estadísticas Descriptivas (Goles y Rendimiento)
Al analizar el comportamiento anotador a lo largo de los casi 50 mil partidos, descubrimos una fuerte tendencia general hacia la "ventaja de la localía":

*   **Goles Locales (`home_score`):** Los equipos que juegan en casa anotan en promedio **1.75 goles** por partido. El 50% de las veces (la Mediana), marcan al menos 1 gol, pero se han llegado a registrar partidos atípicos con una victoria máxima de **31 goles** anotados por el local. Las matemáticas detectaron 6,284 valores atípicos (outliers) históricos.
*   **Goles Visitantes (`away_score`):** En contraste, ser visitante impacta fuertemente el rendimiento. El promedio cae a **1.18 goles** por partido, y en el 25% de los partidos (Primer Cuartil), el equipo visitante se va sin anotar un solo gol (0). 

*Puedes observar la distribución completa en los gráficos guardados en la carpeta `outputs/dist_home_score.png` y los diagramas de caja en `outputs/boxplot_home_score.png`.*

### 2.2 Variables Categóricas y Frecuencias (Torneos y Escenarios)
El motor también extrajo el Top 10 de comportamiento para cada variable de texto puro:

*   **¿Qué torneos se juegan más?:** De los 49.071 partidos de la historia, la inmensa mayoría corresponden a **Amistosos (Friendly)** con 18.181 encuentros. Muy por debajo están las Clasificatorias al Mundial de la FIFA (8.755) y la Clasificación a la Eurocopa (2.824). _(Ver `outputs/categorica_tournament.png` para el gráfico del top 10)._
*   **Potencias Locales:** La selección que más veces ha jugado de local históricamente en esta base de datos es **Brasil** (610 partidos), seguida casi un empate técnico por **Argentina** (599) y **México** (596). _(Ver `outputs/categorica_equipo_local.png`)_
*   **Sedes Internacionales:** Curiosamente, el reporte arrojó que **Estados Unidos** es históricamente el país que más partidos ha albergado (1.472), muy por encima de Francia (912) e Inglaterra (761), probablemente debido al alto volumen de giras de amistosos y Copa América en occidente.

---

## 📈 3. El Explorador Visual (Gráficos Interactivos)

Toda esta información cruda fue enviada e inyectada al frontend mediante JSON (con un límite seguro de visualización), permitiendo construir nuestro **Explorador Visual con Javascript**.

Nuestra interfaz web permite cruzar estas variables dinámicamente usando diferentes representaciones matemáticas, como:

1.  **Gráficos de Barras / Áreas (Comparativas):** Usados en la interfaz para enfrentar, por ejemplo, los Continentes o Torneos en el Eje X contra la sumatoria total de goles en el Eje Y, descubriendo qué competiciones son más goleadoras.
2.  **Gráfico de Líneas (Tendencias Temporales):** En el dashboard web, cruzando la variable `fecha` procesada contra los goles promedio por año, este gráfico demostró cómo el promedio de goles ha variado por décadas, identificando años dorados ofensivos.
3.  **Gráficos de Pastel Dinámicos (Proporciones):** Sirven para responder preguntas como *"De todos los partidos jugados en la historia, ¿qué porcentaje representa las Clasificatorias al mundial?"*. Nuestra aplicación recalcula este porcentaje exacto on-the-fly frente a los filtros que aplique el usuario.

---

## ⚙️ 4. Arquitectura del Proyecto y Memoria API (CRUD)

Detrás de este informe estadístico corre una arquitectura moderna programada desde cero.

### Componentes Principales:
*   **Motor Analítico (Backend):** Programado en Python (`procesamiento_universal.py` y `main.py`). Se usa `FastAPI` para levantar un servidor veloz, y `Pandas` para hacer el perfilado y análisis que leyeron arriba en formato de Dataframe en milisegundos. Validamos tipos de datos usando `Pydantic` (`schemas.py`).
*   **Interfaz Dinámica (Frontend):** Programado en HTML5 nativo (`interfaz_premium.html`), decorado con `TailwindCSS` en modo Dark UI, y gráficos inyectados en vivo mediante lógica de `Chart.js` y JavaScript. Todo el cruce de datos y filtrado ocurre en el navegador del usuario para no sobrecargar el servidor.

### Endpoints de API requeridos (Cumplimiento de Rúbrica Fase 4)
Este sistema no solo analiza datos; también guarda y maneja los reportes en una Memoria RAM temporal mediante **4 Endpoints CRUD** RESTful que pueden comprobarse en vivo en la *Pestaña 4: Memoria API* de la aplicación:

1.  **POST `/analizar/csv`:** Sube el archivo base, inyecta Pandas, extrae JSONs y gráficos, y guarda el reporte estructurado de los casi 50.000 de registros en la memoria del backend.
2.  **GET `/historial`:** Lista el maestro de todos los análisis y DataFrames que hemos guardado hoy y los muestra en una lista.
3.  **GET `/historial/{id}`:** Endpoint con paso de variable en la ruta para invocar los datos específicos de un análisis anterior, redibujando los gráficos sin volver a subir el CSV.
4.  **DELETE `/historial/{id}`:** Simula una petición de eliminación, limpiando en tiempo real esos casi 4MB de memoria RAM directamente del servidor en Python.

---

### Instrucciones de Ejecución Local
Para evaluar la plataforma y probar el EDA conectando backend y frontend tú mismo:

1. Instalar dependencias requeridas (FastAPI, Pandas, Uvicorn, etc):
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
2. Levantar el servidor backend localmente:
   \`\`\`bash
   python -m uvicorn main:app --reload
   \`\`\`
3. Abrir el archivo **`interfaz_premium.html`** directamente en Google Chrome o Edge.
4. Subir la base de datos CSV en la primera pestaña y disfrutar.
