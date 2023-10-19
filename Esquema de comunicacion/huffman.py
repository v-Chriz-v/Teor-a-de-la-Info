import math
import heapq
from collections import Counter, defaultdict

#--------------------------------------------------------------------------------------------------------------------#

def comprimir_huffman(datos_binarios):

    # Obtén las frecuencias de los bytes
    frecuencias = contar_frecuencias(datos_binarios)
    
    # Construye el árbol Huffman
    arbol_huffman = construir_arbol_huffman(frecuencias)
    
    # Genera la tabla Huffman
    tabla_huffman = {byte: codigo for byte, codigo in arbol_huffman}

    # Crear un diccionario de frecuencias para contar la frecuencia de cada símbolo
    frecuencias_segmentos = defaultdict(int)

    # Contar las frecuencias de los símbolos en los datos binarios
    for byte in datos_binarios:
        frecuencias_segmentos[byte] += 1

    # Ordenar los símbolos por frecuencia de mayor a menor
    simbolos_ordenados = sorted(tabla_huffman.keys(), key=lambda simbolo: -frecuencias_segmentos[simbolo])

    # Calcular la frecuencia total
    frecuencia_total = sum(frecuencias_segmentos[simbolo] for simbolo in simbolos_ordenados)

    # Generar y guardar la tabla de símbolos y frecuencias en un archivo de texto
    with open("tabla_huffman.txt", "w") as tabla_file:
        tabla_file.write("Símbolo\tCódigo Huffman\tFrecuencia\n")
        
        for simbolo in simbolos_ordenados:
            codigo = tabla_huffman[simbolo]
            frecuencia = frecuencias_segmentos[simbolo]
            frecuencia_final = frecuencia / frecuencia_total

            # Formatear la frecuencia como porcentaje (seis decimales)
            frecuencia_final_str = f"{frecuencia_final:.6f}"

            tabla_file.write(f"{simbolo}\t{codigo}\t{frecuencia_final_str}\n")

    datos_codificados = bytearray()
    codigo_actual = b""

    for byte in datos_binarios:
        codigo_actual += tabla_huffman[byte].encode("utf-8")

        while len(codigo_actual) >= 8:
            # Divide y agrega bytes completos al resultado
            byte_cortado = codigo_actual[:8]
            datos_codificados.append(int(byte_cortado, 2))
            codigo_actual = codigo_actual[8:]

    if codigo_actual:
        # Agregar el último byte (si es que hay alguno)
        datos_codificados.append(int(codigo_actual, 2))

    return bytes(datos_codificados), tabla_huffman


#--------------------------------------------------------------------------------------------------------------------#

def descomprimir_huffman(datos_codificados, tabla_huffman):

    # Accede al segundo elemento de la tupla, que es la tabla Huffman
    tabla_huffman = tabla_huffman[1]

    datos_binarios = bytearray()
    codigo_actual = b""  # Asegura que código_actual sea de tipo bytes

    for byte in datos_codificados:
        codigo_actual += chr(byte).encode("utf-8")  # Convierte byte a cadena y luego a bytes

        # Revisa si el código actual coincide con algún código de la tabla Huffman
        for simbolo, codigo in tabla_huffman.items():
            
            if codigo_actual == codigo:
                datos_binarios.append(ord(simbolo))  # Agrega el símbolo como byte
                codigo_actual = b""  # Reinicia el código actual
                break

    return bytes(datos_binarios)

#--------------------------------------------------------------------------------------------------------------------#

# Función para contar las frecuencias de bits en los datos binarios
def contar_frecuencias(datos_binarios):
    return Counter(datos_binarios)

#--------------------------------------------------------------------------------------------------------------------#

# Función para construir el árbol de Huffman
def construir_arbol_huffman(frecuencias):

    heap = [[peso, [bit, ""]] for bit, peso in frecuencias.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        bajo1 = heapq.heappop(heap)
        bajo2 = heapq.heappop(heap)

        for par in bajo1[1:]:
            par[1] = '0' + par[1]

        for par in bajo2[1:]:
            par[1] = '1' + par[1]

        heapq.heappush(heap, [bajo1[0] + bajo2[0]] + bajo1[1:] + bajo2[1:])
    
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

#--------------------------------------------------------------------------------------------------------------------#
