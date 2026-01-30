""" FUNCIONES PRINCIPALES """

import json
from helpers import promedio_notas, estado_aprobacion, calcular_metricas
from helpers import detectar_atipicos, datos_finales, crear_id, generar_resumen_anual
from helpers import obtener_ciudades, busqueda_binaria_ids, determinar_periodo

def pedir_nombre():
    """ Agrega nombre al estudiante """
    while True:
        try:
            nombre = input("Nombre del estudiante: ")
            if nombre.strip() == "":
                raise ValueError
            if not nombre.isalpha():
                raise ValueError
            return nombre
        except ValueError:
            print("Nombre inválido")

def pedir_edad():
    """ Agrega edad al estudiante """
    while True:
        try:
            edad = int(input("Edad del estudiante: "))
            if 18 < edad < 65:
                return edad
            else:
                print("\nDebe ser mayor de 18 y menor de 65 años\n")
        except ValueError:
            print("Edad inválida")

def pedir_ciudad():
    """ Agrega ciudad al estudiante """
    while True:
        try:
            ciudad = input("Ciudad del estudiante: ")
            if ciudad.strip() == "":
                raise ValueError
            if not ciudad.isalpha():
                raise ValueError
            return ciudad
        except ValueError:
            print("Ciudad inválida")

def pedir_notas(estudiantes):
    """ Agrega notas al estudiante """
    periodo = determinar_periodo()
    if periodo == "cierre":
        print("\n Año cerrado: no se pueden agregar notas\n")
        return
    try:
        idx = int(input("Ingrese el ID del estudiante: "))
    except ValueError:
        print("ID inválido")
        return

    if idx not in estudiantes:
        print("Estudiante no encontrado")
        return

    estudiante = estudiantes[idx]
    notas = estudiante["notas"]

    for p in range(1, periodo):
        clave = f"p{p}"
        if notas[clave] is None:
            notas[clave] = 1

    clave_periodo = f"p{periodo}"

    while True:
        try:
            nota = float(input(f"Nota del periodo {periodo}: "))
            if 1 <= nota <= 7:
                notas[clave_periodo] = nota
                print("Nota registrada")
                imprimir_estudiantes(estudiantes)
                break
            raise ValueError
        except ValueError:
            print("Nota inválida")

def agregar_estudiante(estudiantes):
    """ Agrega estudiante a la lista """
    idx = crear_id(estudiantes)
    estudiante = {
        "nombre": pedir_nombre(),
        "edad": pedir_edad(),
        "ciudad": pedir_ciudad(),
        "notas": {"p1": None,
                  "p2": None,
                  "p3": None
        },
        "notas_finales": None
    }
    estudiantes[idx] = estudiante
    imprimir_estudiantes(estudiantes)

def actualizar_estudiante(estudiantes):
    """ Actualiza datos del estudiante """
    try:
        idx = int(input("Ingrese el ID del estudiante a actualizar: "))
    except ValueError:
        print("ID inválido")
        return
    if idx not in estudiantes:
        print("Estudiante no encontrado")
        return
    estudiante = estudiantes[idx]

    while True:
        try:
            print("Elegir dato a actualizar...")
            print("1. Nombre")
            print("2. Edad")
            print("3. Ciudad")
            print("4. Salir")
            opcion = int(input("Seleccione una opción: "))
            match opcion:
                case 1:
                    estudiante["nombre"] = pedir_nombre()
                    print("\nNombre actualizado\n")
                case 2:
                    estudiante["edad"] = pedir_edad()
                    print("\nEdad actualizada\n")
                case 3:
                    estudiante["ciudad"] = pedir_ciudad()
                    print("\nCiudad actualizada\n")
                case 4:
                    imprimir_estudiantes(estudiantes)
                    return
                case _:
                    print("Opción inválida")
        except ValueError:
            print("\nDebe ingresar un número válido\n")

def eliminar_estudiante(estudiantes):
    """ Elimina estudiante de la lista """
    while True:
        try:
            idx = int(input("Ingrese el ID del estudiante a eliminar: "))
            if idx <= 0:
                raise ValueError
            break
        except ValueError:
            print("ID inválido")
    if idx in estudiantes.keys():
        del estudiantes[idx]
        print("Estudiante eliminado")
        imprimir_estudiantes(estudiantes)
    else:
        print("Estudiante no encontrado")

def imprimir_estudiantes(estudiantes):
    """ Muestra lista de estudiantes """
    with open("lista_estudiantes.txt", 'w', encoding="UTF-8") as file:
        if not estudiantes:
            file.write("No hay estudiantes registrados")
        else:
            file.write("Lista de estudiantes:\n")
            for idx, estudiante in estudiantes.items():
                file.write(f"\nID: {idx}\n")
                file.write(f"Nombre: {estudiante['nombre']}\n")
                file.write(f"Edad: {estudiante['edad']}\n")
                file.write(f"Ciudad: {estudiante['ciudad']}\n")
                file.write(f"Notas: {estudiante['notas']}\n")

def valorar_estudiante(estudiantes):
    """ Muestra valoración del estudiante """

    try:
        idx = int(input("Ingrese el ID del estudiante a valorar: "))
    except ValueError:
        print("ID inválido")
        return

    if idx not in estudiantes:
        print("Estudiante no encontrado")
        return

    estudiante = estudiantes[idx]
    promedio = promedio_notas(estudiante["notas"])

    if promedio == 0:
        print("El estudiante no tiene notas registradas")
        return

    estado = estado_aprobacion(promedio)

    print(
        f"{estudiante['nombre']} de {estudiante['ciudad']} "
        f"ha {estado} con {promedio:.2f}"
    )

def listar_ciudades(estudiantes):
    """ Muestra lista de ciudades """
    ciudades = obtener_ciudades(estudiantes)
    if not ciudades:
        print("No hay ciudades registradas")
        return []
    print("\nCiudades disponibles:")
    for i, ciudad in enumerate(ciudades, start=1):
        print(f"{i}. {ciudad}")
    return ciudades

def buscar_por_ciudad(estudiantes):
    """ Busca estudiante por ciudad """
    ciudades = listar_ciudades(estudiantes)
    if not ciudades:
        return
    while True:
        try:
            idx = int(input("Seleccione el número de la ciudad: "))
            if not 1 <= idx <= len(ciudades):
                raise ValueError
            break
        except ValueError:
            print("Ciudad inválida")

    ciudad_seleccionada = ciudades[idx - 1]

    resultados = [
        (idx, e["nombre"], e["edad"])
        for idx, e in estudiantes.items()
        if e["ciudad"] == ciudad_seleccionada
    ]
    cantidad = len(resultados)

    if not resultados:
        print("No se encontraron estudiantes en esa ciudad")
        return
    print(f"\nEstudiantes en {ciudad_seleccionada}:")
    for idx, nombre, edad in resultados:
        print(f"- ID: {idx} | {nombre} ({edad} años)")

    print(f"\nTotal encontrados: {cantidad} estudiante(s)")

def json_estudiantes(estudiantes):
    """ Guarda los datos de los estudiantes en un archivo JSON """
    with open("estudiantes.json", "w", encoding="utf-8") as f:
        json.dump(estudiantes, f, ensure_ascii=False, indent=4)
    print("\nDatos guardados en estudiantes.json")

def cargar_estudiantes():
    """ Carga los datos de los estudiantes desde un archivo JSON """
    try:
        with open("estudiantes.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
            return {int(k): v for k, v in datos.items()}
    except FileNotFoundError:
        return {}

def mostrar_estudiante(estudiantes):
    """ Muestra información de un estudiante específico """
    ids = tuple(sorted(estudiantes.keys()))

    try:
        idx = int(input("Ingrese el ID del estudiante a mostrar: "))
    except ValueError:
        print("ID inválido")
        return
    resultado = busqueda_binaria_ids(ids, idx, 0, len(ids) - 1)
    if resultado is None:
        print("Estudiante no encontrado")
        return

    estudiante = estudiantes[resultado]
    print(f"\nID: {resultado}")
    print(f"Nombre: {estudiante['nombre']}")
    print(f"Edad: {estudiante['edad']}")
    print(f"Ciudad: {estudiante['ciudad']}")
    print(f"Notas: {estudiante['notas']}\n")

def resumen_estadisticas(estudiantes):
    """ Muestra resumen estadístico de los estudiantes """
    datos = datos_finales(estudiantes)

    if not datos:
        print("No hay datos para generar estadísticas")
        return

    metricas = calcular_metricas(datos)

    porcentaje_aprobados = (metricas['aprobados'] / metricas['total']) * 100
    porcentaje_reprobados = (metricas['reprobados'] / metricas['total']) * 100

    print("\n---Resumen Estadístico---")
    print(f"Total de estudiantes: {metricas['total']}")
    print(f"Estudiantes aprobados: {metricas['aprobados']} ({porcentaje_aprobados:.2f}%)")
    print(f"Estudiantes reprobados: {metricas['reprobados']} ({porcentaje_reprobados:.2f}%)")
    print(f"Promedio general de notas: {metricas['promedio_general']:.2f}\n")

    atipicos = detectar_atipicos(
        datos,
        metricas['promedio_general'],
        metricas['desviacion']
    )

    if not atipicos:
        print("No hay estudiantes con notas atipicas")
        return

    print("Estudiantes con notas atipicas:")
    print("\n⚠️ Requiere atención! ⚠️\n")
    for idx, nombre, promedio in atipicos:
        print(f"- ID: {idx} | {nombre} ({promedio:.2f})")

def cerrar_temporada_curso(estudiantes):
    """ Cierra año académico """
    periodo = determinar_periodo()
    if periodo != "cierre":
        return

    for estudiante in estudiantes.values():
        if estudiante["notas_finales"] is not None:
            continue
        notas = estudiante["notas"]

        for p in ("p1", "p2", "p3"):
            if notas[p] is None:
                notas[p] = 1

        estudiante["notas_finales"] = (
            notas["p1"],
            notas["p2"],
            notas["p3"]
        )

    print("\nAño cerrado\n")
    guardar_resumen_anual(estudiantes)

def guardar_resumen_anual(estudiantes):
    """ Transcribir los datos a forma más legible """
    resumen = generar_resumen_anual(estudiantes)

    if resumen is None:
        return

    with open("resumen_anual.txt", "w", encoding="utf-8") as f:
        f.write("Resumen Anual\n")

        f.write(f"Total estudiantes: {resumen['total_estudiantes']}\n")
        f.write(
            f"Aprobados: {resumen['aprobados']} "
            f"({resumen['porcentaje_aprobados']:.2f}%)\n"
        )
        f.write(
            f"Reprobados: {resumen['reprobados']} "
            f"({resumen['porcentaje_reprobados']:.2f}%)\n"
        )
        f.write(f"Promedio general: {resumen['promedio_general']:.2f}\n\n")

        if resumen["atipicos"]:
            f.write("⚠️ Estudiantes con notas atípicas: ⚠️\n")
            for e in resumen["atipicos"]:
                f.write(
                    f"- ID {e['id']} | {e['nombre']} "
                    f"({e['promedio_final']:.2f})\n"
                )

    print("\nResumen anual guardado en resumen_anual.txt\n")

def reiniciar_curso(estudiantes):
    """ Reinicia el curso """
    periodo = determinar_periodo()
    if periodo != 1:
        return

    for estudiante in estudiantes.values():
        estudiante["notas"] = {"p1": None, "p2": None, "p3": None}
        estudiante["notas_finales"] = None
    print("\nCurso reiniciado\n")
    guardar_resumen_anual(estudiantes)
    json_estudiantes(estudiantes)
    