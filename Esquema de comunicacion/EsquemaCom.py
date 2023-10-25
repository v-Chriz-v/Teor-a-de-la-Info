import random
import time
import math
import wave
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from collections import Counter, defaultdict
import heapq
from huffman import contar_frecuencias, construir_arbol_huffman, comprimir_huffman, descomprimir_huffman
from ShannonFano import contar_frecuencias, construir_arbol_shannon_fano, comprimir_shannon_fano, descomprimir_shannon_fano
from Britate_Variable import comprimir_vbr, descomprimir_vbr
from RLE import comprimir_RLE, descomprimir_RLE

#--------------------------------------------------------------------------------------------------------------------#

# Función para simular un canal de transmisión (perfil A2DP de Bluetooth)
def Canal(segmentos, canales):

    datos_recibidos = [[] for _ in range(len(canales))]
    entropias = [[] for _ in range(len(canales))]

    i = 0  # Índice para recorrer los segmentos

    while i < len(segmentos):

        for j, canal in enumerate(canales):

            # Probabilidad de error en la transmisión
            probabilidad_de_error = random.random()
            
            if i < len(segmentos):
                segmento = segmentos[i]
                segmento_con_ruido = simular_ruido(segmento, probabilidad_de_error)

                if segmento_con_ruido is not None:
                    canal.append(segmento_con_ruido)
                    i += 1

                    entropia = calcular_Entropia(probabilidad_de_error)
                    entropias[j].append(entropia)

    return datos_recibidos, entropias

#--------------------------------------------------------------------------------------------------------------------#

# Función para asignar datos a canales usando modulación
def modulacion(segmentos, canales):

    i = 0 

    while i < len(segmentos):

        for canal in canales:

            if i < len(segmentos):
                canal.append(segmentos[i])
                i += 1

#--------------------------------------------------------------------------------------------------------------------#

# Función para simular ruido: variación de velocidad
def simular_ruido(segmento, probabilidad_de_error):

    # Evitar cambios de velocidad en segmentos muy cortos
    if len(segmento) < 150:

        return None  # No se transmite el segmento

    speed_factor = random.uniform(0.5, 1.8)

    # Aplicar cambio de velocidad antes de transmitir
    segmento_con_ruido = segmento.speedup(speed_factor)
    
    if random.random() < probabilidad_de_error:
        return None  # No se transmite el segmento debido a un error

    else:
        return segmento_con_ruido  # Se transmite el segmento con ruido

#--------------------------------------------------------------------------------------------------------------------#

def calcular_Entropia(probabilidad_de_error):

    probabilidad_de_exito = 1 - probabilidad_de_error

    entropia = -(probabilidad_de_error * math.log2(probabilidad_de_error) + probabilidad_de_exito * math.log2(probabilidad_de_exito))

    return entropia

#--------------------------------------------------------------------------------------------------------------------#

print("Cargando la canción original...\n")
cancion_original = AudioSegment.from_file("rolita.mp3", format="mp3")
time.sleep(3)

print("Codificando datos...\n")
time.sleep(3)

datos_binarios = cancion_original.raw_data

with open("Cancion_codificada.dat", "wb") as archivo:
    archivo.write(datos_binarios)

# Dividir los datos binarios en segmentos
segmentos = [cancion_original[i:i + 2000] for i in range(0, len(cancion_original), 2000)]

# Crear 5 canales de transmisión
canales = [[] for _ in range(5)]

# Asignar segmentos a los canales
modulacion(segmentos, canales)

print("Transmitiendo...\n")
time.sleep(3)
datos_recibidos, entropias = Canal(segmentos, canales)

#--------------------------------------------------------------------------------------------------------------------#

"""
print("Encriptando...\n")
time.sleep(3)
datos_encriptados = [comprimir_huffman(dato.raw_data) for dato in datos_recibidos]

print("Desencriptando...\n")
time.sleep(3)
datos_desencriptados = [descomprimir_huffman(dato.raw_data, tabla_huffman) for dato, tabla_huffman in zip(datos_recibidos, datos_encriptados)]
"""

#--------------------------------------------------------------------------------------------------------------------#

"""
print("Comprimiendo...\n")
time.sleep(3)
datos_encriptados, arbol = comprimir_shannon_fano(datos_binarios)

print("Descomprimiendo...\n")
time.sleep(3)
datos_desencriptados = descomprimir_shannon_fano(datos_encriptados, arbol)
datos_desencriptados = bytes(datos_desencriptados)

"""

#--------------------------------------------------------------------------------------------------------------------#

#"""
print("Comprimiendo...\n")
time.sleep(3)
datos_encriptados = comprimir_vbr(datos_binarios)

print("Descomprimiendo...\n")
time.sleep(3)
datos_desencriptados = descomprimir_vbr(datos_encriptados)
datos_desencriptados = bytes(datos_desencriptados)

#"""

#--------------------------------------------------------------------------------------------------------------------#

"""
print("Comprimiendo...\n")
time.sleep(3)
datos_encriptados = comprimir_RLE(datos_binarios)

print("Descomprimiendo...\n")
time.sleep(3)
datos_desencriptados = descomprimir_RLE(datos_encriptados)
datos_desencriptados = bytes(datos_desencriptados)

"""

#--------------------------------------------------------------------------------------------------------------------#

entropia_total = 0

for sublist in entropias:
    
    for p in sublist:

        if p > 0:

            entropia_total -= p * math.log2(p)

# Crear una lista de números de segmentos para el eje x
num_segmentos = list(range(len(entropias)))

print(f'La entropia del esquema es de: {entropia_total:.2f} bits\n')

print('"Reproduciendo" canción...')

# Tamaño de segmento
tamaño_segmento = len(segmentos[0].raw_data)

# Inicializar una canción vacía
canción_modificada = AudioSegment.silent(duration=0)

# Pista para realizar un seguimiento de la posición actual en la canción modificada
posición_actual = 0

for dato_desencriptado in datos_desencriptados:

    # Verificar si dato_desencriptado es del tipo bytes antes de continuar
    if isinstance(dato_desencriptado, bytes) and len(dato_desencriptado) == tamaño_segmento:

        # Agregar cada dato desencriptado directamente a la canción modificada
        canción_modificada = canción_modificada.overlay(AudioSegment(data=dato_desencriptado, frame_rate=canción_original.frame_rate, sample_width=canción_original.sample_width, channels=canción_original.channels), position=posición_actual)
        posición_actual += tamaño_segmento

# Guardar la canción modificada con ruido en un archivo
canción_modificada.export("cancion_modificada.wav", format="wav")

plt.plot(num_segmentos, [p for sublist in entropias for p in sublist], marker='o', linestyle='-')
plt.xlabel('Número de Segmento')
plt.ylabel('Entropía')
plt.title('Curva de Entropía')
plt.grid(True)

plt.xticks(num_segmentos)  
plt.yticks([round(i, 2) for i in list(np.arange(0, 1.1, 0.1))])

plt.show()

#--------------------------------------------------------------------------------------------------------------------#