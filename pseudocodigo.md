```
// -------------------------------
// Constantes de tipos de celda
// -------------------------------
CELDA_VACIA ← 0
CELDA_OBSTACULO ← 1
CELDA_ROBOT ← 2
CELDA_PAQUETE ← 3
CELDA_ENTREGA ← 4

// -------------------------------
// MATRIZ DEL ALMACÉN
// (ejemplo 5x5, se puede modificar)
// -------------------------------
plano_almacen ← [
    [0, 0, 0, 1, 0],
    [0, 2, 0, 1, 3],
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0],
    [3, 0, 0, 0, 4]
]

// -------------------------------
// FUNCIONES
// -------------------------------

Funcion BuscarCeldasConValor(valor, matriz)
    coordenadas ← lista vacía

    Para fila desde 0 hasta número de filas - 1
        Para columna desde 0 hasta número de columnas - 1
            Si matriz[fila][columna] = valor Entonces
                Agregar (fila, columna) a coordenadas
            FinSi
        FinPara
    FinPara

    Retornar coordenadas
FinFuncion


Funcion EncontrarCaminoMasCorto(inicio, destino, matriz)
    filas ← número de filas de la matriz
    columnas ← número de columnas de la matriz

    visitado ← matriz de [filas][columnas] con todos los valores en FALSO
    cola ← nueva cola
    Encolar (inicio, [inicio])  // cada elemento es (posición_actual, camino_recorrido)

    direcciones ← [(-1, 0), (1, 0), (0, -1), (0, 1)]  // arriba, abajo, izq, der

    Mientras cola no esté vacía
        (posicion_actual, camino_actual) ← desencolar de cola
        (fila, columna) ← posicion_actual

        Si posicion_actual = destino Entonces
            Retornar camino_actual
        FinSi

        Para cada (df, dc) en direcciones
            nueva_fila ← fila + df
            nueva_columna ← columna + dc

            Si nueva_fila y nueva_columna están dentro de la matriz Y
               no visitado[nueva_fila][nueva_columna] Y
               matriz[nueva_fila][nueva_columna] ≠ CELDA_OBSTACULO Entonces

                Marcar visitado[nueva_fila][nueva_columna] como VERDADERO
                nuevo_camino ← copia de camino_actual + (nueva_fila, nueva_columna)
                Encolar ( (nueva_fila, nueva_columna), nuevo_camino )
            FinSi
        FinPara
    FinMientras

    Retornar NULO  // no se encontró camino posible
FinFuncion


Subproceso SimularMovimiento(camino)
    Para i desde 0 hasta largo de camino - 1
        posicion ← camino[i]

        Si i = 0 Entonces
            Mostrar "📍 El robot parte en", posicion
        Sino
            Mostrar "➡️ El robot se mueve a", posicion
        FinSi
    FinPara
FinSubproceso


Subproceso IniciarRecoleccionYEntrega(plano, pos_robot, pos_entrega)
    paquetes ← BuscarCeldasConValor(CELDA_PAQUETE, plano)
    total_paquetes ← cantidad de paquetes
    entregados ← 0

    Para cada paquete en paquetes
        camino_al_paquete ← EncontrarCaminoMasCorto(pos_robot, paquete, plano)

        Si camino_al_paquete es NULO Entonces
            Mostrar "❌ No se pudo llegar al paquete en", paquete
            Continuar con el siguiente paquete
        FinSi

        SimularMovimiento(camino_al_paquete)
        Mostrar "✅ Paquete recogido en", paquete
        entregados ← entregados + 1
        plano[paquete] ← CELDA_VACIA
        pos_robot ← paquete

        camino_a_entrega ← EncontrarCaminoMasCorto(pos_robot, pos_entrega, plano)

        Si camino_a_entrega es NULO Entonces
            Mostrar "❌ No se pudo entregar desde", pos_robot
            Continuar
        FinSi

        SimularMovimiento(camino_a_entrega)
        Mostrar "📦 Paquete entregado en", pos_entrega
        pos_robot ← pos_entrega
    FinPara

    Si entregados > 0 Entonces
        Mostrar "🎉 Se entregaron", entregados, "de", total_paquetes, "paquetes."
    Sino
        Mostrar "😭 No se pudieron entregar paquetes."
    FinSi
FinSubproceso


// -------------------------------
// PROCESO PRINCIPAL
// -------------------------------

Inicio
    pos_robot ← BuscarCeldasConValor(CELDA_ROBOT, plano_almacen)[0]
    pos_entrega ← BuscarCeldasConValor(CELDA_ENTREGA, plano_almacen)[0]

    IniciarRecoleccionYEntrega(plano_almacen, pos_robot, pos_entrega)
Fin
```