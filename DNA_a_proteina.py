# 1. Tabla de Nucleótidos (Diccionario de Codones)
tabla_nucleotidos = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
}

# 2. Entrada: Lectura del archivo .txt
nombre_archivo = "M60748.1 Human histone H1 (H1F4) ge.txt" # [cite: 88]

try:
    with open(nombre_archivo, "r") as f:
        lineas = f.readlines()
        
    # Limpieza: Ignoramos la primera línea si empieza con '>' (formato FASTA)
    # y quitamos saltos de línea/espacios de toda la secuencia
    if lineas[0].startswith(">"):
        secuencia_completa = "".join(lineas[1:]).upper().replace("\n", "").replace(" ", "").strip()
    else:
        secuencia_completa = "".join(lineas).upper().replace("\n", "").replace(" ", "").strip()
        
    print(f"Secuencia cargada con éxito. Longitud total: {len(secuencia_completa)} nucleótidos.")

    # 3. Posiciones de traducción (Ejercicio 10)
    inicio_5 = int(input("Introduce el índice de inicio (ej. 0): ")) # [cite: 89]
    fin_3 = int(input("Introduce el índice de fin: ")) # [cite: 90]

    # Inicialización de variables
    Seq_n = secuencia_completa[inicio_5 : fin_3] # [cite: 93]
    proteina = "" # [cite: 94]

    # 4. Estructura de Iteración: Traducción de 3 en 3
    for i in range(0, len(Seq_n), 3): # [cite: 96]
        codon = Seq_n[i : i + 3] # [cite: 97]
        
        if len(codon) == 3: # [cite: 98]
            aminoacido = tabla_nucleotidos.get(codon) # [cite: 99]
            if aminoacido: # [cite: 100]
                proteina += aminoacido # [cite: 101]

    # 5. Resultados
    print("\n--- RESULTADO DE LA TRADUCCIÓN ---")
    print(f"Proteína: {proteina}") # [cite: 106]
    print(f"Longitud de la proteína: {len(proteina)} aminoácidos.") # 

except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{nombre_archivo}'. Asegúrate de que esté en la misma carpeta.")