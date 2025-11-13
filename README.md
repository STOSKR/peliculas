# Películas API

API REST desarrollado con Django y Django REST Framework para consultar información de películas desde TMDB.

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Clonar el repositorio

2. Crear entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Copiar `.env.example` a `.env` y configurar:
```
SECRET_KEY=tu-secret-key
DEBUG=True
TMDB_API_KEY=tu-api-key-de-tmdb
```

Para obtener TMDB API Key: https://www.themoviedb.org/settings/api

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Ejecutar servidor:
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
movies/
├── repositories/     # Abstracción de acceso a datos
├── services/         # Lógica de negocio
├── serializers/      # Validación y transformación de datos
└── views.py          # Controladores HTTP
```

## Arquitectura

El proyecto sigue el patrón Repository con separación en capas:

- **Views**: Controladores que manejan peticiones HTTP
- **Serializers**: Validación y serialización de datos
- **Services**: Lógica de negocio y orquestación
- **Repositories**: Abstracción del acceso a datos (TMDB API + SQLite)

## Tecnologías

- Django 5.1.3
- Django REST Framework 3.15.2
- django-cors-headers 4.6.0
- python-decouple 3.8
- requests 2.32.3

## CORS

Configurado para permitir peticiones desde:
- http://localhost:4200 (Angular)
