import numpy as np
from collections import deque

# Constantes que representan los tipos de celda
CELDA_VACIA = 0        # Espacio libre donde el robot puede moverse
CELDA_OBSTACULO = 1    # Celda bloqueada, el robot no puede pasar por aquí
CELDA_ROBOT = 2        # Posición inicial del robot
CELDA_PAQUETE = 3      # Paquete que el robot debe recoger
CELDA_ENTREGA = 4      # Zona de entrega final para dejar el paquete

# Definir el plano del almacén como una matriz de NumPy
plano_almacen = np.array([
    [0, 0, 0, 1, 0],
    [0, 2, 0, 1, 3],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [3, 0, 0, 0, 4]
])


def buscar_celdas_con_valor(valor_buscado, matriz):
    """
    Busca todas las coordenadas en una matriz donde se encuentra un valor específico.

    Parámetros:
    - valor_buscado (int): El valor que se desea localizar.
    - matriz (np.ndarray): La matriz en la que se busca.

    Retorna:
    - List[Tuple[int, int]]: Lista de coordenadas (fila, columna) donde se encontró el valor.
    """
    coordenadas_numpy = list(zip(*np.where(matriz == valor_buscado)))
    coordenadas_formateadas = [(int(fila), int(columna)) for fila, columna in coordenadas_numpy]
    return coordenadas_formateadas


def encontrar_camino_mas_corto(inicio, destino, matriz):
    """
    Encuentra el camino más corto desde una posición inicial a un destino, evitando obstáculos,
    utilizando búsqueda en anchura (BFS).

    Parámetros:
    - inicio (tuple): Coordenada (fila, columna) de inicio.
    - destino (tuple): Coordenada (fila, columna) del objetivo.
    - matriz (np.ndarray): El plano del almacén.

    Retorna:
    - List[Tuple[int, int]]: El camino desde inicio hasta destino como lista de coordenadas.
      Retorna None si no se encuentra un camino válido.
    """
    filas, columnas = matriz.shape
    celdas_visitadas = np.full((filas, columnas), False)
    cola_busqueda = deque()
    cola_busqueda.append((inicio, [inicio]))

    # Direcciones posibles: arriba, abajo, izquierda, derecha
    direcciones_movimiento = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while cola_busqueda:
        posicion_actual, camino_actual = cola_busqueda.popleft()
        fila_actual, columna_actual = posicion_actual

        # Si se llega al destino, se retorna el camino recorrido
        if posicion_actual == destino:
            return camino_actual
        
        # Explorar vecinos (celdas adyacentes válidas)
        for desplazamiento_fila, desplazamiento_columna in direcciones_movimiento:
            nueva_fila = fila_actual + desplazamiento_fila
            nueva_columna = columna_actual + desplazamiento_columna

            # Validar que la nueva posición esté dentro de los límites y no sea obstáculo
            if (
                0 <= nueva_fila < filas and
                0 <= nueva_columna < columnas and
                not celdas_visitadas[nueva_fila, nueva_columna] and
                matriz[nueva_fila, nueva_columna] != CELDA_OBSTACULO
            ):
                # Marcar la celda como visitada y guardar el nuevo camino
                celdas_visitadas[nueva_fila, nueva_columna] = True
                nuevo_camino = camino_actual + [(nueva_fila, nueva_columna)]
                cola_busqueda.append(((nueva_fila, nueva_columna), nuevo_camino))

    return None # No se encontró camino posible


def simular_movimiento_robot(camino):
    """
    Imprime paso a paso cómo se movería el robot por un camino determinado.

    Parámetro:
    - camino (List[Tuple[int, int]]): Secuencia de coordenadas a seguir por el robot.
    """
    contador = 1
    for coordenada in camino:
        if contador == 1:
            contador += 1
            print(f"📍 El robot parte en la celda {coordenada}")
            continue
        print(f"➡️  Robot se mueve a la celda {coordenada}")


def iniciar_recoleccion_y_entrega(plano, posicion_inicial_robot, posicion_zona_entrega):
    """
    Ejecuta el ciclo completo de recolección y entrega de todos los paquetes del almacén.

    Parámetros:
    - plano (np.ndarray): La matriz del almacén.
    - posicion_inicial_robot (tuple): Coordenada inicial del robot.
    - posicion_zona_entrega (tuple): Coordenada de la zona de entrega.
    """
    coordenadas_paquetes = buscar_celdas_con_valor(CELDA_PAQUETE, plano)
    cantidad_paquetes = len(coordenadas_paquetes)
    paquetes_entregados = 0

    for coordenada_paquete in coordenadas_paquetes:
        # Buscar camino hacia el paquete
        camino_hacia_paquete = encontrar_camino_mas_corto(posicion_inicial_robot, coordenada_paquete, plano)
        if not camino_hacia_paquete:
            print("❌ No se pudo llegar al paquete en", coordenada_paquete)
            continue

        simular_movimiento_robot(camino_hacia_paquete)
        print("✅ Paquete recogido en", coordenada_paquete)
        paquetes_entregados += 1
        plano[coordenada_paquete] = CELDA_VACIA
        posicion_inicial_robot = coordenada_paquete  # el robot se mueve al paquete

        # Buscar camino hacia la zona de entrega
        camino_hacia_entrega = encontrar_camino_mas_corto(posicion_inicial_robot, posicion_zona_entrega, plano)
        if not camino_hacia_entrega:
            print("❌ No se pudo llegar a la zona de entrega desde", posicion_inicial_robot)
            continue

        simular_movimiento_robot(camino_hacia_entrega)
        print("📦 Paquete entregado en la zona de entrega", posicion_zona_entrega)
        posicion_inicial_robot = posicion_zona_entrega

    # Resultado final
    if paquetes_entregados:
        print(f"🎉 Se han entregado {paquetes_entregados} paquete(s) de {cantidad_paquetes}.")
    else:
        print("😭 No se pudieron entregar los paquetes.")


def main():
    """
    Función principal: busca las posiciones iniciales del robot y la zona de entrega,
    y ejecuta el proceso de recolección y entrega de paquetes.
    """
    coordenada_robot = buscar_celdas_con_valor(CELDA_ROBOT, plano_almacen)[0]
    coordenada_entrega = buscar_celdas_con_valor(CELDA_ENTREGA, plano_almacen)[0]

    iniciar_recoleccion_y_entrega(plano_almacen, coordenada_robot, coordenada_entrega)


# Punto de entrada del programa
if __name__ == "__main__":
    main()