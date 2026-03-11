from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class ResumenNumerico(BaseModel):
    promedio: float
    mediana: float
    desviacion_estandar: float
    maximo: float
    minimo: float
    suma: float
    valores_nulos: int
    valores_unicos: int


class ResumenCategorico(BaseModel):
    valores_nulos: int
    valores_unicos: int
    top_frecuencias: Dict[str, int]


class PartidoInput(BaseModel):
    torneo: str
    ciudad: str
    pais: str
    equipo_local: str
    equipo_visitante: str
    goles_local: int
    goles_visitante: int
    neutral: bool


class EstadisticasPartido(BaseModel):
    total_goles: int
    resultado: str
    empate: bool
    ganador: str


class AnalisisUniversalSalida(BaseModel):
    id: Optional[int]
    total_filas: int
    total_columnas: int
    nombres_columnas: List[str]
    # Diccionario de { "nombre_columna": { promedio, maximo, minimo, suma, etc... } }
    resumen_numerico: Dict[str, ResumenNumerico]
    # Diccionario de { "nombre_columna": ResumenCategorico }
    resumen_categorico: Dict[str, ResumenCategorico]