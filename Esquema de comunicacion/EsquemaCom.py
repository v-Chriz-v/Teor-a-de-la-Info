import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from collections import Counter, defaultdict
import heapq

#--------------------------------------------------------------------------------------------------------------------#

# Función de encriptación
def encriptar(data):
    return bytes((byte + 1) & 0xFF for byte in data)

#--------------------------------------------------------------------------------------------------------------------#

# Función de desencriptación
def desencriptar(data):
    return bytes((byte - 1) & 0xFF for byte in data)

#--------------------------------------------------------------------------------------------------------------------#

# Función para simular un canal de transmisión (perfil A2DP de Bluetooth)
def Canal(segmentos):

    datos_recibidos = []
    entropias = []

    for segmento in segmentos:

        # Probabilidad de error en la transmisión
        probabilidad_de_error = random.random() 

        entropia = calcular_Entropia(probabilidad_de_error)
        entropias.append(entropia)

        if probabilidad_de_error <= 0.4 and probabilidad_de_error >= 0.6:

            # Segmento silencioso en caso de error
            datos_recibidos.append(AudioSegment.silent(len(segmento)))  

        else:

            # Aplicar cambio de velocidad antes de transmitir
            segmento_con_ruido = simular_ruido(segmento, probabilidad_de_error)
            datos_recibidos.append(segmento_con_ruido)

    return datos_recibidos, entropias

#--------------------------------------------------------------------------------------------------------------------#

# Función para simular ruido: variación de velocidad
def simular_ruido(segmento, probabilidad_de_error):

    # Evitar cambios de velocidad en segmentos muy cortos
    if len(segmento) < 150: 
        return segmento

    if probabilidad_de_error >= 0.4 and probabilidad_de_error <= 0.6:

        speed_factor = random.uniform(0.5, 1.8)
        return segmento.speedup(speed_factor)

    return segmento

#--------------------------------------------------------------------------------------------------------------------#

def calcular_Entropia(probabilidad_de_error):

    probabilidad_de_exito = 1 - probabilidad_de_error

    # Calculamos la entropía
    entropia = -(probabilidad_de_error * math.log2(probabilidad_de_error) + probabilidad_de_exito * math.log2(probabilidad_de_exito))

    return entropia

#--------------------------------------------------------------------------------------------------------------------#

# Función para contar las frecuencias de bits en los datos binarios
def contar_frecuencias(datos_binarios):
    return Counter(datos_binarios)

#--------------------------------------------------------------------------------------------------------------------#

# Función para construir un árbol de Huffman
def construir_arbol_huffman(frecuencias):

    pila = [[peso, [bit, ""]] for bit, peso in frecuencias.items()]
    heapq.heapify(pila)
    
    while len(pila) > 1:

        baja = heapq.heappop(pila)
        sube = heapq.heappop(pila)

        for par in baja[1:]:
            par[1] = '0' + par[1]

        for par in sube[1:]:
            par[1] = '1' + par[1]

        heapq.heappush(pila, [baja[0] + sube[0]] + baja[1:] + sube[1:])
    
    return sorted(heapq.heappop(pila)[1:], key=lambda p: (len(p[-1]), p))

#--------------------------------------------------------------------------------------------------------------------#

# Función para comprimir datos usando Huffman
def comprimir_huffman(datos_binarios):

    frecuencias = contar_frecuencias(datos_binarios)

    arbol_huffman = construir_arbol_huffman(frecuencias)

    tabla_huffman = {bit: codigo for bit, codigo in arbol_huffman}

    datos_codificados = "".join(tabla_huffman[bit] for bit in datos_binarios)

    return datos_codificados.encode("utf-8"), tabla_huffman

#--------------------------------------------------------------------------------------------------------------------#

# Función para decodificar datos usando Huffman
def descomprimir_huffman(datos_codificados, tabla_huffman):

    datos_binarios = []
    bits_actuales = ""
    
    for bit in datos_codificados.decode("utf-8"):

        bits_actuales += bit

        for original_bit, codigo in tabla_huffman.items():

            if codigo == bits_actuales:

                datos_binarios.append(original_bit)
                bits_actuales = ""
                break

    return bytes(datos_binarios)

#--------------------------------------------------------------------------------------------------------------------#

# Cargar la canción original
print("Cargando la canción original...\n")
cancion_original = AudioSegment.from_file("rolita.mp3", format="mp3")
time.sleep(3)

print("Codificando datos...\n")
time.sleep(3)

# Convertir la canción a binario y encriptar
datos_binarios = cancion_original.raw_data

# Guardar los datos binarios en un archivo
with open("Cancion_codificada.dat", "wb") as archivo:
    archivo.write(datos_binarios)

# Dividir los datos binarios en segmentos
segmentos = [cancion_original[i:i + 2000] for i in range(0, len(cancion_original), 2000)]

# Transmitir los datos a través del canal y recibir datos simulados
print("Transmitiendo...\n")
time.sleep(3)
datos_recibidos, entropias = Canal(segmentos)  # Simulación de la transmisión

# Desencriptar los datos simulados
print("Desencriptando...\n")
time.sleep(3)
datos_desencriptados = [desencriptar(dato.raw_data) for dato in datos_recibidos]

entropia_total = -sum(p * math.log2(p) for p in entropias if p > 0)
print(f'La entropía del esquema es de: {entropia_total:.2f} bits\n')

print('"Reproduciendo" canción...')

# Reconstruir la canción modificada con ruido
canción_modificada = AudioSegment.empty()
tablas_huffman_segmentos = []  # Lista para almacenar las tablas de Huffman de cada segmento

for i, dato_desencriptado in enumerate(datos_desencriptados):
    canción_modificada += AudioSegment(data=dato_desencriptado, frame_rate=cancion_original.frame_rate, sample_width=cancion_original.sample_width, channels=cancion_original.channels)
    
    # 1. Convertir el segmento a datos binarios
    datos_binarios_segmento = dato_desencriptado

    # 2. Calcular las frecuencias de los símbolos en el segmento
    frecuencias_segmento = contar_frecuencias(datos_binarios_segmento)

    # 3. Construir un árbol de Huffman para el segmento
    arbol_huffman_segmento = construir_arbol_huffman(frecuencias_segmento)

    # 4. Generar la tabla de Huffman para el segmento
    tabla_huffman_segmento = [(simbolo, codigo, frecuencia) for simbolo, codigo in arbol_huffman_segmento for frecuencia in [frecuencias_segmento[simbolo]]]

    # Agregar la tabla de Huffman del segmento a la lista
    tablas_huffman_segmentos.append(tabla_huffman_segmento)

# Guardamos las tablas de Huffman en un archivo de texto
with open("Tablas_Huffman.txt", "w") as archivo_huffman:
    archivo_huffman.write("Tabla de Huffman de Segmentos:\n")

    for i, tabla in enumerate(tablas_huffman_segmentos):

        archivo_huffman.write(f"Segmento {i + 1}:\n")
        archivo_huffman.write("Símbolo\tCódigo Huffman\tFrecuencia\n")

        for simbolo, codigo, frecuencia in tabla:

            archivo_huffman.write(f"{simbolo}\t{codigo}\t{frecuencia}\n")
        archivo_huffman.write("\n")

# Crear una lista de números de segmentos para el eje x
num_segmentos = list(range(len(entropias)))

# Crear el gráfico de la curva de entropía
plt.plot(num_segmentos, entropias, marker='o', linestyle='-')
plt.xlabel('Número de Segmento')
plt.ylabel('Entropía')
plt.title('Curva de Entropía')
plt.grid(True)

# Establecer valores enteros en el eje x
plt.xticks(num_segmentos)  
plt.yticks([round(i, 2) for i in list(np.arange(0, 1.1, 0.1))])

# Mostrar el gráfico
plt.show()

#--------------------------------------------------------------------------------------------------------------------#
