
# Simulamos datos falsos del LiDAR (en la realidad esto vendría del tópico /scan)
ranges_fake = [n * 0.01 for n in range(1, 361)]  # 360 valores simulados

def reducir_scan(ranges, n_sectores=10):
    tamaño_sector = len(ranges) // n_sectores  # 360 // 10 = 36
    sectores_reducidos = []
    
    for i in range(n_sectores):
        inicio = i * tamaño_sector
        fin = inicio + tamaño_sector
        sector = ranges[inicio:fin]        # tomamos un pedazo de 36 valores
        sectores_reducidos.append(min(sector))  # guardamos el mínimo de ese pedazo
    
    return sectores_reducidos

print(reducir_scan(ranges_fake))
