""" FUNCIONES """

import json
import statistics

def promedio_notas(notas):
    """ Calcula el promedio de las notas """
    if not notas:
        return 0
    return sum(notas) / len(notas)

def estado_aprobacion(promedio):
    """ Determina si el estudiante está aprobado o reprobado """
    return "aprobado" if promedio >= 7 else "reprobado"

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

def pedir_notas():
    """ Agrega notas al estudiante """
    notas = []
    for i in range(3):
        while True:
            try:
                nota = float(input(f"Nota {i + 1}: "))
                if 0 <= nota <= 10:
                    notas.append(nota)
                    break
                raise ValueError
            except ValueError:
                print("Nota inválida")
    return notas

def crear_id(estudiantes):
    """ Crea ID único para cada estudiante """
    if not estudiantes:
        return 1
    return max(estudiantes.keys()) + 1

def agregar_estudiante(estudiantes):
    """ Agrega estudiante a la lista """
    idx = crear_id(estudiantes)
    estudiante = {
        "nombre": pedir_nombre(),
        "edad": pedir_edad(),
        "ciudad": pedir_ciudad(),
        "notas": []
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
            print("4. Notas")
            print("5. Salir")
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
                    estudiante["notas"] = pedir_notas()
                    print("\nNotas actualizadas\n")
                case 5:
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

    if not estudiante["notas"]:
        print("El estudiante no tiene notas registradas")
        return
    promedio = promedio_notas(estudiante["notas"])
    estado = estado_aprobacion(promedio)

    print(
        f"{estudiante['nombre']} de {estudiante['ciudad']} "
        f"ha {estado} con {promedio:.2f}"
    )

def obtener_ciudades(estudiantes):
    """ Obtiene lista de ciudades únicas """
    return sorted({e["ciudad"] for e in estudiantes.values()})

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
    if not estudiantes:
        print("No hay estudiantes registrados")
        return

    total = len(estudiantes)
    aprobados = 0
    reprobados = 0
    datos_promedios = []

    for idx, estudiante in estudiantes.items():
        if estudiante["notas"]:
            promedio = promedio_notas(estudiante["notas"])
            datos_promedios.append((idx, estudiante['nombre'], promedio))
            estado = estado_aprobacion(promedio)
            if estado == "aprobado":
                aprobados += 1
            else:
                reprobados += 1

    if not datos_promedios:
        print("No hay notas para generar estadísticas")
        return

    promedios = [p for _, _, p in datos_promedios]
    promedio_general = sum(promedios) / len(promedios)
    desviacion = statistics.stdev(promedios) if len(promedios) > 1 else 0

    porcentaje_aprobados = (aprobados / total) * 100
    porcentaje_reprobados = (reprobados / total) * 100

    print("\n---Resumen Estadístico---")
    print(f"Total de estudiantes: {total}")
    print(f"Estudiantes aprobados: {aprobados} ({porcentaje_aprobados:.2f}%)")
    print(f"Estudiantes reprobados: {reprobados} ({porcentaje_reprobados:.2f}%)")
    print(f"Promedio general de notas: {promedio_general:.2f}\n")

    if desviacion == 0:
        print("No hay suficientes datos para calcular la desviación estándar")
        return

    umbral = 2*desviacion
    atipicos = [
        (idx, nombre, promedio)
        for idx, nombre, promedio in datos_promedios
        if abs(promedio - promedio_general) > umbral
    ]

    if not atipicos:
        print("No hay estudiantes con notas atipicas")
        return

    print("Estudiantes con notas atipicas:")
    print("\n⚠️ Requiere atención! ⚠️\n")
    for idx, nombre, promedio in atipicos:
        print(f"- ID: {idx} | {nombre} ({promedio:.2f})")