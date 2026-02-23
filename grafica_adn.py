import matplotlib
matplotlib.use('TkAgg') #Fuerza el usode ventanas interactivas
import matplotlib.pyplot as plt
from Bio.Seq import Seq

# 1. Tu secuencia de ADN
secuencia = Seq("ATGCATGCATGCGCCGCTAGCTAGCTAGCGGGATTTTAACCGG")

# 2. Contamos cada base
conteos = {
    'Adenina': secuencia.count("A"),
    'Timina': secuencia.count("T"),
    'Citosina': secuencia.count("C"),
    'Guanina': secuencia.count("G")
}

# 3. Calculamos el porcentaje de GC
gc_content = (conteos['Citosina'] + conteos['Guanina']) / len(secuencia) * 100

# 4. Creamos la gráfica
plt.bar(conteos.keys(), conteos.values(), color=['blue', 'red', 'green', 'orange'])
plt.title(f"Composición de la Secuencia\nContenido GC: {gc_content:.2f}%")
plt.ylabel("Cantidad de bases")

print(f"Análisis completado. Porcentaje GC: {gc_content:.2f}%")
print("Cerrando la ventana de la gráfica para terminar...")

plt.show()