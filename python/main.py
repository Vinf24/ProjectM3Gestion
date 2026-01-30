""" ARCHIVO PRINCIPAL """

from datos import estudiantes
from funciones import agregar_estudiante, actualizar_estudiante, mostrar_estudiante
from funciones import eliminar_estudiante, valorar_estudiante, cerrar_temporada_curso
from funciones import buscar_por_ciudad, json_estudiantes, resumen_estadisticas
from funciones import guardar_resumen_anual, pedir_notas, reiniciar_curso

while True:
    try:
        # Menú de opciones
        cerrar_temporada_curso(estudiantes)
        print("\n---Opciones---")
        print("Estudiantes: 1. Agregar 2. Actualizar 3. Eliminar")
        print("Estudiantes: 4. Mostrar 5. Valorar 6. Buscar por ciudad")
        print("7. Agregar notas 8. Resumen estadistico 9. Reiniciar curso")
        print("10. Salir")
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
                pedir_notas(estudiantes)
            case 8:
                resumen_estadisticas(estudiantes)
            case 9:
                reiniciar_curso(estudiantes)
            case 10:
                cerrar_temporada_curso(estudiantes)
                guardar_resumen_anual(estudiantes)
                json_estudiantes(estudiantes)
                break
            case _:
                print("Opción inválida")
    except ValueError:
        print("Opción inválida")
