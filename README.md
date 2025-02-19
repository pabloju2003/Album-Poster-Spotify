# Album-Poster-Spotify
API para crear posters de Albums con el codigo de Spotify

-Cómo configurar y utilizar la API de Spotify para obtener datos de un álbum y generar un póster automáticamente con Python y PIL:

  1️⃣ Crear una Aplicación en la API de Spotify
  
      📌 Paso 1: Crear una cuenta de desarrollador en Spotify
            1.Ve a Spotify Developer Dashboard.
            2.Inicia sesión con tu cuenta de Spotify.
            3.Haz clic en "Create an App" (Crear una aplicación).
            4.Asigna un nombre a la aplicación (ejemplo: AlbumPosterApp).
            5.En "Description", pon cualquier descripción (ejemplo: App para generar pósters de álbumes).
            6.Acepta los términos y condiciones.
            7.Haz clic en "Create".
        
      📌 Paso 2: Obtener las credenciales (Client ID y Client Secret)
            8.Abre tu aplicación en el dashboard.
            9.Copia el "Client ID" y "Client Secret".
            10.Guárdalos, los necesitaremos más adelante.

  2️⃣ Instalar las Dependencias en Python
      Abre la terminal y ejecuta:
          pip install spotipy pillow requests colorthief      


-Pasos a seguir para crear el poster:

    1. Busca el album del que quieras crear el album.
    2. Copia el enlace.
    3. Ve a https://www.spotifycodes.com/#create y pega el enlace para crear el potify_code en formato .png
    4. Mueve el .png descargado a la carpeta de trabajo donde esté el script y cambiale el nombre al .png como spotify_code.
    5. Ejecuta en la terminal el script.
    6. Te pedirá que introduzcas el nombre del album del que quieras crear el poster.
    7. Luego te dejará introducir un nombre diferente para que aparezca el que tu quieras como el titulo del poster.
    8. Se creará la imagen formato .png dentro de la carpeta de trabajo.
