# Realizado por Ian Holender 
# 8 noviembre 2023
#Codigo para crear un modelo de rueda en formato OBJ 
# tomando en cuenta las especificaciones del usuario,n caso de no recibir
# esopecificaciones se toman los valores predeterminados (8 lados, radio 1.0, ancho 0.5)
import sys
import math

# Solicita los datos al usuario o utiliza valores predeterminados
lados = input("Ingrese los lados del triángulo (entre 3 y 360): ")
radio = input("Ingrese el radio de la rueda: ")
ancho = input("Ingrese el ancho de la rueda: ")

# Valores predeterminados en caso de que no se proporcionen valores
ladoDefault = 8
radioDefault = 1.0
anchoDefault = 0.5

# Convierte la entrada del usuario en valores numéricos o usa los predeterminados
try:
    lados = int(lados) if lados else ladoDefault
    radio = float(radio) if radio else radioDefault
    ancho = float(ancho) if ancho else anchoDefault
except ValueError:
    print("Los valores ingresados deben ser números válidos.")
    sys.exit(1)

def create_wheel_model(lados, radio, ancho):
    if lados < 3 or lados > 360:
        print("El número de lados debe estar entre 3 y 360.")
        return

    # Inicializa la lista de vértices y caras
    vertices = []
    faces = []
    
    for i in range(lados):
        angle = 2 * math.pi * i / lados
        x = radio * math.cos(angle)
        y = radio * math.sin(angle)
        z1 = -ancho / 2
        z2 = ancho / 2

        # Crea los vértices para la parte exterior de la llanta
        vertices.append((x, y, z1))
        vertices.append((x, y, z2))
        
    vertices.append((0, 0, z1))
    vertices.append((0, 0, z2))    

    # Calcula los vectores de normalización para cada vértice
    normals = []
    for vertex in vertices:
        # Normalización simple, ya que es una rueda
        normal = (vertex[0], vertex[1], 0)
        normals.append(normal)

    for i in range(lados):
        # Crea las caras conectando los vértices para formar las caras exteriores
        v1 = i * 2
        v2 = i * 2 + 1
        v3 = (i * 2 + 2) % (lados * 2)
        v4 = (i * 2 + 3) % (lados * 2)
        v5 = lados * 2 + 1
        v6 = lados * 2

        # Invierte las normales de las caras al cambiar el orden de los vértices
        faces.append([v4, v2, v1])
        faces.append([v1, v3, v4])
        faces.append([v3, v1, v5])
        faces.append([v4, v6, v2])

    # Escribe el modelo en un archivo OBJ
    with open("modelo_rueda.obj", "w") as obj_file:
        for i, (vertex, normal) in enumerate(zip(vertices, normals), start=1):
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
            obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
        for i, face in enumerate(faces, start=1):
            obj_file.write(f"f {face[0]+1}//{face[0]+1} {face[1]+1}//{face[1]+1} {face[2]+1}//{face[2]+1}\n")

    print("Modelo de rueda creado y guardado en 'modelo_rueda.obj'")

# Crea el modelo de rueda
create_wheel_model(lados, radio, ancho)