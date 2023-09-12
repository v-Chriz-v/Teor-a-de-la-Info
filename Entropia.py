import math
import numpy as np
import matplotlib.pyplot as plt

resultados = []
frecuencias = []
probabilidades = []
tiradas = 15

i = 1
while i <= tiradas:
	resultados.append(np.random.randint(1, 7))
	resultados.sort()

	i = i + 1

print(resultados)

for n in range(6):
	frecuencias.append(resultados.count(n + 1))

print(frecuencias)

for probs in frecuencias:
	probabilidad = (probs / tiradas)
	probabilidades.append(probabilidad)

print(probabilidades)

def calcular_entropia(probabilidades):
	entropia = -sum(p * math.log2(p) for p in probabilidades if p > 0)
	return entropia

entropia_total = calcular_entropia(probabilidades)

print(entropia_total)

# Crear el gráfico de barras para mostrar la distribución de probabilidad
plt.bar(range(1, 7), probabilidades)
plt.xlabel('Cara del Dado')
plt.ylabel('Probabilidad')
plt.title('Distribución de Probabilidad de Lanzamientos de Dado')
plt.grid(True)

# Mostrar el gráfico de barras
plt.savefig("Grafica.jpg", format="jpg")
plt.show()