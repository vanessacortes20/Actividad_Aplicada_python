# 📊 Universal Analytical API & Dynamic Dashboard

Un ecosistema completo de Análisis de Datos construido en **Python (FastAPI + Pandas)** con un Frontend dinámico e interactivo. Este proyecto permite a los usuarios subir cualquier archivo CSV, y mediante un motor de inferencia matemática, la API calcula automáticamente estadísticas descriptivas que son renderizadas "al vuelo" en un Dashboard web oscuro y premium. 

Desarrollado originalmente para analizar Partidos Históricos de Fútbol Internacional, el motor fue refactorizado para ser **100% agnóstico**, capaz de perfilar ventas, mediciones climáticas o cualquier data tabular estructurada.

---

## ⚽ Contexto del Proyecto y Dataset Original
Este motor fue construido y testeado utilizando una extensa base de datos histórica del **Fútbol Internacional (1872 - 2024)**. El archivo CSV original (`dataset_espanol.csv`) contiene registros detallados de decenas de miles de partidos oficiales y amistosos.

### 🎯 Objetivos del Proyecto (Fase Analítica)
1. **Limpieza de Datos:** Estandarizar nombres de equipos y torneos, manejando valores nulos en locaciones.
2. **Análisis Exploratorio (EDA):** Extraer métricas descriptivas clave como los promedios de goles históricos, torneos más frecuentes y ciudades sede predominantes.
3. **Despliegue Dinámico:** Construir una API robusta que automatice este análisis matemático mediante Pandas y lo sirva a una interfaz gráfica web.

### 📈 Hallazgos Clave del Análisis Descriptivo
Al someter el dataset al motor de Pandas, se revelaron los siguientes hallazgos principales (visualizables en la pestaña *Explorador Interactivo* del Dashboard):
* **Frecuencia de Torneos:** La abrumadora mayoría de los registros históricos corresponden a partidos *Amistosos (Friendly)*, superando por amplio margen a eventos formales como Clasificatorias Mundialistas o la Copa del Mundo en sí.
* **Ciudades Sede Predominantes:** Ciudades europeas y latinoamericanas como *Kuala Lumpur*, *Doha* y *Londres* lideran históricamente la organización de partidos, sirviendo como hubs neutrales o recurrentes.
* **Tendencia de Goleo:** El promedio de goles combinados ha ido fluctuando drásticamente a lo largo de las décadas (mayor goleo a principios del siglo XX, estabilizándose hacia épocas modernas).
* **Factor de Localía (Top Equipos):** Existe una tendencia estadísticamente marcada donde el `Ganador` coincide con el `Equipo Local`, impulsando el diseño de las variables predictivas del proyecto.

---

## 🏗️ Arquitectura y Tecnologías
El proyecto se divide en dos capas fuertemente desacopladas:

### Backend (Data Science API)
* **[FastAPI](https://fastapi.tiangolo.com/):** Framework moderno y asíncrono para construir la API RESTful.
* **[Pydantic](https://docs.pydantic.dev/):** Garantiza la integridad de los datos mediante validación estricta de tipos e inputs.
* **[Pandas](https://pandas.pydata.org/):** El motor principal de procesamiento. Infiere tipos de datos numéricos y categóricos, gestiona nulos y ejecuta agregaciones estadísticas (Mediana, Desviación Estándar, Frecuencias Top 5).
* **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI ultrarrápido utilizado para correr la aplicación.

### Frontend (Generative Dashboard UI)
* **HTML5/CSS3:** Diseño responsivo, tema "Dark Neon Premium" con micro-interacciones.
* **Vanilla JavaScript:** Lógica de abstracción para parsear el JSON universal y construir tarjetas (cards) dinámicamente según la cantidad de columnas del archivo.
* **[Chart.js](https://www.chartjs.org/):** Gráficos interactivos de Radar, Dona, Barras Polar y Líneas generados localmente en el navegador.

---

## 📂 Visión General del Proyecto

```text
Futbol/
│
├── data/                            # Directorio local de datasets
│   ├── dataset_espanol.csv          # Dataset de prueba sugerido (Fútbol Histórico)
│   ├── dataset_limpio.csv           
│   └── results.csv                  
│
├── outputs/                         # Gráficos e imágenes exportadas del análisis
│
├── main.py                          # 🚀 Archivo principal de FastAPI (Enrutamiento y Endpoints)
├── procesamiento_universal.py       # 🧮 Motor de Data Science con Pandas
├── schemas.py                       # 🛡️ Modelos de validación estricta Pydantic
│
├── interfaz_premium.html            # 🎨 Dashboard interactivo Frontend (Punto de entrada Web)
│
├── requirements.txt                 # Dependencias exactas de Python
├── respuestas_reflexion.md          # Respuestas teóricas de la Fase 5 y Flujo de Datos
├── README.md                        # Este documento explicativo
└── .gitignore                       # Ignora la carpeta venv y caché de Python en Git
```

---

## 🚀 Guía de Instalación y Ejecución Local

Para clonar y correr este entorno analítico en tu propia máquina, sigue estos pasos:

### 1. Clonar el Repositorio
Abre tu terminal y descarga el código fuente:
```bash
git clone https://github.com/vanessacortes20/Actividad_Aplicada_python.git
cd Actividad_Aplicada_python
```

### 2. Crear un Entorno Virtual (Opcional pero recomendado)
Crea y activa un entorno aislado para no afectar tu ecosistema global de Python:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias Requeridas
Instala el framework de la API y las librerías matemáticas ejecutando:
```bash
pip install -r requirements.txt
```

### 4. Encender el Servidor API
Levanta el servicio web localmente en el puerto 8000:
```bash
python -m uvicorn main:app --reload
```
*Si la consola emite el mensaje `Application startup complete.`, el motor estará funcionando exitosamente.*

---

## 💻 Uso del Dashboard (Interfaz Gráfica Principal)
Mientras que Swagger UI es útil para pruebas técnicas, **el archivo `interfaz_premium.html` es el verdadero corazón interactivo del proyecto**. Fue diseñado explícitamente como una interfaz "Premium" para que cualquier usuario interactúe con el motor analítico de manera visual y estética, sin necesidad de saber programar.

1. Con tu servidor Uvicorn encendido localmente, ve a tus carpetas y **haz doble clic** directamente en el archivo `interfaz_premium.html` para abrirlo en Chrome, Safari o tu navegador favorito.
2. Utiliza la zona interactiva central de arrastrar y soltar (Drag & Drop) para subir tu archivo `data/dataset_espanol.csv`.
3. Navega de forma dinámica por las 4 modernas tarjetas horizontales ("Visión General", "Limpieza", "Explorador Visual" y la "Memoria API").

## 🧪 Pruebas Técnicas de API (Swagger UI)
Este proyecto cumple con estándares OpenAPI. Si deseas aislar el Frontend del análisis técnico estricto, puedes testear todos los **Endpoints CRUD** programáticamente visitando la consola autogenerada nativa:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
