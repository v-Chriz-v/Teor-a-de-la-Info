import collections

#--------------------------------------------------------------------------------------------------------------------#

# Función para comprimir datos usando Run-Length Encoding (RLE)
def comprimir_RLE(datos):
    datos_comprimidos = []
    contador = 1

    for i in range(1, len(datos)):
        if datos[i] == datos[i - 1]:
            contador += 1
        else:
            datos_comprimidos.append(datos[i - 1])
            datos_comprimidos.append(contador)
            contador = 1

    # Añade el último símbolo y su frecuencia
    datos_comprimidos.append(datos[-1])
    datos_comprimidos.append(contador)

    # Crear y guardar un archivo de texto con símbolo y frecuencia
    with open("tabla_rle.txt", "w") as tabla_file:
        tabla_file.write("Símbolo\tFrecuencia\n")

        for i in range(0, len(datos_comprimidos), 2):
            tabla_file.write(f"{datos_comprimidos[i]}\t{datos_comprimidos[i+1]}\n")

    return datos_comprimidos

#--------------------------------------------------------------------------------------------------------------------#

# Función para descomprimir datos usando Run-Length Encoding (RLE)
def descomprimir_RLE(datos_comprimidos):
    datos_descomprimidos = []

    for i in range(0, len(datos_comprimidos), 2):
        simbolo = datos_comprimidos[i]
        frecuencia = datos_comprimidos[i + 1]
        datos_descomprimidos.extend([simbolo] * frecuencia)

    return datos_descomprimidos

#--------------------------------------------------------------------------------------------------------------------#