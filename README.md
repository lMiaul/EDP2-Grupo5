# Sistema LogiStock Cacao 🍫

LogiStock Cacao es una aplicación web interactiva desarrollada en **Streamlit** diseñada para gestionar el proceso de acopio de cacao. Conecta con una base de datos en **MongoDB** para almacenar la información de los usuarios, agricultores, y los registros de acopio.

## Vistas y Roles

El sistema cuenta con dos vistas principales dependiendo del rol del usuario que inicie sesión:

1. **Acopiador (`pages/1_Acopiador.py`)**:
   - Permite registrar el ingreso de nuevos sacos de cacao.
   - Vincula el acopio a agricultores registrados.
   - Credenciales Demo: `acopiador@valleverde.com` / `123`

2. **Administrador / Dashboard (`pages/2_Dashboard.py`)**:
   - Proporciona un panel de control (Dashboard) con KPIs del negocio.
   - Visualiza estadísticas de acopio, totales y gráficos relevantes.
   - Credenciales Demo: `admin@valleverde.com` / `admin`

## Servicios Seleccionados

1. **Frontend / Lógica de Aplicación**: [Streamlit](https://streamlit.io/) (Framework de Python rápido para aplicaciones de datos).
2. **Base de Datos**: [MongoDB Atlas](https://www.mongodb.com/atlas/database) (NoSQL en la nube) conectado mediante `pymongo`.

## Requisitos Previos

- Tener [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/install/) instalados en tu máquina.
- Un archivo `.env` configurado en la raíz del proyecto.

### Configuración del archivo `.env`

Asegúrate de crear un archivo llamado `.env` en la raíz del proyecto con la siguiente estructura (reemplazando los valores por los de tu base de datos MongoDB):

```env
MONGODB_URL="mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/"
DB_NAME="cac_valleverde"
```

## Ejecución con Docker

El proyecto ya incluye un `Dockerfile` y un `docker-compose.yml` listos para ser utilizados.

### 1. Construir e iniciar el contenedor

Abre tu terminal en la carpeta raíz del proyecto (donde se encuentra el archivo `docker-compose.yml`) y ejecuta el siguiente comando:

```bash
docker-compose up --build
```
*(Si quieres ejecutarlo en segundo plano, añade la bandera `-d`: `docker-compose up -d --build`)*

### 2. Acceder a la Aplicación

Una vez que el contenedor esté corriendo, abre tu navegador web y visita:

👉 **http://localhost:8501**

### 3. Detener la Aplicación

Para detener el contenedor en ejecución, puedes usar `Ctrl + C` en la terminal donde está corriendo, o ejecutar el siguiente comando desde otra terminal:

```bash
docker-compose down
```

## Notas Adicionales

- Durante la construcción de la imagen (`Dockerfile`), las dependencias son leídas del archivo `requirements.txt`.
- Hemos configurado un volumen en el `docker-compose.yml` (`.:/app`), lo que significa que los cambios que realices en el código local (`app.py`, `pages/`, etc.) se reflejarán automáticamente en el contenedor de Streamlit sin necesidad de reconstruir la imagen cada vez.