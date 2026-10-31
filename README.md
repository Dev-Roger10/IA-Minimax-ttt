# Tres en Raya con MiniMax

Juego de Tres en Raya (Tic-Tac-Toe) hecho con Python y Flask, donde la IA usa el algoritmo **MiniMax puro** (sin poda) para elegir su jugada. Tú juegas con `X` y la IA con `O`.

Con MiniMax la IA revisa todas las partidas posibles desde el tablero actual, así que nunca pierde: lo mejor que puedes lograr es un empate.

## Cómo funciona

- El tablero es una lista de 9 celdas (`'X'`, `'O'` o `''` si está vacía).
- Cuando haces clic en una celda, el navegador envía el tablero al servidor (`POST /mover`).
- El servidor marca tu jugada y prueba cada celda libre con `O`. Para cada una baja por el árbol de jugadas con `minimax()` hasta que alguien gana o se llena el tablero.
- Puntajes: `+10` si gana la IA, `-10` si gana el humano, `0` si empatan.
- La IA elige la celda con el puntaje más alto y el servidor devuelve el tablero actualizado y el estado de la partida (`continua`, `humano_gana`, `ia_gana` o `empate`).

La lógica está en [app.py](app.py) y la interfaz en [templates/index.html](templates/index.html).

## Requisitos

- Python 3.8 o superior
- Flask

## Instalación y uso

```bash
# opcional: entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

pip install flask
python app.py
```

Después abre http://localhost:5001 en el navegador.

## Estructura

```
.
├── app.py               # servidor Flask y algoritmo MiniMax
└── templates/
    └── index.html       # interfaz del juego
```

## Notas

- El marcador de victorias, empates y derrotas se guarda solo en la página, así que se reinicia al recargar.
- La interfaz usa iconos de [Tabler Icons](https://tabler.io/icons) desde un CDN, por lo que necesita conexión a internet para mostrarlos.
- Hay una versión más eficiente del mismo juego con poda alfa-beta, que usa el puerto 5002 para poder correr las dos a la vez.
