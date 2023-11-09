#Fernanda Osorio A01026502
# Generador de rueda en formato OBJ
#8 de noviembre del 2023

import math

normals = []
def generar_modelo(num_sides, radius, width):
    if num_sides < 3 or num_sides > 360:
        print("El número de lados del círculo debe estar entre 3 y 360.")
        num_sides = 8

    if radius <= 0 or width <= 0:
        print("El radio y el ancho de la rueda deben ser valores positivos.")
        radius = 1.0
        width = 0.5
    

    # Inicializamos listas para almacenar vértices, normales y caras
    vertices = []
    # normals = []
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
        a1 = (i - 1)% (2 * num_sides)
        a1 = a1 if a1 != 0 else 2 * num_sides
        ## b: segundo vertice de la cara
        # modulo para que no se salga del arreglo
        b = (2 * i + 1) % (2 * num_sides)
        ## c: tercer vertice de la cara
        c = (2 * i + 2) % (2 * num_sides)
        ## d: cuarto vertice de la cara
        d = (2 * i + 3) % (2 * num_sides)

        #normals
        V1 = [vertices[b][i] - vertices[a][i] for i in range(3)]
        V2 = [vertices[c][i] - vertices[a][i] for i in range(3)]
        normal = calculate_normal(cross_product(V1, V2))
        normals.append(normal)
        ##Faces para los lados
        face1 = (b+1, c+1, d+1)
        face2 = (a+1, c+1, b+1)
        ##Faces para las tapas superiores
        face3 = (len(vertices)-1, c+1, a+1)
        face4 = (len(vertices)-2, b+1, d+1)
        ##Faces con la misma normal
        face5 = (len(vertices)-2, b+1, d+1)
        face6 = (len(vertices)-1, c+1, a+1)
        ##Faces para tapa inferior
        face7 = (a + 1, c + 1, len(vertices) - 1)
        face8 = (d + 1, b + 1, len(vertices) - 2)
        
        faces.extend([face1, face2, face3, face4, face5, face6, face7, face8])
        
    right_normal = calculate_normal(cross_product([0, 0, 1], [1, 0, 0]))
    left_normal = calculate_normal(cross_product([0, 0, 1], [-1, 0, 0]))
    normals.extend([right_normal, left_normal])
    left_cap_normal = calculate_normal((-1, 0, 0))
    right_cap_normal = calculate_normal((1, 0, 0))
    normals.extend([left_cap_normal, right_cap_normal])

    num_faces = len(faces)

    # Escribir el modelo en un archivo OBJ
    with open("rueda.obj", "w") as obj_file:
        obj_file.write("# Modelo de rueda generado\n")
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for normal in normals:
            obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
        #normals to faces
        for i, face in enumerate(faces):
            v1, v2, v3 = face
            # Calcular el vector de la cara usando los vertices de la cara
            pcVector1 = [vertices[v2 - 1][i] - vertices[v1 - 1][i] for i in range(3)]
            pcVector2 = [vertices[v3 - 1][i] - vertices[v1 - 1][i] for i in range(3)]
            vn = Normal_vector(pcVector1, pcVector2)

            obj_file.write(f"f {face[0]}//{vn} {face[1]}//{vn} {face[2]}//{vn}\n")

    print("Modelo de rueda generado en 'rueda.obj'.")

def cross_product(V1, V2):
    V3 = [0, 0, 0]
    V3[0] = V1[1] * V2[2] - V1[2] * V2[1]
    V3[1] = V1[2] * V2[0] - V1[0] * V2[2]
    V3[2] = V1[0] * V2[1] - V1[1] * V2[0]
    return V3

#función para calcular las normales de las caras
def Normal_vector(v1,v2):
    count=0
    normal=calculate_normal(cross_product(v1,v2))
    #si la normal no está en la lista de normales, se agrega y se regresa el índice de la normal
    if normal not in normals:
        normals.append(normal)
        return count
    # si la normal ya está en la lista de normales, se regresa el índice de la normal
    else:
        return normals.index(normal) + 1 

def calculate_normal(vector):
    #Calcular la magnitud del vector
    magnitude = math.sqrt(sum(component ** 2 for component in vector))

    # Asegurar que la magnitud no sea cero
    if magnitude == 0:
        return (0, 0, 0)  # Return a zero vector

    # Calcular el vector normalizado
    normal = tuple(component / magnitude for component in vector)

    return normal

if __name__ == "__main__":
    lados = (input("Número de lados del círculo: "))
    radio = (input("Radio del círculo: "))
    ancho = (input("Ancho de la rueda: "))

    radio = float(radio) if radio else 1.0
    ancho = float(ancho) if ancho else 0.5
    lados = int(lados) if lados else 8

    generar_modelo(lados, radio, ancho)
