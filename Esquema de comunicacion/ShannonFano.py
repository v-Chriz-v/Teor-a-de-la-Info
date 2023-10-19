import collections

#--------------------------------------------------------------------------------------------------------------------#

def contar_frecuencias(datos):
    # Contar las frecuencias de cada byte en los datos
    frecuencias = collections.Counter(datos)
    
    # Ordenar el diccionario de frecuencias de mayor a menor
    frecuencias_ordenadas = dict(sorted(frecuencias.items(), key=lambda x: x[1], reverse=True))
        
    return frecuencias_ordenadas

#--------------------------------------------------------------------------------------------------------------------#

def construir_arbol_shannon_fano(frecuencias):

    if len(frecuencias) == 0:
        return []

    # Ordenar símbolos por frecuencia descendente
    simbolos_ordenados = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)

    # Caso base: si solo hay un símbolo, devolver el árbol con ese símbolo
    if len(simbolos_ordenados) == 1:
        return [(simbolos_ordenados[0][0], '')]

    # Dividir símbolos en dos grupos aproximadamente iguales
    mitad = len(simbolos_ordenados) // 2
    grupo1 = simbolos_ordenados[:mitad]
    grupo2 = simbolos_ordenados[mitad:]

    # Construir el árbol de forma recursiva
    arbol_grupo1 = construir_arbol_shannon_fano(dict(grupo1))
    arbol_grupo2 = construir_arbol_shannon_fano(dict(grupo2))

    # Asignar '0' a los símbolos en el grupo 1 y '1' al grupo 2
    arbol = [(simbolo, codigo + '0') for simbolo, codigo in arbol_grupo1] + [(simbolo, codigo + '1') for simbolo, codigo in arbol_grupo2]

    return arbol

#--------------------------------------------------------------------------------------------------------------------#

def comprimir_shannon_fano(datos):

    frecuencias = contar_frecuencias(datos)
    arbol = construir_arbol_shannon_fano(frecuencias)

    # Construir un diccionario para buscar rápidamente los códigos
    diccionario_codigo = {simbolo: codigo for simbolo, codigo in arbol}

    # Calcular las probabilidades de los símbolos
    total_simbolos = sum(frecuencias.values())
    probabilidades = {simbolo: frecuencia / total_simbolos for simbolo, frecuencia in frecuencias.items()}

    datos_encriptados = []
    codigo_actual = ''

    for byte in datos:
        codigo_actual += diccionario_codigo[byte]

        while len(codigo_actual) >= 8:

            # Dividir y agregar bytes completos al resultado
            byte_cortado = codigo_actual[:8]
            datos_encriptados.append(int(byte_cortado, 2))
            codigo_actual = codigo_actual[8:]

    if codigo_actual:

        # Agregar el último byte (si es que hay alguno)
        datos_encriptados.append(int(codigo_actual, 2))

    # Generar y guardar la tabla de símbolos y probabilidades en un archivo de texto
    with open("tabla_shannon_fano.txt", "w") as tabla_file:
        tabla_file.write("Símbolo\tProbabilidad\n")

        for simbolo, probabilidad in probabilidades.items():
            tabla_file.write(f"{simbolo}\t{probabilidad:.6f}\n")

    return bytes(datos_encriptados), arbol

#--------------------------------------------------------------------------------------------------------------------#

def descomprimir_shannon_fano(datos, arbol):

    diccionario_simbolo = {codigo: simbolo for simbolo, codigo in arbol}

    datos_binarios = ''.join(format(byte, '08b') for byte in datos)
    datos_desencriptados = []

    codigo_actual = ''
    
    for bit in datos_binarios:
        codigo_actual += bit

        if codigo_actual in diccionario_simbolo:

            simbolo = diccionario_simbolo[codigo_actual]
            datos_desencriptados.append(simbolo)
            codigo_actual = ''

    return datos_desencriptados
    
#--------------------------------------------------------------------------------------------------------------------#