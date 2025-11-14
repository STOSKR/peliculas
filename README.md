# Películas API

API REST desarrollado con Django y Django REST Framework para consultar información de películas desde la API de OMDB.

## Descripción

Esta aplicación expone un API REST que permite buscar películas por nombre y acceder a su información detallada. Internamente, la aplicación consulta la API de OMDB (Open Movie Database) para obtener los datos de las películas.

## Requisitos Previos

- Python 3.8+
- pip (gestor de dependencias de Python)
- Una API Key de OMDB (gratuita): http://www.omdbapi.com/apikey.aspx

## Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/STOSKR/peliculas.git
cd peliculas
```

### 2. Crear entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
SECRET_KEY=tu-secret-key-django
DEBUG=True
OMDB_API_KEY=tu-api-key-de-omdb
```

**Nota:** Para obtener una API Key de OMDB (gratuita): http://www.omdbapi.com/apikey.aspx

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Crear usuarios mock

```bash
python manage.py create_mock_users
```

Esto creará 3 usuarios hardcoded:
- `admin` / `admin123` (superusuario)
- `usuario1` / `pass123`
- `usuario2` / `pass123`

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000`

## Autenticación

Este API utiliza **JWT (JSON Web Tokens)** para autenticación. Todos los endpoints de películas requieren autenticación.

### Obtener Token de Acceso

**Endpoint:** `POST /api/auth/login/`

**Body (JSON):**
```json
{
  "username": "usuario1",
  "password": "pass123"
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refrescar Token

**Endpoint:** `POST /api/auth/refresh/`

**Body (JSON):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta exitosa (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar el Token en las Peticiones

Para acceder a los endpoints protegidos, incluye el token en el header `Authorization`:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Ejemplo con curl:**
```bash
curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
     http://localhost:8000/api/movies/search/?query=matrix
```

### Configuración de Tokens

- **Access Token**: Válido por 1 hora
- **Refresh Token**: Válido por 7 días

## Endpoints Expuestos

### 1. Búsqueda de Películas

Permite buscar películas por nombre o término de búsqueda.

**Endpoint:** `GET /api/movies/search/`
**Autenticación:** Requerida (JWT)

**Parámetros:**
- `query` (requerido): Término de búsqueda
- `page` (opcional): Número de página para resultados paginados (default: 1)

**Ejemplo de uso:**
```bash
GET http://localhost:8000/api/movies/search/?query=guardians&page=1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta exitosa (200 OK):**
```json
{
  "Search": [
    {
      "imdbID": "tt2015381",
      "Title": "Guardians of the Galaxy",
      "Year": "2014",
      "Type": "movie",
      "Poster": "https://m.media-amazon.com/images/..."
    },
    {
      "imdbID": "tt3896198",
      "Title": "Guardians of the Galaxy Vol. 2",
      "Year": "2017",
      "Type": "movie",
      "Poster": "https://m.media-amazon.com/images/..."
    }
  ],
  "totalResults": "15",
  "Response": "True"
}
```

**Respuesta sin resultados (200 OK):**
```json
{
  "Search": [],
  "totalResults": "0",
  "Response": "True"
}
```

**Error - Parámetro faltante (400 Bad Request):**
```json
{
  "error": "Query parameter is required"
}
```

### 2. Detalle de Película

Obtiene información detallada de una película específica mediante su ID de IMDB.

**Endpoint:** `GET /api/api/movies/<imdb_id>/`
**Autenticación:** Requerida (JWT)

**Parámetros:**
- `imdb_id` (requerido, en URL): ID de IMDB de la película (ej: tt0133093)

**Ejemplo de uso:**
```bash
GET http://localhost:8000/api/movies/tt2015381/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta exitosa (200 OK):**
```json
{
  "imdbID": "tt2015381",
  "Title": "Guardians of the Galaxy",
  "Year": "2014",
  "Rated": "PG-13",
  "Released": "01 Aug 2014",
  "Runtime": "121 min",
  "Genre": "Action, Adventure, Comedy",
  "Director": "James Gunn",
  "Writer": "James Gunn, Nicole Perlman, Dan Abnett",
  "Actors": "Chris Pratt, Zoe Saldana, Dave Bautista",
  "Plot": "A group of intergalactic criminals must pull together to stop a fanatical warrior...",
  "Language": "English",
  "Country": "United States",
  "Awards": "Nominated for 2 Oscars. 52 wins & 103 nominations total",
  "Poster": "https://m.media-amazon.com/images/...",
  "Metascore": "76",
  "imdbRating": "8.0",
  "imdbVotes": "1,200,000",
  "Type": "movie",
  "Response": "True"
}
```

**Error - Película no encontrada (200 OK con error):**
```json
{
  "Error": "Incorrect IMDb ID."
}
```

## Decisiones Técnicas

### Arquitectura

El proyecto implementa una **arquitectura en capas con patrón Repository** para mantener una clara separación de responsabilidades:

```
movies/
├── views.py              # Capa de presentación (controladores HTTP)
├── services/             # Capa de lógica de negocio
│   └── movie_service.py
└── repositories/         # Capa de acceso a datos
    └── omdb_repository.py
```

**Capas:**

1. **Views (Controladores)**: Manejan las peticiones HTTP, validan parámetros de entrada y retornan respuestas HTTP apropiadas.

2. **Services (Lógica de negocio)**: Orquestan las operaciones, aplican reglas de negocio y transforman datos cuando es necesario.

3. **Repositories (Acceso a datos)**: Abstraen la comunicación con APIs externas (OMDB). Esta capa podría fácilmente cambiarse para usar otra fuente de datos sin afectar el resto del código.

**Ventajas de esta arquitectura:**
- **Testabilidad**: Cada capa puede ser testeada independientemente
- **Mantenibilidad**: Cambios en una capa no afectan a las demás
- **Escalabilidad**: Fácil agregar nuevas funcionalidades o fuentes de datos
- **Claridad**: Separación clara de responsabilidades

### Framework y Dependencias

- **Django 5.1.3**: Framework web principal
- **Django REST Framework 3.15.2**: Para construir el API REST con vistas basadas en clases (APIView)
- **djangorestframework-simplejwt 5.3.1**: Autenticación JWT para DRF
- **django-cors-headers 4.6.0**: Manejo de CORS para permitir peticiones desde aplicaciones web cliente
- **python-decouple 3.8**: Gestión de configuración mediante variables de entorno
- **requests 2.32.3**: Cliente HTTP para consumir la API de OMDB

### Configuración CORS

El proyecto está configurado para permitir peticiones CORS desde aplicaciones web cliente. Específicamente, se permite el acceso desde:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',  # Angular development server
]
```

Esto habilita que una aplicación Angular (u otro framework frontend) corriendo en `localhost:4200` pueda realizar llamadas XHR/Fetch al API sin problemas de CORS.

**Ubicación:** `peli/settings.py`

### Autenticación

Actualmente, el API implementa **autenticación JWT (JSON Web Tokens)** con usuarios mock hardcoded.

**Implementación:**
- **Simple JWT**: Librería `djangorestframework-simplejwt` para gestión de tokens
- **Usuarios mock**: 3 usuarios hardcoded creados mediante comando de Django
- **Access Token**: Válido por 1 hora
- **Refresh Token**: Válido por 7 días
- **Algoritmo**: HS256

**Flujo de autenticación:**
1. Usuario envía credenciales a `/api/auth/login/`
2. Si son válidas, recibe `access_token` y `refresh_token`
3. Incluye `access_token` en header `Authorization: Bearer <token>` para cada petición
4. Cuando expira, usa `refresh_token` en `/api/auth/refresh/` para obtener nuevo `access_token`

**Usuarios disponibles (hardcoded):**
```python
# Creados con: python manage.py create_mock_users
admin / admin123 (superusuario)
usuario1 / pass123
usuario2 / pass123
```

**Endpoints de autenticación:**
- `POST /api/auth/login/` - Obtener tokens (access + refresh)
- `POST /api/auth/refresh/` - Refrescar access token

**Ventajas de JWT:**
- Stateless: no requiere almacenar sesiones en servidor
- Escalable: ideal para APIs REST
- Seguro: firmado con clave secreta
- Auto-contenido: incluye información del usuario

**Alternativas consideradas pero no implementadas:**
- Token Authentication: más simple pero requiere almacenamiento en BD
- Session Authentication: no ideal para APIs REST stateless
- OAuth2: demasiado complejo para este MVP

### Gestión de Configuración

Se utiliza **python-decouple** para gestionar configuración sensible mediante variables de entorno:
- `SECRET_KEY`: Clave secreta de Django
- `DEBUG`: Modo debug (True/False)
- `OMDB_API_KEY`: Clave de API de OMDB

También se puede implementar con os y hacer llamadas con os.getenv("KEY"), pero con python-decouple queda mucho más limpio y simple

### Manejo de Errores

**Validación de parámetros:**
- Si falta el parámetro `query` en búsqueda: retorna `400 Bad Request`

**Errores de API externa:**
- La capa de servicio normaliza las respuestas de error de OMDB
- Si OMDB retorna error en búsqueda: se convierte a respuesta vacía válida
- Si OMDB retorna error en detalle: se reenvía el mensaje de error

**Errores de conexión:**
- Actualmente, errores HTTP de `requests` se propagan como `500 Internal Server Error`
- Mejora futura: implementar try/catch para errores de red y timeouts

### Base de Datos

El proyecto utiliza **SQLite** (base de datos por defecto de Django). 
Actualmente no se persiste ninguna información localmente, pero la infraestructura está lista para implementar funcionalidades como:
- Películas favoritas de usuarios
- Caché de búsquedas frecuentes
- Historial de búsquedas

### Caché

**No implementado actualmente**, pero se considera para optimización futura:

**Opciones evaluadas:**
- **Django Cache Framework**: con backend Redis para cachear respuestas de OMDB
- **Tiempo de vida**: 1-24 horas dependiendo del tipo de datos
- **Estrategia**: Cache-aside pattern

**Beneficios:**
- Reducir llamadas a API externa (límites de rate)
- Mejorar tiempos de respuesta
- Reducir costos si se usa API de pago

## Estructura del Proyecto

```
peliculas/
├── manage.py                 # Script de gestión de Django
├── requirements.txt          # Dependencias del proyecto
├── db.sqlite3               # Base de datos SQLite
├── .env                     # Variables de entorno (no incluido en Git)
├── peli/                    # Configuración del proyecto Django
│   ├── settings.py          # Configuración principal
│   ├── urls.py              # URLs raíz del proyecto
│   └── wsgi.py              # Punto de entrada WSGI
└── movies/                  # Aplicación principal
    ├── views.py             # Controladores HTTP (APIView)
    ├── urls.py              # URLs de la app movies
    ├── models.py            # Modelos de datos (vacío actualmente)
    ├── services/
    │   └── movie_service.py # Lógica de negocio
    └── repositories/
        └── omdb_repository.py # Comunicación con OMDB API
```

## Buenas Prácticas Implementadas

✅ **Separación de responsabilidades** mediante arquitectura en capas  
✅ **Principio DRY** (Don't Repeat Yourself)  
✅ **Variables de entorno** para configuración sensible  
✅ **Gestión de dependencias** con requirements.txt  
✅ **Código idiomático Python** siguiendo PEP 8  
✅ **Vistas basadas en clases** de DRF para mejor organización  
✅ **Validación de parámetros** en endpoints  
✅ **Respuestas HTTP semánticas** con códigos de estado apropiados  
✅ **Configuración CORS** para aplicaciones web cliente  

## Mejoras Futuras

- [ ] Implementar autenticación (Token/JWT)
- [ ] Agregar sistema de películas favoritas con persistencia en BD
- [ ] Implementar caché para optimizar llamadas a OMDB
- [ ] Agregar tests unitarios y de integración
- [ ] Implementar paginación personalizada
- [ ] Agregar logging estructurado
- [ ] Documentación automática con Swagger/OpenAPI
- [ ] Rate limiting para proteger el API
- [ ] Dockerización del proyecto

## Tecnologías Utilizadas

- **Python 3.x**
- **Django 5.1.3** - Framework web
- **Django REST Framework 3.15.2** - Construcción de API REST
- **djangorestframework-simplejwt 5.3.1** - Autenticación JWT
- **django-cors-headers 4.6.0** - Soporte CORS
- **python-decouple 3.8** - Gestión de configuración
- **requests 2.32.3** - Cliente HTTP
- **SQLite** - Base de datos

## API Externa Utilizada

- **OMDB API** (Open Movie Database): http://www.omdbapi.com/
  - Proporciona información detallada sobre películas, series y episodios
  - Requiere API Key gratuita
  - Límite: 1000 peticiones diarias en plan gratuito

## Autor

Proyecto desarrollado como prueba técnica para demostrar conocimientos en Django, Django REST Framework y diseño de APIs REST.

