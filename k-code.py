#####Elabore un algoritmo (posteriormente se codificará en Python) en el que halle el k-mero
#(subcadena de nucleótidos de tamaño k) de mayor frecuencia en una cadena
#ENTRADA: 1 secuencia nucleótidos y el tamaño del k-mero
#SALIDA: el k-mero de mayor frecuencia y el valor de dicha frecuencia
def hallar_kmero_frecuente(secuencia, k):
    # Diccionario para almacenar los k-meros y sus frecuencias
    frecuencias = {}
    n = len(secuencia)
    
    # Recorrido de la secuencia para extraer subcadenas de tamaño k
    for i in range(n - k + 1):
        kmero = secuencia[i:i+k]
        if kmero in frecuencias:
            frecuencias[kmero] += 1
        else:
            frecuencias[kmero] = 1
            
    # Identificar la frecuencia máxima
    if not frecuencias:
        return [], 0
        
    max_frec = max(frecuencias.values())
    
    # Filtrar todos los k-meros que tengan esa frecuencia máxima
    kmeros_maximos = [k_key for k_key, v in frecuencias.items() if v == max_frec]
    
    return kmeros_maximos, max_frec

# --- PRUEBA CON EL EJEMPLO DE CLASE ---
# Datos obtenidos de tus notas del Dr. Osorio
secuencia_ejemplo = "ACGTTGCATGTCGCATGATGATGAGAGCT"
valor_k = 3

resultados, frecuencia = hallar_kmero_frecuente(secuencia_ejemplo, valor_k)

# Salida de resultados
print(f"ENTRADA: {secuencia_ejemplo}, k={valor_k}")
for kmero in resultados:
    print(f"k-mero: {kmero}")
print(f"frecuencia: {frecuencia}")