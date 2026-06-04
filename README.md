# Sistema LogiStock Cacao 🍫

**LogiStock Cacao** es una aplicación web interactiva desarrollada en **Streamlit** para la gestión del proceso de acopio de cacao. El sistema permite registrar agricultores, gestionar ingresos de sacos de cacao y visualizar métricas operativas mediante un dashboard administrativo.

La aplicación se ejecuta sobre una arquitectura contenerizada usando **Docker Compose**, integrando una aplicación **Streamlit** con una base de datos **MongoDB** local persistente.

---

## Arquitectura del Sistema

El proyecto está compuesto por dos servicios principales orquestados mediante Docker Compose:

| Servicio | Tecnología | Descripción |
|----------|------------|-------------|
| `web` | Streamlit + Python | Aplicación principal del sistema (`logistock_app`) |
| `mongo` | MongoDB | Base de datos NoSQL para almacenamiento persistente (`logistock_mongo`) |

### Arquitectura de Contenedores

```text
┌───────────────────────┐
│   Streamlit (web)     │
│   logistock_app       │
│   Port: 8501          │
└───────────┬───────────┘
            │
            │ mongodb://mongo:27017/
            │
┌───────────▼───────────┐
│      MongoDB          │
│    logistock_mongo    │
│    Port: 27017        │
└───────────────────────┘
            │
            ▼
     Volumen Persistente
        mongo_data
```

---

## Características de Rendimiento y Despliegue

Recientemente se ha optimizado el sistema para garantizar un despliegue rápido y una experiencia de usuario fluida:

- **Autoseed de Base de Datos:** La base de datos MongoDB se inicializa automáticamente con datos de demostración (Agricultores, Usuarios y Acopios) a través de `scripts/init-mongo.js` en su primera ejecución. No es necesario correr scripts manuales de Jupyter.
- **Tiempos de Build Optimizados:** Se utiliza `.dockerignore` para excluir entornos virtuales (`.venv`), reduciendo el tamaño del contexto de build y acelerando la compilación.
- **Consultas cacheadas:** El dashboard utiliza la función `@st.cache_data` nativa de Streamlit para almacenar en memoria las respuestas de MongoDB, previniendo recargas lentas durante la interacción de datos y eliminando cuellos de botella.

---

## Vistas y Roles

El sistema cuenta con dos módulos principales dependiendo del rol del usuario autenticado.

### 1. Vista Acopiador

Archivo: `pages/1_Acopiador.py`

Funciones principales:
- Registro del ingreso de sacos de cacao.
- Asociación del acopio a agricultores registrados.
- Gestión operativa del proceso de recepción.

**Credenciales Demo:**
- **Usuario:** acopiador@valleverde.com
- **Contraseña:** 123

### 2. Vista Administrador / Dashboard

Archivo: `pages/2_Dashboard.py`

Funciones principales:
- Visualización de KPIs del negocio.
- Estadísticas de acopio.
- Reportes gráficos y métricas operativas.
- Monitoreo general del sistema.

**Credenciales Demo:**
- **Usuario:** admin@valleverde.com
- **Contraseña:** admin

---

## Tecnologías Utilizadas

- **Frontend / Lógica de Aplicación:** Streamlit
- **Backend:** Python
- **Base de Datos:** MongoDB
- **Contenerización:** Docker
- **Orquestación:** Docker Compose

---

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado Docker y Docker Desktop (si usas Windows/Mac). Verifica la instalación ejecutando:

```bash
docker --version
docker compose version
```

---

## Ejecución del Proyecto

### 1. Construir e Iniciar los Servicios

Desde la raíz del proyecto, ejecuta el siguiente comando para correrlo en segundo plano:

```bash
docker compose up -d --build
```

Este comando realizará automáticamente:
- Construcción de la imagen optimizada (ignorando archivos locales innecesarios).
- Levantamiento del contenedor MongoDB.
- **Inyección automática** de la semilla de datos a través de `init-mongo.js`.
- Levantamiento de la aplicación Streamlit conectada a MongoDB local.

### 2. Acceder a la Aplicación

Una vez iniciados los servicios, abre tu navegador en:

👉 **http://localhost:8501**

### 3. Verificar Contenedores Activos y Logs

Para verificar el estado de los servicios:
```bash
docker compose ps
```

Para ver los logs en tiempo real (útil para ver la carga inicial del seed):
```bash
docker compose logs -f
```

### 4. Detener la Aplicación

Para detener todos los servicios sin borrar datos:
```bash
docker compose down
```

### 5. Reiniciar la Base de Datos desde Cero

Si deseas borrar todos los datos (incluyendo el autoseed) para iniciar con una base de datos limpia:
```bash
docker compose down -v
```
*(Al volver a correr `docker compose up`, el script `init-mongo.js` volverá a poblar los datos de prueba iniciales).*

---

## Variables de Entorno

Las variables de conexión se inyectan a través del `docker-compose.yml` al contenedor web:

```env
MONGODB_URL=mongodb://mongo:27017/
DB_NAME=cac_valleverde
```

---

## Autor

Proyecto desarrollado para la gestión de acopio de cacao **LogiStock Cacao** 🍫