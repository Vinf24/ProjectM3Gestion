""" ARCHIVO PRINCIPAL """

from datos import estudiantes
from funciones import agregar_estudiante, actualizar_estudiante, mostrar_estudiante
from funciones import eliminar_estudiante, valorar_estudiante
from funciones import buscar_por_ciudad, json_estudiantes, resumen_estadisticas

while True:
    try:
        # Menú de opciones
        print("\n---Gestión de Estudiantes---")
        print("1. Agregar estudiante")
        print("2. Actualizar estudiante")
        print("3. Eliminar estudiante")
        print("4. Mostrar estudiantes")
        print("5. Valorar estudiante")
        print("6. Buscar por ciudad")
        print("7. Resumen estadistico")
        print("8. Salir")
        opcion = int(input("Seleccione una opción: "))
        match opcion:
            case 1:
                agregar_estudiante(estudiantes)
            case 2:
                actualizar_estudiante(estudiantes)
            case 3:
                eliminar_estudiante(estudiantes)
            case 4:
                mostrar_estudiante(estudiantes)
            case 5:
                valorar_estudiante(estudiantes)
            case 6:
                buscar_por_ciudad(estudiantes)
            case 7:
                resumen_estadisticas(estudiantes)
            case 8:
                json_estudiantes(estudiantes)
                break
            case _:
                print("Opción inválida")
    except ValueError:
        print("Opción inválida")
