from pydub import AudioSegment
import random

# Cargar la canción
song = AudioSegment.from_file("cancion.mp3", format="mp3")

# Convertir la canción a binario
binary_data = song.raw_data

# Función de cifrado básica (XOR con una clave)
def encrypt(data, key):
    encrypted_data = bytearray()
    for byte in data:
        encrypted_data.append(byte ^ key)
    return encrypted_data

# Encriptar los datos binarios
encryption_key = random.randint(0, 255)
encrypted_data = encrypt(binary_data, encryption_key)

# Simular ruido: variación de velocidad
def simulate_noise(segment):
    min_segment_duration = 1000  # Establece la duración mínima en milisegundos
    if len(segment) < min_segment_duration:
        return segment
    speed_factor = random.uniform(0.3, 1.9)
    return segment.speedup(speed_factor)

# Simular el canal y ruido
segment_size = 10000
encrypted_segments = [AudioSegment(data=encrypted_data[i:i+segment_size], frame_rate=song.frame_rate, sample_width=song.sample_width, channels=song.channels) for i in range(0, len(encrypted_data), segment_size)]
noisy_segments = [simulate_noise(segment) for segment in encrypted_segments]

# Función de descifrado básica
def decrypt(data, key):
    return encrypt(data, key)

# Reconstruir la señal de audio
reconstructed_data = bytes([byte ^ encryption_key for segment in noisy_segments for byte in segment.raw_data])
reconstructed_song = AudioSegment(data=reconstructed_data, frame_rate=song.frame_rate, sample_width=song.sample_width, channels=song.channels)

# Guardar la canción reconstruida en un archivo
reconstructed_song.export("cancion_reconstruida.mp3", format="mp3")
