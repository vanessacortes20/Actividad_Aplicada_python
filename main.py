from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from schemas import AnalisisUniversalSalida, PartidoInput, EstadisticasPartido
from procesamiento_universal import analizar_csv_universal

app = FastAPI(
    title="API Analítica Universal de Datos (CSV)",
    description="Motor de análisis dinámico construido con Pandas capaz de procesar cualquier archivo estructurado.",
    version="2.0-Universal"
)

# Configurar CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memoria temporal
historial = {}
contador_id = 1


@app.post("/analizar/csv", response_model=AnalisisUniversalSalida)
async def procesar_dataset_universal(archivo: UploadFile = File(...)):
    global contador_id

    if not archivo.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="El archivo proporcionado no es un .csv válido.")

    try:
        # Leer el contenido del archivo subido en memoria
        contenido_bytes = await archivo.read()
        texto_csv = contenido_bytes.decode("utf-8")
        
        # Pasar todo el texto crudo a Pandas para que haga el perfilado (profiling) dinámico
        resultado_crudo = analizar_csv_universal(texto_csv)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error interno procesando el archivo CSV: {str(e)}")

    # Guardar en base de datos temporal
    resultado_final = { "id": contador_id, **resultado_crudo }
    historial[contador_id] = resultado_final
    contador_id += 1

    return resultado_final

@app.post("/analizar/partido", response_model=EstadisticasPartido)
def procesar_partido_individual(partido: PartidoInput):
    """
    Endpoint para pruebas de Fase 5. Procesamiento rápido de un solo JSON para 
    evitar que Swagger UI se congele renderizando Dataframes pesados.
    """
    global contador_id
    
    # 1. El JSON llega validado por Pydantic (PartidoInput)
    # 2. Hacemos matemática simple controlada 
    total_goles = partido.goles_local + partido.goles_visitante
    empate = partido.goles_local == partido.goles_visitante
    ganador = "Empate" if empate else (partido.equipo_local if partido.goles_local > partido.goles_visitante else partido.equipo_visitante)
    
    resultados_calculados = {
        "total_goles": total_goles,
        "resultado": f"{partido.goles_local}-{partido.goles_visitante}",
        "empate": empate,
        "ganador": ganador
    }
    
    # 3. Guardar en historial
    resultado_final_con_id = {
        "id": contador_id,
        "tipo": "Analisis Individual",
        "input": partido.model_dump(),
        "resultados": resultados_calculados
    }
    
    historial[contador_id] = resultado_final_con_id
    contador_id += 1
    
    # 4. Retornamos usando el modelo de salida
    return resultados_calculados

@app.get("/historial")
def obtener_historial():
    return list(historial.values())

@app.get("/historial/{record_id}")
def obtener_analisis(record_id: int):
    if record_id not in historial:
        raise HTTPException(status_code=404, detail="El análisis con el ID proveído no existe.")
    return historial[record_id]

@app.delete("/historial/{record_id}")
def eliminar_analisis(record_id: int):
    if record_id not in historial:
        raise HTTPException(status_code=404, detail="Análisis no encontrado")
    del historial[record_id]
    return {"mensaje": f"El registro {record_id} ha sido borrado de la memoria exitosamente."}