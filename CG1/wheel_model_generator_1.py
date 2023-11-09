import argparse
import numpy as np

def generate_wheel_model(num_sides, radius, width):
    if num_sides < 3 or num_sides > 360:
        print("El número de lados del círculo debe estar entre 3 y 360.")
        num_sides = 8

    if radius <= 0 or width <= 0:
        print("El radio y el ancho de la rueda deben ser valores positivos.")
        radius = 1.0
        width = 0.5
    

    # Inicializamos listas para almacenar vértices, normales y caras
    vertices = []
    normals = []
    faces = []
    facesN = []
    V1 = []
    V2 = []
    V4 = []
    

     # Calcular vértices y normales
    for i in range(num_sides):
        ##angulo 
        angle = 2 * np.pi * i / num_sides
        ##coordenadas
        # x es el radio por el coseno del angulo porque es el eje x
        # y es el radio por el seno del angulo porque es el eje y
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        ##vertices
        ## z es el ancho entre 2 porque es el eje z
        vertices.append((x, y, -width / 2))
        vertices.append((x, y, width / 2))
        ##vertices para caras 
        #(0,0,-width/2)
        #(0,0,width/2)
        ##normales
        ## z es -1 porque es el eje z para que se vea hacia abajo
        ## para ver para afuera es 1 ??
        # normals.append((0, 0, -1))
    vertices += [(0, 0, -width / 2), (0, 0, width / 2)]
    
    

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
        b1 = (2 * i - 1) % (2 * num_sides)
        b1 = b1 if b1 != 0 else 2 * num_sides
        ## c: tercer vertice de la cara
        c = (2 * i + 2) % (2 * num_sides)
        c1 = (2 * i -2)% (2 * num_sides)
        c1 = c1 if c1 != 0 else 2 * num_sides
        ## d: cuarto vertice de la cara
        d = (2 * i + 3) % (2 * num_sides)
        d1 = (2 * i - 3) % (2 * num_sides)
        d1 = d1 if d1 != 0 else 2 * num_sides
        ## cara 1: a, b, c
        ## cara 2: a, c, d
        ## necestio el +1 porque los indices empiezan en 1
        face1 = f"f {b+1}//{b1+1} {c+1}//{c1+1} {d+1}//{d1+1}\n"
        face2 = f"f {a+1}//{a1+1} {c+1}//{c1+1} {b+1}//{b1+1}\n"
        ##Faces para las tapas
        #tapa : a, c, (0,0,-width/2)
        #tapa : b, d, (0,0,width/2)
        face3 = f"f {c+1}//{c1+1} {a+1}//{1+1} {len(vertices)-1}\n"
        face4 = f"f {b+1}//{b1+1} {d+1}//{d1+1} {len(vertices)-2}\n"

        # face3 = f"f {a+1}//{width/2} {b+1}//{width/2} {width/2}\n"
        # face4 = f"f {a+1}//{-width/2} {b+1}//{-width/2} {-width/2}\n"
        faces.append(face1)
        faces.append(face2)
        faces.append(face3)
        faces.append(face4)
        facesN.append([a+1,b+1,c+1,d+1])

        #normals
        normal1 = calculate_normal(cross_product(V1, V2))
        normal2 = calculate_normal(cross_product(V2, V1))
        normal3 = calculate_normal(cross_product(V2, V1))
        normal4 = calculate_normal(cross_product(V1, V2))
        normals.extend([normal1, normal2, normal3, normal4])

    ##faltan las tapas
    ##Las caras estan al reves
    for face in facesN:
        V1[0] = vertices[face[0] - 1][0] - vertices[face[1]][0]
        V1[1] = vertices[face[0] - 1][1] - vertices[face[1]][1]
        V1[2] = vertices[face[0] - 1][2] - vertices[face[1]][2]
        
        V2[0] = vertices[face[0] - 1][0] - vertices[face[2]][0]
        V2[1] = vertices[face[0] - 1][1] - vertices[face[2]][1]
        V2[2] = vertices[face[0] - 1][2] - vertices[face[2]][2]
        #cross product
        V4 = cross_product(V1,V2)
        #normal
        #cross product magnitude
        Vmagnitud = np.sqrt(V4[0]**2 + V4[1]**2 + V4[2]**2)
        normal = (V4[0]/Vmagnitud, V4[1]/Vmagnitud, V4[2]/Vmagnitud)
        normals.append(normal)

    print(V4)

    # Escribir el modelo en un archivo OBJ
    with open("wheel_model.obj", "w") as obj_file:
        obj_file.write("# Modelo de rueda generado\n")
        for vertex in vertices:
            obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        # for normal in normals:
        #     obj_file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")
        obj_file.write("usemtl Material\n")
        obj_file.write("s off\n")
        for face in faces:
            obj_file.write(face)

    print("Modelo de rueda generado en 'wheel_model.obj'.")

def cross_product(V1,V2):
    V3 = []
    V3[0] = V1[1] * V2[2] - V1[2] * V2[1]
    V3[1] = V1[2] * V2[0] - V1[0] * V2[2]
    V3[2] = V1[0] * V2[1] - V1[1] * V2[0]
    return V3


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera un modelo de rueda en formato OBJ.")
    parser.add_argument("--lados", type=int, default=8, help="Número de lados del círculo (entre 3 y 360)")
    parser.add_argument("--radio", type=float, default=1.0, help="Radio del círculo (positivo)")
    parser.add_argument("--ancho", type=float, default=0.5, help="Ancho de la rueda (positivo)")
    args = parser.parse_args()

    generate_wheel_model(args.lados, args.radio, args.ancho)
