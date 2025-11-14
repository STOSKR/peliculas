# Películas API

API REST con Django y DRF para buscar películas y ver su información detallada. Los datos se obtienen de OMDB API.

## 📑 Índice

- [Colección de Postman](#-colección-de-postman)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Endpoints Expuestos](#endpoints-expuestos)
  - [Autenticación](#autenticación)
  - [Películas](#películas)
  - [Favoritos](#favoritos)
- [Decisiones Técnicas](#decisiones-técnicas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Buenas Prácticas Implementadas](#buenas-prácticas-implementadas)
- [Mejoras Futuras](#mejoras-futuras)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)

## 📦 Colección de Postman

Incluye una colección de Postman lista para usar: `Movie_API.postman_collection.json`

**Para importarla:**
1. Abre Postman
2. Click en "Import"
3. Selecciona el archivo `Movie_API.postman_collection.json`
4. La colección incluye todos los endpoints con autenticación JWT configurada

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

## Endpoints Expuestos

### Autenticación

Todos los endpoints de películas y favoritos requieren autenticación JWT.

#### 1. Login - Obtener Tokens

**Endpoint:** `POST /api/auth/login/`  
**Autenticación:** No requerida

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

**Error - Credenciales inválidas (401 Unauthorized):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

**Error - Campos faltantes (400 Bad Request):**
```json
{
  "username": ["This field is required."],
  "password": ["This field is required."]
}
```

**Usuarios disponibles:**
- `admin` / `admin123` (superusuario)
- `usuario1` / `pass123`
- `usuario2` / `pass123`

#### 2. Refresh - Renovar Access Token

**Endpoint:** `POST /api/auth/refresh/`  
**Autenticación:** No requerida

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

**Error - Refresh token inválido o expirado (401 Unauthorized):**
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

**Error - Campo faltante (400 Bad Request):**
```json
{
  "refresh": ["This field is required."]
}
```

**Configuración de tokens:**
- **Access Token**: Válido por 1 hora
- **Refresh Token**: Válido por 7 días

**Uso del token:**  
Incluye el access token en el header `Authorization` de cada petición:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

### Películas

#### 3. Buscar Películas

**Endpoint:** `GET /api/movies/search/`  
**Autenticación:** Requerida (JWT)

**Parámetros:**
- `query` (requerido): Término de búsqueda
- `page` (opcional): Número de página (default: 1)

**Ejemplo:**
```bash
GET http://localhost:8000/api/movies/search/?query=matrix&page=1
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta exitosa (200 OK):**
```json
{
  "Search": [
    {
      "imdbID": "tt0133093",
      "Title": "The Matrix",
      "Year": "1999",
      "Type": "movie",
      "Poster": "https://..."
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

**Error - Sin autenticación (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Error - Token inválido (401 Unauthorized):**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

#### 4. Detalle de Película

**Endpoint:** `GET /api/movies/<imdb_id>/`  
**Autenticación:** Requerida (JWT)

**Parámetros:**
- `imdb_id` (requerido, en URL): ID de IMDB (ej: tt0133093)

**Ejemplo:**
```bash
GET http://localhost:8000/api/movies/tt0133093/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta exitosa (200 OK):**
```json
{
  "imdbID": "tt0133093",
  "Title": "The Matrix",
  "Year": "1999",
  "Rated": "R",
  "Released": "31 Mar 1999",
  "Runtime": "136 min",
  "Genre": "Action, Sci-Fi",
  "Director": "Lana Wachowski, Lilly Wachowski",
  "Actors": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
  "Plot": "A computer hacker learns from mysterious rebels...",
  "Poster": "https://...",
  "imdbRating": "8.7",
  "Type": "movie",
  "Response": "True"
}
```

**Error - Película no encontrada (200 OK):**
```json
{
  "Error": "Incorrect IMDb ID."
}
```

**Error - Sin autenticación (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Error - Token inválido (401 Unauthorized):**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

---

### Favoritos

#### 5. Listar Favoritos

**Endpoint:** `GET /api/movies/favorites/`  
**Autenticación:** Requerida (JWT)

**Ejemplo:**
```bash
GET http://localhost:8000/api/movies/favorites/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta exitosa (200 OK):**
```json
[
  {
    "imdb_id": "tt0133093",
    "title": "The Matrix",
    "year": "1999",
    "poster": "https://...",
    "added_at": "2025-11-14T10:30:00Z"
  }
]
```

**Respuesta con lista vacía (200 OK):**
```json
[]
```

**Error - Sin autenticación (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 6. Añadir a Favoritos

**Endpoint:** `POST /api/movies/favorites/`  
**Autenticación:** Requerida (JWT)

**Body (JSON):**
```json
{
  "imdb_id": "tt0133093",
  "title": "The Matrix",
  "year": "1999",
  "poster": "https://..."
}
```

**Respuesta exitosa (201 Created):**
```json
{
  "imdb_id": "tt0133093",
  "title": "The Matrix",
  "year": "1999",
  "poster": "https://...",
  "added_at": "2025-11-14T10:30:00Z"
}
```

**Error - Ya existe (400 Bad Request):**
```json
{
  "error": "Esta película ya está en favoritos"
}
```

**Error - Datos inválidos (400 Bad Request):**
```json
{
  "imdb_id": ["This field is required."],
  "title": ["This field is required."]
}
```

**Error - Sin autenticación (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Error - Token inválido (401 Unauthorized):**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

#### 7. Eliminar de Favoritos

**Endpoint:** `DELETE /api/movies/favorites/<imdb_id>/`  
**Autenticación:** Requerida (JWT)

**Ejemplo:**
```bash
DELETE http://localhost:8000/api/movies/favorites/tt0133093/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Respuesta exitosa (200 OK):**
```json
{
  "message": "Película eliminada de favoritos"
}
```

**Error - No encontrada (404 Not Found):**
```json
{
  "error": "Película no encontrada en favoritos"
}
```

**Error - Sin autenticación (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Error - Token inválido (401 Unauthorized):**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

---

### Resumen de Endpoints

| Método | Endpoint | Autenticación | Descripción |
|--------|----------|---------------|-------------|
| POST | `/api/auth/login/` | No | Obtener access y refresh tokens |
| POST | `/api/auth/refresh/` | No | Renovar access token |
| GET | `/api/movies/search/` | Sí | Buscar películas por nombre |
| GET | `/api/movies/<imdb_id>/` | Sí | Obtener detalle de película |
| GET | `/api/movies/favorites/` | Sí | Listar películas favoritas |
| POST | `/api/movies/favorites/` | Sí | Añadir película a favoritos |
| DELETE | `/api/movies/favorites/<imdb_id>/` | Sí | Eliminar película de favoritos |

## Autenticación

### Detalles de Implementación

Este API utiliza **JWT (JSON Web Tokens)** para autenticación. Los detalles de uso están en la sección [Endpoints Expuestos](#endpoints-expuestos).

## Decisiones Técnicas

### Arquitectura

He usado una **arquitectura en capas con patrón Repository** para mantener el código organizado y fácil de mantener:

```
movies/
├── views.py              # Controladores HTTP (reciben peticiones, devuelven respuestas)
├── services/             # Lógica de negocio
│   └── movie_service.py
├── repositories/         # Acceso a datos externos
│   └── omdb_repository.py
├── models.py             # Modelos de base de datos
└── serializers.py        # Transformación de datos para la API
```

**¿Por qué esta estructura?**

He separado las responsabilidades en capas para que el código quede más limpio:

1. **Views**: Se encargan solo de recibir la petición HTTP y devolver la respuesta. No tienen lógica de negocio.

2. **Services**: Aquí va la lógica. Por ejemplo, si necesito validar algo o combinar datos de varios sitios, lo hago aquí.

3. **Repositories**: Hablan con APIs externas (OMDB en este caso). Si mañana quiero cambiar OMDB por otra API, solo toco esta capa.

4. **Models**: Definen la estructura de la base de datos (en este caso, las películas favoritas).

5. **Serializers**: Convierten los datos del modelo a JSON y validan lo que llega del cliente.

Esta separación hace que sea fácil entender dónde está cada cosa y modificar una parte sin romper las demás.

### Framework y Dependencias

- **Django 5.1.3**: Framework web principal
- **Django REST Framework 3.15.2**: Para construir el API REST con vistas basadas en clases (APIView)
- **djangorestframework-simplejwt 5.3.1**: Autenticación JWT para DRF
- **django-cors-headers 4.6.0**: Manejo de CORS para permitir peticiones desde aplicaciones web cliente
- **python-decouple 3.8**: Gestión de configuración mediante variables de entorno
- **requests 2.32.3**: Cliente HTTP para consumir la API de OMDB

### Configuración CORS

Django por defecto bloquea peticiones desde otros orígenes (política CORS). Como el requisito era que pudiera consumirse desde una app Angular en `localhost:4200`, he tenido que configurarlo.

**Configuración en `settings.py`:**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',  # Angular dev server
]
```

Esto permite que una aplicación web corriendo en ese puerto pueda hacer fetch/XHR a la API sin problemas de CORS.

Si en el futuro se necesitan añadir más orígenes (por ejemplo, cuando la app esté en producción), solo habría que añadirlos a esta lista.

### Autenticación

He decidido usar **JWT (JSON Web Tokens)** porque es lo más habitual en APIs REST modernas.

**¿Cómo funciona?**
- El usuario envía sus credenciales a `/api/auth/login/`
- Si son correctas, recibe dos tokens:
  - **Access token**: dura 1 hora, se usa para acceder a la API
  - **Refresh token**: dura 7 días, sirve para renovar el access token sin volver a poner usuario/contraseña
- Para cada petición, el cliente incluye el access token en el header: `Authorization: Bearer <token>`
- Cuando el access token expira, usa el refresh token en `/api/auth/refresh/` para obtener uno nuevo

**Usuarios mock**

Como no hacía falta un sistema completo de gestión de usuarios, he creado 3 usuarios hardcoded con un comando Django:

```python
# python manage.py create_mock_users crea:
admin / admin123 (es superusuario, puede acceder al admin de Django)
usuario1 / pass123
usuario2 / pass123
```

**¿Por qué JWT y no sesiones?**
- JWT no necesita guardar nada en el servidor (stateless), cada token tiene toda la info que necesita
- Es más fácil de escalar: no hay que sincronizar sesiones entre servidores
- Funciona mejor para APIs que van a ser consumidas por apps móviles o SPAs

**Configuración**

Solo he configurado lo esencial en `settings.py`:
- Access token expira en 1 hora (suficiente para una sesión de trabajo normal)
- Refresh token expira en 7 días (para no tener que hacer login constantemente)

### Variables de Entorno

He usado **python-decouple** para manejar la configuración sensible que no debería estar en el código:

```env
SECRET_KEY=tu-clave-secreta-django
DEBUG=True
OMDB_API_KEY=tu-api-key-omdb
```

**¿Por qué python-decouple y no os.getenv()?**

Ambas opciones funcionan, pero `decouple` tiene ventajas:
- Convierte automáticamente tipos (bool, int, etc.)
- Lee archivos `.env` automáticamente
- Permite valores por defecto de forma más limpia
- Es más explícito y fácil de leer

Ejemplo:
```python
# Con decouple
DEBUG = config('DEBUG', default=False, cast=bool)

# Con os.getenv
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # menos claro
```

### Gestión de Favoritos

He implementado un sistema completo de favoritos con persistencia en SQLite:

**Decisiones de diseño:**

1. **Modelo simple**: Una tabla `Favorite` con los campos esenciales (usuario, película, fecha)

2. **imdb_id como clave primaria**: En lugar de usar el `id` autogenerado de Django, he usado `imdb_id` directamente como primary key porque:
   - Es único por naturaleza (IMDB garantiza IDs únicos)
   - Simplifica las queries (no necesito buscar por `id` interno)
   - Es más intuitivo en la API: `DELETE /favorites/tt0133093/` en vez de `/favorites/42/`

3. **Constraint de unicidad por usuario**: Un usuario no puede añadir la misma película dos veces
   ```python
   class Meta:
       unique_together = ('user', 'imdb_id')
   ```

4. **Manejo de duplicados**: Si intentas añadir una película que ya está en favoritos, retorna error 400 con mensaje claro

5. **Cada usuario ve solo sus favoritos**: Las queries filtran automáticamente por `request.user`

**Endpoints:**
- `GET /api/movies/favorites/` - Lista tus favoritos
- `POST /api/movies/favorites/` - Añade una película (requiere: imdb_id, title, year, poster)
- `DELETE /api/movies/favorites/<imdb_id>/` - Elimina de favoritos

### Manejo de Errores

**Validación de entrada:**
- Si falta el parámetro `query` en búsqueda → `400 Bad Request`
- Si el body de crear favorito es inválido → `400 Bad Request` con detalles del error
- Si intentas añadir una película ya en favoritos → `400 Bad Request` con mensaje explicativo

**Errores de base de datos:**
- Django lanza `IntegrityError` cuando hay duplicados en favoritos
- Lo he capturado para devolver un mensaje amigable en vez de un error 500

**Errores de API externa (OMDB):**
- Si OMDB retorna error en búsqueda → lo convierto a lista vacía (para dar mejor UX)
- Si OMDB retorna error en detalle → reenvío el mensaje de error tal cual
- Si hay error de red → Django devuelve 500 (como mejora futura, habría que capturar esto y dar un mensaje más claro)

**Errores de autenticación:**
- Sin token o token inválido → `401 Unauthorized`
- Token expirado → `401 Unauthorized` (cliente debe usar refresh token)

### Base de Datos

He usado **SQLite** (la base de datos por defecto de Django) porque:
- Es suficiente para el alcance de este proyecto
- No requiere instalación ni configuración adicional
- Es fácil de versionar y distribuir para hacer pruebas
- Se podría migrar a PostgreSQL o MySQL sin problemas si el proyecto crece

**Tablas principales:**
- `auth_user`: Usuarios de Django (admin, usuario1, usuario2)
- `movies_favorite`: Películas favoritas de cada usuario

### Caché

No está implementado todavía, pero sería una buena mejora para:
- **Reducir llamadas a OMDB**: La API gratuita tiene límite de 1000 peticiones al día
- **Mejorar rendimiento**: Cachear búsquedas populares y detalles de películas

**Implementación futura:**
- Redis con Django Cache Framework
- Cache de 1 hora para detalles de películas (no cambian frecuentemente)
- Cache de 30 minutos para búsquedas

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

- **Arquitectura en capas**: Separación clara entre views, services y repositories
- **Variables de entorno**: Configuración sensible fuera del código (SECRET_KEY, API keys)
- **Validación de datos**: Serializers de DRF para validar entrada del usuario
- **Manejo de errores**: Mensajes claros y códigos HTTP apropiados
- **CORS configurado**: Permite consumo desde aplicaciones web
- **Autenticación robusta**: JWT con access y refresh tokens
- **Código limpio**: PEP 8, nombres descriptivos, funciones con responsabilidad única
- **Constraint de BD**: `unique_together` para evitar duplicados en favoritos
- **Usuarios aislados**: Cada usuario solo ve sus propios favoritos  

## Mejoras Futuras

Si tuviera más tiempo, añadiría:

- **Caché**: Redis para reducir llamadas a OMDB y mejorar tiempos de respuesta
- **Rate limiting**: Limitar peticiones por usuario para evitar abuso
- **Filtros y búsqueda**: Buscar dentro de favoritos, ordenar por fecha/título

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

