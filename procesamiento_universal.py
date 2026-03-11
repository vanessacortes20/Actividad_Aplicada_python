import pandas as pd
import numpy as np

def analizar_csv_universal(contenido_csv: str) -> dict:
    """
    Función pura universal que recibe el texto de cualquier CSV, 
    lo perfila con Pandas de forma dinámica y devuelve estadísticas agnósticas.
    """
    import io
    
    # 1. Cargar el dataframe
    try:
        df = pd.read_csv(io.StringIO(contenido_csv))
    except Exception as e:
        raise ValueError(f"No se pudo analizar el CSV: {str(e)}")

    if df.empty:
        raise ValueError("El DataFrame está vacío.")

    # 1.5 Auto-Traducir al Español y embellecer columnas conocidas y desconocidas
    diccionario_traduccion = {
        "home_score": "Goles Local", "away_score": "Goles Visitante",
        "home_team": "Equipo Local", "away_team": "Equipo Visitante",
        "tournament": "Torneo", "city": "Ciudad", "country": "País Anfitrión",
        "neutral": "Cancha Neutral", "date": "Fecha de Juego",
        "equipo_local": "Equipo Local", "equipo_visitante": "Equipo Visitante",
    }
    
    nuevas_columnas = {}
    for col in df.columns:
        col_limpia = str(col).lower().strip()
        if col_limpia in diccionario_traduccion:
            nuevas_columnas[col] = diccionario_traduccion[col_limpia]
        else:
            # Para otras variables, limpiamos guiones bajos y ponemos mayúscula inicial
            nuevas_columnas[col] = str(col).replace("_", " ").title()
            
    df = df.rename(columns=nuevas_columnas)

    # Convertir valores NaN o nulos a None para que pydantic/FastAPI pueda enviarlos en JSON
    df = df.replace({np.nan: None})
    
    total_filas = int(len(df))
    total_columnas = int(len(df.columns))

    resumen_numerico = {}
    resumen_categorico = {}

    # 2. Separar e inferir tipos
    # Consideramos "numéricas" aquellas int o float
    cols_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
    # Consideramos "categóricas" o de texto aquellas de tipo object (strings) o bool
    cols_categoricas = df.select_dtypes(include=['object', 'bool', 'category']).columns.tolist()

    # 3. Extraer estadísticas numéricas
    for col in cols_numericas:
        serie = df[col].dropna()
        total_nulos = int(df[col].isnull().sum())
        total_unicos = int(df[col].nunique())
        
        if not serie.empty:
            resumen_numerico[col] = {
                "promedio": round(float(serie.mean()), 4),
                "mediana": round(float(serie.median()), 4),
                "desviacion_estandar": round(float(serie.std()) if len(serie) > 1 else 0.0, 4),
                "maximo": float(serie.max()),
                "minimo": float(serie.min()),
                "suma": float(serie.sum()),
                "valores_nulos": total_nulos,
                "valores_unicos": total_unicos
            }
        else:
            resumen_numerico[col] = {
                "promedio": 0.0, "mediana": 0.0, "desviacion_estandar": 0.0,
                "maximo": 0.0, "minimo": 0.0, "suma": 0.0,
                "valores_nulos": total_nulos, "valores_unicos": total_unicos
            }

    # 4. Extraer estadísticas categóricas (Frecuencias - Top 5)
    for col in cols_categoricas:
        serie = df[col].dropna()
        total_nulos = int(df[col].isnull().sum())
        total_unicos = int(df[col].nunique())
        
        if not serie.empty:
            # Obtener el Top 5 más repetido usando value_counts
            top_5 = serie.value_counts().head(5)
            # Convertimos el top_5 a dict: { "Nombre": frecuencia_int }
            resumen_categorico[col] = {
                "valores_nulos": total_nulos,
                "valores_unicos": total_unicos,
                "top_frecuencias": {str(k): int(v) for k, v in top_5.items()}
            }
        else:
            resumen_categorico[col] = {
                "valores_nulos": total_nulos,
                "valores_unicos": total_unicos,
                "top_frecuencias": {}
            }

    # 5. Extracting Raw Data is disabled for Phase 5 testing to avoid Swagger UI freezing.

    resultado = {
        "total_filas": total_filas,
        "total_columnas": total_columnas,
        "nombres_columnas": df.columns.tolist(),
        "resumen_numerico": resumen_numerico,
        "resumen_categorico": resumen_categorico
    }
    
    return resultado
