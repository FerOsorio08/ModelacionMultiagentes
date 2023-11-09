#Fernanda Osorio A01026502
# Generador de rueda en formato OBJ
#8 de noviembre del 2023

import math

def generar_modelo(num_sides, radius, width):
    if num_sides < 3 or num_sides > 360 or (num_sides == None):
        print("El número de lados del círculo debe estar entre 3 y 360.")
        num_sides = 8

    if radius <= 0 or width <= 0 or (radius == None) or (width == None):
        print("El radio y el ancho de la rueda deben ser valores positivos.")
        radius = 1.0
        width = 0.5
    

    # Inicializamos listas para almacenar vértices, normales y caras
    vertices = []
    normals = []
    faces = []

     # Calcular vértices y normales
    for i in range(num_sides):
        ##angulo 
        angle = 2 * math.pi * i / num_sides
        ##coordenadas
        y = radius * math.cos(angle)
        z = radius * math.sin(angle)
        ##vertices
        ##de acuerdo a unity, el centro del objeto es el origen
        vertices.append((-width / 2, y, z))
        vertices.append((width / 2, y, z))
    
    #Agregar los vertices de las tapas
    vertices += [(-width / 2,0,0), (width / 2,0,0)]


    # Calcular caras en sentido antihorario
    for i in range(num_sides):
        ## a: primer vertice de la cara
        ## se multiplica por 2 para que se recorra el arreglo de vertices
        a = 2 * i
        ## b: segundo vertice de la cara
        # modulo para que no se salga del arreglo
        b = (2 * i + 1) % (2 * num_sides)
        ## c: tercer vertice de la cara
        c = (2 * i + 2) % (2 * num_sides)
        ## d: cuarto vertice de la cara
        d = (2 * i + 3) % (2 * num_sides)

        #normals
        V1,V2,V3 = vertices[a], vertices[b], vertices[d]
        # V1 = [vertices[b][i] - vertices[a][i] for i in range(3)]
        # V2 = [vertices[c][i] - vertices[a][i] for i in range(3)]
        normal = calculate_normal(V1, V2, V3)
        normals.append(normal)

        face1 = (b+1, c+1, d+1)
        face2 = (a+1, c+1, b+1)
        ##Faces para las tapas
        face3 = (a+1, c+1, len(vertices)-1)
        face4 = (d+1, b+1, len(vertices)-2)
        face5 = (a+1, b+1, d+1)
        face6 = (a+1, d+1, c+1)
        # face7 = (len(vertices)-1, c+1, a+1)
        # face8 = (len(vertices)-2, b+1, d+1)
        # face5 = (len(vertices) - 4, len(vertices) - 3, len(vertices) - 1)
        # face6 = (len(vertices) - 2, len(vertices) - 3, len(vertices) - 1)
        # faces.extend([face5, face6])

       
        faces.extend([face1, face2, face3, face4])
    face5 = (len(vertices) - 2, len(vertices) - 1, len(vertices) - 3)
    face6 = (len(vertices) - 3, len(vertices) - 1, len(vertices) - 4)
    faces.extend([face5, face6])
    right_normal = calculate_normal(vertices[len(vertices)-2], vertices[0], vertices[2])
    left_normal = calculate_normal(vertices[len(vertices)-1], vertices[1], vertices[3])
    normals.append(right_normal)
    normals.append(left_normal)
    
    # Escribir el modelo en un archivo OBJ
    with open("rueda.obj", "w") as obj_file:
        obj_file.write("# Modelo de rueda generado\n")
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for normal in normals:
            obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
        for i, face in enumerate(faces):
            if i < len(faces) - num_sides * 2:
                face_normal = i // 2 + 1

            elif i < len(faces) - num_sides:
                face_normal = num_sides * 2 + 1

                face_normal = num_sides * 2 + 2

            obj_file.write(f"f {face[0]}//{face_normal} {face[1]}//{face_normal} {face[2]}//{face_normal}\n")

    print("Modelo de rueda generado en 'rueda.obj'.")


def calculate_normal(vector1, vector2, vector3):

    # #Calcular el vector normal
    Ux = vector2[0] - vector1[0]
    Uy = vector2[1] - vector1[1]
    Uz = vector2[2] - vector1[2]

    Vx = vector3[0] - vector1[0]
    Vy = vector3[1] - vector1[1]
    Vz = vector3[2] - vector1[2]
    #normal vector
    normal = (Uy * Vz - Uz * Vy, Uz * Vx - Ux * Vz, Ux * Vy - Uy * Vx)
    #magnitude
    # magnitude = math.sqrt(sum(component ** 2 for component in normal))
    magnitude = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)

    return (normal[2]/magnitude, normal[1]/magnitude, normal[0]/magnitude)

if __name__ == "__main__":
    lados = int(input("Número de lados del círculo: "))
    radio = float(input("Radio del círculo: "))
    ancho = float(input("Ancho de la rueda: "))

    generar_modelo(lados, radio, ancho)