from collections import defaultdict

#--------------------------------------------------------------------------------------------------------------------#

# Función para comprimir datos usando Britate Variable
def comprimir_vbr(datos_audio):
    
    datos_comprimidos = []
    contador = 0
    silencio = True
    repeticiones = defaultdict(int)

    for dato in datos_audio:
        if dato == 0:
            if not silencio:
                datos_comprimidos.append(contador)
                contador = 1
                silencio = True
            else:
                contador += 1
        else:
            if silencio:
                datos_comprimidos.append(-contador)
                contador = 1
                silencio = False
            else:
                contador += 1

    datos_comprimidos.append(contador if silencio else -contador)

    # Contar las frecuencias de los símbolos identificadores
    for dato in datos_comprimidos:
        repeticiones[abs(dato)] += 1

    # Ordenar símbolos y frecuencias de mayor a menor
    simbolos_frecuencias = sorted(repeticiones.items(), key=lambda x: x[1], reverse=True)

    with open("tabla_vbr.txt", "w") as tabla_file:
        tabla_file.write("Símbolo\tProbabilidad\n")

        for simbolo, frecuencia in simbolos_frecuencias:
            tabla_file.write(f"{simbolo}\t{frecuencia / len(datos_comprimidos):.6f}\n")

    return datos_comprimidos

#--------------------------------------------------------------------------------------------------------------------#

# Función para descomprimir datos usando Britate Variable
def descomprimir_vbr(datos_comprimidos):

    datos_audio = []
    silencio = True

    for dato in datos_comprimidos:
        if dato > 0:
            if silencio:
                datos_audio.extend([0] * dato)
                silencio = False
            else:
                datos_audio.extend([1] * dato)
        else:
            if not silencio:
                datos_audio.extend([0] * (-dato))
                silencio = True
            else:
                datos_audio.extend([1] * (-dato))

    return datos_audio

#--------------------------------------------------------------------------------------------------------------------#