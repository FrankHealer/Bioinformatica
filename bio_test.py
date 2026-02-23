from Bio.Seq import Seq

# 1. Definimos una secuencia de ADN (fragmento de ejemplo)
dna_seq = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTACCCGCTAG")

# 2. Transcripción (ADN -> ARN)
mrna_seq = dna_seq.transcribe()

# 3. Traducción (ARN -> Proteína)
protein_seq = mrna_seq.translate()

print("--- Resultados de Bioinformática ---")
print(f"ADN: {dna_seq}")
print(f"ARN: {mrna_seq}")
print(f"Proteína: {protein_seq}")