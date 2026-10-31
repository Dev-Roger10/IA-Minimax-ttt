"""
SUBTEMA 1: ALGORITMO MINIMAX
Juego: Tres en Raya (Tic-Tac-Toe)
La IA usa el algoritmo MiniMax puro para encontrar la mejor jugada.
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# El tablero es una lista de 9 posiciones (0 a 8, de izquierda a derecha y de arriba a abajo)
# donde cada celda guarda 'X', 'O' o '' si esta vacia.

def verificar_ganador(tablero, jugador):
    """Comprueba si un jugador ha ganado revisando filas, columnas y diagonales."""
    ganancias = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columnas
        [0, 4, 8], [2, 4, 6]               # diagonales
    ]
    for combo in ganancias:
        # gana si las tres celdas de la combinacion son del mismo jugador
        if all(tablero[i] == jugador for i in combo):
            return True
    return False

def obtener_movimientos_disponibles(tablero):
    """Retorna los indices de las celdas vacias."""
    return [i for i, celda in enumerate(tablero) if celda == '']

def tablero_lleno(tablero):
    """Devuelve True si no quedan celdas vacias."""
    return '' not in tablero

# MiniMax sin poda: recorre todo el arbol de jugadas posibles hasta llegar a un final
# (alguien gana o se llena el tablero) y va subiendo el mejor puntaje hacia la raiz.

def minimax(tablero, es_maximizador):
    """
    MiniMax recursivo sin poda.

    La IA ('O') es la que maximiza y el humano ('X') el que minimiza.
    Puntajes: +10 si gana la IA, -10 si gana el humano, 0 si empatan.
    """
    # casos base: si la partida ya termino no hay nada mas que explorar
    if verificar_ganador(tablero, 'O'):
        return 10
    if verificar_ganador(tablero, 'X'):
        return -10
    if tablero_lleno(tablero):
        return 0

    movimientos = obtener_movimientos_disponibles(tablero)

    if es_maximizador:
        # turno de la IA, se queda con el puntaje mas alto de sus opciones
        mejor_puntaje = float('-inf')
        for mov in movimientos:
            tablero[mov] = 'O'                          # prueba la jugada
            puntaje = minimax(tablero, False)            # ahora responde el humano
            tablero[mov] = ''                            # la deshace para probar la siguiente
            mejor_puntaje = max(mejor_puntaje, puntaje)
        return mejor_puntaje
    else:
        # turno del humano, la IA asume que va a elegir lo peor para ella
        mejor_puntaje = float('inf')
        for mov in movimientos:
            tablero[mov] = 'X'
            puntaje = minimax(tablero, True)
            tablero[mov] = ''
            mejor_puntaje = min(mejor_puntaje, puntaje)
        return mejor_puntaje

def obtener_mejor_movimiento(tablero):
    """
    Es el primer nivel del arbol: prueba cada celda libre con 'O',
    le pide el puntaje a minimax y se queda con la celda que dio el mayor.
    """
    mejor_puntaje = float('-inf')
    mejor_mov = None

    for mov in obtener_movimientos_disponibles(tablero):
        tablero[mov] = 'O'
        puntaje = minimax(tablero, False)   # despues de jugar 'O' le toca al humano
        tablero[mov] = ''
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_mov = mov

    return mejor_mov

@app.route('/')
def index():
    """Sirve la pagina principal del juego."""
    return render_template('index.html')

@app.route('/mover', methods=['POST'])
def mover():
    """
    Recibe el tablero y la celda que eligio el humano, la marca,
    y si la partida sigue responde con la jugada de la IA.
    """
    datos = request.json
    tablero = datos['tablero']
    indice_humano = datos['indice']

    tablero[indice_humano] = 'X'

    # si el humano cierra la partida, la IA ya no juega (mov_ia = -1)
    if verificar_ganador(tablero, 'X'):
        return jsonify({'tablero': tablero, 'estado': 'humano_gana', 'mov_ia': -1})

    if tablero_lleno(tablero):
        return jsonify({'tablero': tablero, 'estado': 'empate', 'mov_ia': -1})

    mov_ia = obtener_mejor_movimiento(tablero)
    tablero[mov_ia] = 'O'

    # la jugada de la IA tambien puede terminar la partida
    if verificar_ganador(tablero, 'O'):
        return jsonify({'tablero': tablero, 'estado': 'ia_gana', 'mov_ia': mov_ia})

    if tablero_lleno(tablero):
        return jsonify({'tablero': tablero, 'estado': 'empate', 'mov_ia': mov_ia})

    return jsonify({'tablero': tablero, 'estado': 'continua', 'mov_ia': mov_ia})

if __name__ == '__main__':
    # puerto 5001 para que no choque con la version de alfa-beta (5002)
    app.run(debug=True, port=5001)
