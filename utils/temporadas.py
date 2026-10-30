"""
Utilidades para calcular "temporadas" (rachas de meses consecutivos) de un producto.

Los períodos se expresan como enteros aaaamm (por ejemplo, 202512 = diciembre 2025).
Importante: NO se puede restar aaaamm directamente, porque 202512 -> 202601 da 89
aunque sean meses consecutivos. Por eso se convierte a un índice de mes continuo.
"""


def a_indice_mes(periodo):
    """aaaamm -> número de mes continuo (para medir huecos entre años)."""
    return (periodo // 100) * 12 + (periodo % 100)


def contar_temporadas(periodos):
    """Cantidad de rachas de meses consecutivos en que el producto estuvo activo."""
    if not periodos:
        return 0
    indices = sorted({a_indice_mes(p) for p in periodos})
    return 1 + sum(1 for a, b in zip(indices, indices[1:]) if b - a > 1)


def primera_aparicion_ultima_temporada(periodos):
    """Primer período (aaaamm) de la última racha de meses consecutivos."""
    if not periodos:
        return None
    ordenados = sorted(set(periodos))
    inicio = ordenados[-1]
    for i in range(len(ordenados) - 1, 0, -1):
        if a_indice_mes(ordenados[i]) - a_indice_mes(ordenados[i - 1]) > 1:
            break
        inicio = ordenados[i - 1]
    return inicio