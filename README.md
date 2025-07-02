# 🤖 Robot Recolector de Paquetes

Este proyecto implementa la lógica de un robot que navega en un almacén, recolecta paquetes y los transporta a una zona de entrega, evitando obstáculos en su camino. Se utiliza el algoritmo de búsqueda en anchura (**BFS**) y se simula el proceso mediante programación en Python y pseudocódigo.

## Descripción del proyecto

A través de una matriz que representa el plano de un almacén, el robot:

1. Identifica su posición inicial y la ubicación de todos los paquetes.
2. Encuentra el camino más corto hacia el paquete más cercano, esquivando obstáculos.
3. Simula el movimiento del robot hasta el paquete.
4. Transporta el paquete a la zona de entrega.
5. Repite el proceso si existen más paquetes por recoger.

El comportamiento del robot se basa exclusivamente en lógica programada, lo que demuestra cómo mediante algoritmos se puede simular una inteligencia aparentemente autónoma.

---

## Tecnologías utilizadas

- **Python 3.10+**
- **NumPy**: para el manejo de la matriz del almacén.
- **collections.deque**: para implementar la cola de búsqueda del algoritmo BFS.
