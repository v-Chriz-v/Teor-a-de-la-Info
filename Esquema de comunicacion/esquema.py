from pydub import AudioSegment
import random

def encriptar(data):
    return bytes((byte + 1) & 0xFF for byte in data)

def desencriptar(data):
    return bytes((byte - 1) & 0xFF for byte in data)

# Carga la canción original
cancion_original = AudioSegment.from_file("cancion.mp3", format="mp3")

# Convierte la canción a binario y encripta
datos_binarios = cancion_original.raw_data
datos_encriptados = encriptar(datos_binarios)

# Función para simular ruido: variación de velocidad
def ruido(segmento):
    probabilidad_de_cambio = 0.4  # Probabilidad de cambio por segmento
    if len(segmento) < 150:  # Evitar cambios de velocidad en segmentos muy cortos
        return segmento
    if random.random() < probabilidad_de_cambio:
        speed_factor = random.uniform(0.6, 1.6)  # Rango de velocidad
        return segmento.speedup(speed_factor)
    return segmento

# Duración máxima de un segmento en milisegundos
duracion_maxima_segmento = 5000

segmentos_modificados = []

# Divide los datos encriptados en segmentos y aplica ruido (cambios de velocidad) aleatoriamente
inicio = 0
while inicio < len(datos_encriptados):
    duracion_segmento = random.randint(2500, duracion_maxima_segmento)
    fin = min(inicio + duracion_segmento, len(datos_encriptados))

    # Ajusta la longitud de los datos encriptados si es necesario
    if (fin - inicio) % (cancion_original.sample_width * cancion_original.channels) != 0:
        fin += (cancion_original.sample_width * cancion_original.channels) - ((fin - inicio) % (cancion_original.sample_width * cancion_original.channels))

    # Extrae el segmento actual
    segmento = AudioSegment(data=datos_encriptados[inicio:fin], frame_rate=cancion_original.frame_rate, sample_width=cancion_original.sample_width, channels=cancion_original.channels)

    # Aplica la función de ruido al segmento actual
    segmento_modificado = ruido(segmento)

    # Agrega el segmento modificado al resultado
    segmentos_modificados.append(segmento_modificado)

    # Actualiza el punto de inicio para el próximo segmento
    inicio = fin

# Combina todos los segmentos modificados en una sola canción
cancion_modificada = sum(segmentos_modificados)

# Desencriptar los datos
datos_con_ruido = b''.join(segmento.raw_data for segmento in segmentos_modificados)
datos_desencriptados = desencriptar(datos_con_ruido)

# Reconstruir la canción modificada con ruido
cancion_modificada_con_ruido = AudioSegment(data=datos_desencriptados, frame_rate=cancion_original.frame_rate, sample_width=cancion_original.sample_width, channels=cancion_original.channels)

# Guardar la canción modificada con ruido en un archivo
cancion_modificada_con_ruido.export("cancion_reconstruida.mp3", format="mp3")
