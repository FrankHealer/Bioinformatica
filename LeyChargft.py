def verificar_chargaff(secuencia):
    # Convertir a mayúsculas para evitar errores
    secuencia = secuencia.upper()
    
    # 1. Contar bases
    a = secuencia.count('A')
    t = secuencia.count('T')
    c = secuencia.count('C')
    g = secuencia.count('G')
    total = len(secuencia)
    
    # 2. Calcular porcentajes
    p_purinas = ((a + g) / total) * 100
    p_pirimidinas = ((t + c) / total) * 100
    
    # 3. Mostrar resultados
    print(f"Resultados para: {secuencia}")
    print(f"A: {a}, T: {t}, C: {c}, G: {g}")
    print(f"Purinas (A+G): {p_purinas:.2f}%")
    print(f"Pirimidinas (T+C): {p_pirimidinas:.2f}%")
    
    # 4. Verificación lógica
    if (a + g) == (t + c):
        print("✅ La Ley de Chargaff se cumple perfectamente.")
    else:
        # En biología real puede haber pequeñas variaciones
        print("❌ La proporción no es exacta.")

# Ejemplo de uso
seq_ejemplo = "ATGCGATCGTAGCTAG"
verificar_chargaff(seq_ejemplo)