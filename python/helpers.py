""" FUNCIONES SECUNDARIAS (HELPERS) """

import statistics
from datetime import datetime

def promedio_notas(notas):
    """ Calcula el promedio de las notas """
    if not notas:
        return 0
    return sum(notas) / len(notas)

def estado_aprobacion(promedio):
    """ Determina si el estudiante está aprobado o reprobado """
    return "aprobado" if promedio >= 7 else "reprobado"

def calcular_metricas(datos):
    """ Calcula métricas de los datos """
    total = len(datos)
    promedios = [p for _, _, p in datos]
    aprobados = sum(1 for p in promedios if p >= 7)
    reprobados = total - aprobados

    promedio_general = sum(promedios) / total
    desviacion = statistics.stdev(promedios) if total > 1 else 0

    return {
        "total": total,
        "aprobados": aprobados,
        "reprobados": reprobados,
        "promedio_general": promedio_general,
        "desviacion": desviacion
    }

def detectar_atipicos(datos, promdio_general, desviacion):
    """ Detecta estudiantes con notas atipicas """
    if desviacion == 0:
        return []

    umbral = 2*desviacion
    return [
        (idx, nombre, promedio)
        for idx, nombre, promedio in datos
        if abs(promedio - promdio_general) > umbral
    ]

def datos_finales(estudiantes):
    """ Muestra datos finales de los estudiantes """
    datos = []

    for idx, estudiante in estudiantes.items():
        finales = estudiante.get("notas_finales")
        if finales is not None:
            promedio = promedio_notas(finales)
            datos.append((idx, estudiante['nombre'], promedio))

    return datos

def crear_id(estudiantes):
    """ Crea ID único para cada estudiante """
    if not estudiantes:
        return 1
    return max(estudiantes.keys()) + 1

def obtener_ciudades(estudiantes):
    """ Obtiene lista de ciudades únicas """
    return sorted({e["ciudad"] for e in estudiantes.values()})

def busqueda_binaria_ids(ids, objetivo, inicio, fin):
    """ Realiza una búsqueda binaria de IDs para usar recursividad """
    if inicio > fin:
        return None

    medio = (inicio + fin) // 2

    if ids[medio] == objetivo:
        return ids[medio]
    if objetivo < ids[medio]:
        return busqueda_binaria_ids(ids, objetivo, inicio, medio - 1)
    return busqueda_binaria_ids(ids, objetivo, medio + 1, fin)

def determinar_periodo():
    """ Determina periodo según minuto """
    minuto = datetime.now().minute 
    ciclo = minuto % 10
    if ciclo <= 2:
        return 1
    if ciclo <= 5:
        return 2
    if ciclo <= 8:
        return 3
    return "cierre"

def generar_resumen_anual(estudiantes):
    """Genera los datos consolidados del resumen anual"""

    datos = datos_finales(estudiantes)
    if not datos:
        return None

    metricas = calcular_metricas(datos)
    atipicos = detectar_atipicos(
        datos,
        metricas["promedio_general"],
        metricas["desviacion"]
    )

    return {
        "total_estudiantes": metricas["total"],
        "aprobados": metricas["aprobados"],
        "reprobados": metricas["reprobados"],
        "porcentaje_aprobados": metricas["aprobados"] / metricas["total"] * 100,
        "porcentaje_reprobados": metricas["reprobados"] / metricas["total"] * 100,
        "promedio_general": metricas["promedio_general"],
        "desviacion": metricas["desviacion"],
        "estudiantes": [
            {
                "id": idx,
                "nombre": nombre,
                "promedio_final": promedio
            }
            for idx, nombre, promedio in datos
        ],
        "atipicos": [
            {
                "id": idx,
                "nombre": nombre,
                "promedio_final": promedio
            }
            for idx, nombre, promedio in atipicos
        ]
    }
