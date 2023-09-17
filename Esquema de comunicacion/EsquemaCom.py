import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment

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

        if probabilidad_de_error < 0.4 and probabilidad_de_error > 0.6:

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

    # Calculamos la entropia
    entropia = -(probabilidad_de_error * math.log2(probabilidad_de_error) + probabilidad_de_exito * math.log2(probabilidad_de_exito))

    return entropia

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
print(f'La entropia del esquema es de: {entropia_total:.2f} bits\n')

print('"Reproduciendo" canción...')

# Reconstruir la canción modificada con ruido

# Inicializar una canción vacía
canción_modificada = AudioSegment.empty()  
for dato_desencriptado in datos_desencriptados:
    canción_modificada += AudioSegment(data=dato_desencriptado, frame_rate=cancion_original.frame_rate, sample_width=cancion_original.sample_width, channels=cancion_original.channels)

# Guardar la canción modificada con ruido en un archivo
canción_modificada.export("cancion_modificada.mp3", format="mp3")

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