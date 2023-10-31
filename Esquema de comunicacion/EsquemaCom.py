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

def Canal(segmentos, canales):

    datos_recibidos = [[] for _ in range(len(canales))]
    entropias = [[] for _ in range(len(canales))]

    i = 0  # Recorre los segmentos

    while i < len(segmentos):

        for j, canal in enumerate(canales):

            # Probabilidad de error en la transmisión
            probabilidad_de_error = random.random()

            if i < len(segmentos):
                segmento = segmentos[i]
                segmento_con_ruido = simular_ruido(segmento, probabilidad_de_error, j, i)

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

    print(f"Canales disponibles: {len(canales)}")

    while i < len(segmentos):

        for canal in canales:

            if i < len(segmentos):

                canal.append(segmentos[i])
                i += 1

#--------------------------------------------------------------------------------------------------------------------#

def simular_ruido(segmento, probabilidad_de_error, canal_index, paquete_index):

    canal_index += 1
    paquete_index += 1

    if random.random() < probabilidad_de_error:

        print(f" XX Paquete {paquete_index} perdido en Canal {canal_index} XX")
        reasignar_paquete = True

        while reasignar_paquete:

            canal_index = (canal_index % len(canales)) + 1
            canal = canales[canal_index - 1]

            if len(canal) < len(segmento):

                canal.append(segmento)
                print(f" -- Paquete {paquete_index} reasignado al Canal {canal_index} --\n")
                reasignar_paquete = False
                return None 
    else:
        print(f"|| Paquete {paquete_index} enviado por el Canal {canal_index} ||\n")
        return segmento

#--------------------------------------------------------------------------------------------------------------------#

def calcular_Entropia(probabilidad_de_error):

    probabilidad_de_exito = 1 - probabilidad_de_error

    entropia = -(probabilidad_de_error * math.log2(probabilidad_de_error) + probabilidad_de_exito * math.log2(probabilidad_de_exito))

    return entropia

#--------------------------------------------------------------------------------------------------------------------#

def calcular_entropia_canal(entropias):

    entropias_canal = [sum(entropia) for entropia in entropias]

    return entropias_canal

#--------------------------------------------------------------------------------------------------------------------#

def calcular_entropia_total(entropias_canal):

    entropia_total = sum(entropias_canal)

    return entropia_total

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

print("\nTransmitiendo...\n")
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
print("\nComprimiendo...\n")
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

print("Calculando entropía de cada canal...")
entropias_canal = calcular_entropia_canal(entropias)

for i, entropia in enumerate(entropias_canal):
    print(f"Canal {i + 1}: {entropia:.2f} bits")

entropia_total = calcular_entropia_total(entropias_canal)
print(f'\nLa entropía total del esquema es de: {entropia_total:.2f} bits')

print('\n"Reproduciendo" canción...')

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

plt.plot(list(range(len(entropias_canal))), entropias_canal, marker='o', linestyle='-')
plt.xlabel('Número de Canal')
plt.ylabel('Entropía')
plt.title('Entropía de Canales')
plt.grid(True)

plt.xticks(list(range(len(entropias_canal))))
plt.show()

#--------------------------------------------------------------------------------------------------------------------#