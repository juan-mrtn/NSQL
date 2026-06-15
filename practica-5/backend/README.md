# Superheroes Backend API

Este proyecto corresponde al Backend de la Single Page Application (SPA) **"SUPERHEROES SPA"**. Está construido utilizando tecnologías modernas y de alto rendimiento orientadas al manejo de bases de datos NoSQL.

## Tecnologías Utilizadas

- **FastAPI**: Framework web de alto rendimiento para construir APIs con Python 3.11+.
- **MongoDB**: Base de datos NoSQL para almacenamiento estructurado en documentos.
- **Motor**: Driver asíncrono oficial de MongoDB para Python, lo que permite aprovechar al máximo la velocidad de FastAPI.
- **Pydantic V2**: Librería para la validación y transformación de datos (utilizada fuertemente para convertir y validar los `ObjectId` de Mongo).
- **Docker & Docker Compose**: Herramientas de orquestación para contenerizar el backend junto con la base de datos y el frontend.

## Arquitectura

El servidor expone una API REST con arquitectura de enrutamiento modular. Los archivos más importantes son:
- `main.py`: Punto de entrada de FastAPI, configura CORS y los eventos de inicio de ciclo de vida (`lifespan`).
- `database.py`: Configura la conexión asíncrona a MongoDB utilizando el driver `motor`.
- `models.py`: Define los esquemas (Schemas) utilizando Pydantic para validar entradas y salidas (DTOs). Incluye lógica especializada para castear `ObjectId` a `str`.
- `routers/superheroes.py`: Controladores REST que manejan las operaciones CRUD (Crear, Leer, Actualizar, Borrar) para la colección de superhéroes.
- `seeder.py`: Utilidad ejecutada al levantar el servidor que siembra (seed) 40 superhéroes iniciales en caso de que la base de datos esté vacía.

---

## El desafío de las imágenes de Yoolk

Una de las consignas fundamentales del proyecto era extraer todos los avatares de la página [Yoolk.ninja](https://yoolk.ninja/iconset/charavatar/). 
El desafío principal es que Yoolk aloja las imágenes en múltiples directorios según la fecha de subida (ej. `2019/07`, `2021/03`, etc.) y las resoluciones de los nombres de archivo varían drásticamente (algunos terminan en `-1024x819.png`, otros simplemente en `.png`). Esto hace imposible utilizar una función generadora genérica perfecta.

### ¿Cómo obtuvimos y mapeamos todos los links exactos?

El proceso se dividió en tres pasos automatizados para no tener que buscar manualmente a cada uno de los 40 héroes:

#### 1. Web Scraping (Extracción)
Primero, construimos un pequeño script en Python puro aprovechando `urllib` y la librería de expresiones regulares `re`. El script hizo una petición HTTP a la página principal de `charavatar` y filtró el código fuente en búsqueda de cualquier string que coincidiera con la expresión regular:
```regex
https://yoolk\.ninja/wp-content/uploads/\d{4}/\d{2}/[^\"\'\s>]+\.png
```
Con esto, recolectamos dinámicamente un archivo (`yoolk_images.txt`) conteniendo **389 URLs exactas** de imágenes png publicadas en el sitio.

#### 2. Fuzzy Matching (Coincidencia Difusa)
Luego, creamos un script (`patch_db.py`) que leyó directamente los documentos de nuestra colección local de MongoDB. Para cada uno de los héroes de la base de datos, extrajo su nombre y su "Casa" (Marvel / DC), lo normalizó (quitando guiones, mayúsculas y espacios), y buscó a través de las 389 URLs aquella que contuviera la mejor coincidencia. 

Si el héroe no contaba con avatar en el sitio web (lo cual sucedió con héroes menos conocidos o nombrados distinto), se le asignaba un patrón base por defecto para evitar errores en pantalla.

#### 3. Match Exacto y Actualización (Patching)
Dado que algunos héroes como "Cyborg" o "Wonder Woman" presentaban falsos positivos en el *fuzzy matching* por la forma en que Yoolk los nombró (`DC-Comics-Wonder-Woman-1024x819.png`), diseñamos un script final (`patch_exact.py`) que inyectó explícitamente las URLs faltantes a nuestra base de datos. 

Finalmente, actualizamos el código fuente nativo de `seeder.py` introduciendo un **diccionario hardcodeado** con los resultados de las extracciones exactas para garantizar que, si el contenedor se destruye o la base de datos se limpia en un entorno de corrección, la SPA continuará sirviendo los avatares correctos directamente de los servidores de Yoolk.
