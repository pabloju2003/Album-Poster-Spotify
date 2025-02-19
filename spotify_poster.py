import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief
import textwrap
import io

# 📌 Configurar credenciales de Spotify
CLIENT_ID = "TU_CLIENT_ID"
CLIENT_SECRET = "TU_CLIENT_SECRET"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# 📌 Obtener la ruta donde está el script .py
script_dir = os.path.dirname(os.path.abspath(__file__))

# 🔍 Función para obtener datos del álbum
def obtener_datos_album(album_nombre):
    resultado = sp.search(q=album_nombre, type='album', limit=1)
    
    if resultado['albums']['items']:
        album = resultado['albums']['items'][0]
        titulo = album['name']
        artista = album['artists'][0]['name']
        imagen_url = album['images'][0]['url']
        codigo_spotify = f"https://open.spotify.com/album/{album['id']}"
        canciones = [track['name'] for track in sp.album_tracks(album['id'])['items']]

        # 📥 Descargar imagen del álbum
        imagen_respuesta = requests.get(imagen_url)
        imagen = Image.open(io.BytesIO(imagen_respuesta.content))

        # 🎨 Extraer colores predominantes
        color_thief = ColorThief(io.BytesIO(imagen_respuesta.content))
        paleta_colores = color_thief.get_palette(color_count=4)

        return titulo, artista, imagen, paleta_colores, codigo_spotify, canciones

    return None

# 📌 Buscar `spotify_code.png` en la misma carpeta que el script
def obtener_codigo_spotify():
    spotify_code_path = os.path.join(script_dir, "spotify_code.png")
    
    if os.path.exists(spotify_code_path):
        return Image.open(spotify_code_path).resize((280, 55))  # 📌 Reducido un poco, pero más ancho
    else:
        print("⚠️ Advertencia: No se encontró 'spotify_code.png'. Se generará el póster sin el código de Spotify.")
        return None

# 🎨 Generar el póster con título ajustado y Spotify Code más a la derecha
def generar_poster(titulo, artista, imagen, paleta_colores, canciones, codigo_spotify):
    # 📜 Crear el lienzo con margen
    ancho, alto = 1080, 1350
    margen_izq = 100  # Alinear todo a la izquierda
    margen_superior = 50
    margen_derecho = 100
    margen_inferior = 60  # Pequeño margen con la parte inferior
    poster = Image.new("RGB", (ancho, alto), "white")

    # 🖼️ Redimensionar y colocar la portada del álbum
    imagen = imagen.resize((900, 900))
    poster.paste(imagen, (margen_izq, margen_superior))  # Posición con margen

    # 🎨 Dibujar elementos en el póster
    draw = ImageDraw.Draw(poster)

    # 📌 Cargar fuentes con tamaño reducido para el título
    try:
        font_titulo = ImageFont.truetype("GothamBold.ttf", 30)  # 📌 Reducido de 35 a 30
        font_artista = ImageFont.truetype("GothamMedium.ttf", 26)  # 📌 Reducido de 28 a 26
        font_canciones = ImageFont.truetype("GothamBold.ttf", 16)  # Negrita
    except:
        font_titulo = ImageFont.truetype("arial.ttf", 40)
        font_artista = ImageFont.truetype("arial.ttf", 26)
        font_canciones = ImageFont.truetype("arialbd.ttf", 18)  # Arial en negrita

    # 📌 Ajustar el título en varias líneas sin colisionar con la paleta de colores
    max_ancho_titulo = (ancho // 2) + 80  # 📌 Más ancho sin colisionar con la paleta
    lineas_titulo = textwrap.wrap(titulo.upper(), width=25)  # Ajustado para mayor longitud

    # 📌 Dibujar el título línea por línea y calcular la nueva posición para el artista
    titulo_x = margen_izq
    titulo_y = margen_superior + 920  # Justo debajo de la portada
    for linea in lineas_titulo:
        draw.text((titulo_x, titulo_y), linea, fill="black", font=font_titulo)
        titulo_y += 35  # Espaciado entre líneas

    # 📌 Agregar nombre del artista debajo del título
    artista_y = titulo_y + 15  # Espacio entre título y artista
    draw.text((titulo_x, artista_y), artista, fill="black", font=font_artista)

    # 🎨 Dibujar la paleta de colores en su posición original
    x_color = ancho - margen_derecho - (60 * len(paleta_colores))
    y_color = margen_superior + 920
    for color in paleta_colores:
        draw.rectangle([x_color, y_color, x_color + 50, y_color + 50], fill=color)
        x_color += 60

    # 📌 Determinar el espacio restante para las canciones
    espacio_disponible = (alto - margen_inferior) - (artista_y + 50)
    espacio_entre_filas = 22  # Reducido para más filas
    canciones_por_columna = espacio_disponible // espacio_entre_filas  # Calcular dinámicamente

    # 🎵 Dibujar lista de canciones en columnas ajustando el ancho según la canción más larga
    columna_x = margen_izq
    columna_y_inicial = artista_y + 50  # Comienza debajo del artista
    y_text = columna_y_inicial
    max_y = alto - margen_inferior  # Espacio para evitar colisiones con el margen inferior

    # Calcular el ancho de la canción más larga de cada columna
    columnas = []
    canciones_por_columna_real = []
    numero_cancion = 1  # 🔹 Iniciar numeración desde 1 y continuar en cada columna

    for i in range(0, len(canciones), canciones_por_columna):
        columna_canciones = canciones[i:i + canciones_por_columna]
        columnas.append(columna_canciones)
        max_ancho_columna = max(draw.textlength(f"{numero_cancion + j}. {cancion}", font=font_canciones) for j, cancion in enumerate(columna_canciones))
        canciones_por_columna_real.append((columna_canciones, max_ancho_columna))

    for columna_canciones, max_ancho_columna in canciones_por_columna_real:
        for idx, cancion in enumerate(columna_canciones):
            draw.text((columna_x, y_text), f"{numero_cancion}. {cancion}", fill="black", font=font_canciones)
            y_text += espacio_entre_filas
            numero_cancion += 1  # 🔹 Incrementar el número de canción para que siga en la siguiente columna

        # Moverse a la siguiente columna con el ancho ajustado
        columna_x += max_ancho_columna + 30  # Espaciado dinámico
        y_text = columna_y_inicial  # Reiniciar la posición en Y para la nueva columna


    # 📌 Mover código de Spotify más a la derecha
    spotify_logo = obtener_codigo_spotify()
    if spotify_logo:
            poster.paste(spotify_logo, (ancho - margen_derecho - 280, alto - 100))  # 📌 Más a la derecha

    # 💾 Guardar el póster en la misma carpeta que el script
    poster_path = os.path.join(script_dir, "poster_album.png")
    poster.save(poster_path)
    poster.show()

    print(f"✅ Póster guardado en: {poster_path}")

# 🔹 Pedir datos al usuario
album_nombre = input("Introduce el nombre del álbum: ")
resultado_album = obtener_datos_album(album_nombre)

if resultado_album:
    titulo_real, artista, imagen, paleta_colores, codigo_spotify, canciones = resultado_album
    titulo_poster = input(f"Introduce el título que aparecerá en el póster (por defecto: {titulo_real}): ") or titulo_real
    generar_poster(titulo_poster, artista, imagen, paleta_colores, canciones, codigo_spotify)
else:
    print("❌ No se encontró el álbum en Spotify. Intenta con otro nombre.")
