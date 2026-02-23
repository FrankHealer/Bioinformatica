# 1. Entrada de datos
secuencia = input("Inserta la secuencia de nucleótidos: ").upper() #
k = int(input("Inserta el tamaño del k-mero (k): ")) #
n = len(secuencia) #

# 2. Inicialización de variables
max_frec = 0 # Para rastrear la frecuencia más alta
lista_kmeros = [] # Almacena los patrones únicos
lista_conteos = [] # Almacena cuántas veces aparece cada patrón

# 3. Estructura de Iteración (Ventana Deslizante)
# Usamos n - k + 1 para asegurar que procesamos hasta el último nucleótido
for i in range(0, n - k + 1): #
    # Extraer el fragmento de longitud k
    patron = secuencia[i : i + k] #
    encontrado = False # Bandera para saber si el k-mero ya existe en nuestra lista
    
    # Estructura de Identificación y Conteo
    for j in range(len(lista_kmeros)): #
        if patron == lista_kmeros[j]: #
            lista_conteos[j] += 1 #
            encontrado = True #
            
            # Actualizar la frecuencia máxima si este conteo es el nuevo líder
            if lista_conteos[j] > max_frec: #
                max_frec = lista_conteos[j] #
            break # Dejamos de buscar en la lista porque ya lo encontramos
            
    # Si al final del ciclo interno 'encontrado' sigue siendo falso, es un k-mero nuevo
    if not encontrado: #
        lista_kmeros.append(patron) #
        lista_conteos.append(1) #
        if max_frec < 1: #
            max_frec = 1 #

# 4. Salida de Resultados
print("\n--- RESULTADOS ---")
# Buscamos en nuestras listas todos los k-meros que alcanzaron la frecuencia máxima
for m in range(len(lista_kmeros)): #
    if lista_conteos[m] == max_frec: #
        print(f"k-mero: {lista_kmeros[m]}") #
        print(f"frecuencia: {max_frec}") #

# 5. Visualización con Resaltado (Opcional)
# Definimos los colores (Verde para el k-mero, Reset para volver al blanco)
VERDE = "\033[92m"
RESET = "\033[0m"

print("\n--- VISUALIZACIÓN DE PATRONES ---")
for m in range(len(lista_kmeros)):
    if lista_conteos[m] == max_frec:
        ganador = lista_kmeros[m]
        # Reemplazamos el k-mero por una versión coloreada en la secuencia
        secuencia_color = secuencia.replace(ganador, f"{VERDE}{ganador}{RESET}")
        
        print(f"Ubicación de '{ganador}':")
        print(secuencia_color)
        print("-" * 30)