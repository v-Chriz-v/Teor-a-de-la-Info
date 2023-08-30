from pydub import AudioSegment
import random

# Cargar la canción
cancion = AudioSegment.from_file("cancion.mp3", format="mp3")

# Convertir la canción a binario
datos_binarios = cancion.raw_data

# Función de cifrado básica (XOR con una clave)
def encriptar(data, key):
    datos_encriptados = bytearray()
    for byte in data:
        datos_encriptados.append(byte ^ key)
    return datos_encriptados

# Encriptar los datos binarios
llave_encriptacion = random.randint(0, 255)
datos_encriptados = encriptar(datos_binarios, llave_encriptacion)

# Simular ruido: variación de velocidad
def simular_ruido(segment):
    duracion_segmento = 1000  # Establece la duración mínima en milisegundos
    if len(segment) < duracion_segmento:
        return segment
    speed_factor = random.uniform(0.3, 1.9)
    return segment.speedup(speed_factor)

# Simular el canal y ruido
tamaño_segmento = 10000
segmentos_encriptados = [AudioSegment(data=datos_encriptados[i:i+tamaño_segmento], frame_rate=cancion.frame_rate, sample_width=cancion.sample_width, channels=cancion.channels) for i in range(0, len(datos_encriptados), tamaño_segmento)]
noisy_segments = [simular_ruido(segment) for segment in segmentos_encriptados]

# Función de descifrado básica
def desencriptar(data, key):
    return encriptar(data, key)

# Reconstruir la señal de audio
datos_reconstruidos = bytes([byte ^ llave_encriptacion for segment in noisy_segments for byte in segment.raw_data])
cancion_reconstruida = AudioSegment(data=datos_reconstruidos, frame_rate=cancion.frame_rate, sample_width=cancion.sample_width, channels=cancion.channels)

# Guardar la canción reconstruida en un archivo
cancion_reconstruida.export("cancion_reconstruida.mp3", format="mp3")
