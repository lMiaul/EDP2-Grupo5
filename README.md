# Sistema LogiStock Cacao 🍫

**LogiStock Cacao** es una aplicación web interactiva desarrollada en **Streamlit** para la gestión del proceso de acopio de cacao. El sistema permite registrar agricultores, gestionar ingresos de sacos de cacao y visualizar métricas operativas mediante un dashboard administrativo.

La aplicación se ejecuta sobre una arquitectura contenerizada usando **Docker Compose**, integrando una aplicación **Streamlit** con una base de datos **MongoDB** local persistente.

---

# Arquitectura del Sistema

El proyecto está compuesto por dos servicios principales orquestados mediante Docker Compose:

| Servicio | Tecnología | Descripción |
|----------|------------|-------------|
| `web` | Streamlit + Python | Aplicación principal del sistema |
| `mongodb` | MongoDB | Base de datos NoSQL para almacenamiento persistente |

### Arquitectura de Contenedores

```text
┌───────────────────────┐
│   Streamlit (web)     │
│   logistock_app       │
│   Port: 8501          │
└───────────┬───────────┘
            │
            │ mongodb://mongodb:27017/
            │
┌───────────▼───────────┐
│      MongoDB          │
│    logistock_db       │
│    Port: 27017        │
└───────────────────────┘
            │
            ▼
     Volumen Persistente
        mongo_data
```

---

# Vistas y Roles

El sistema cuenta con dos módulos principales dependiendo del rol del usuario autenticado.

## 1. Vista Acopiador

Archivo:

```text
pages/1_Acopiador.py
```

Funciones principales:

- Registro del ingreso de sacos de cacao.
- Asociación del acopio a agricultores registrados.
- Gestión operativa del proceso de recepción.

### Credenciales Demo

```text
Usuario: acopiador@valleverde.com
Contraseña: 123
```

---

## 2. Vista Administrador / Dashboard

Archivo:

```text
pages/2_Dashboard.py
```

Funciones principales:

- Visualización de KPIs del negocio.
- Estadísticas de acopio.
- Reportes gráficos y métricas operativas.
- Monitoreo general del sistema.

### Credenciales Demo

```text
Usuario: admin@valleverde.com
Contraseña: admin
```

---

# Tecnologías Utilizadas

- **Frontend / Lógica de Aplicación:** Streamlit
- **Backend:** Python
- **Base de Datos:** MongoDB
- **Contenerización:** Docker
- **Orquestación:** Docker Compose

---

# Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Docker
- Docker Compose

Verifica la instalación ejecutando:

```bash
docker --version
docker compose version
```

---

# Estructura de Servicios Docker

El proyecto utiliza el siguiente esquema de servicios:

### Servicio `web`

Responsable de ejecutar la aplicación Streamlit.

Configuración principal:

- Construcción mediante `Dockerfile`
- Puerto expuesto: `8501`
- Dependencia de MongoDB
- Reinicio automático (`restart: always`)

Variables de entorno internas:

```env
MONGO_URL=mongodb://mongodb:27017/
DB_NAME=cac_valleverde
```

---

### Servicio `mongodb`

Responsable del almacenamiento persistente de datos.

Configuración principal:

- Imagen oficial de MongoDB
- Puerto expuesto: `27017`
- Persistencia mediante volumen Docker
- Reinicio automático (`restart: always`)

Volumen persistente:

```text
mongo_data
```

Esto evita la pérdida de información incluso si el contenedor es detenido o reiniciado.

---

# Ejecución del Proyecto

## 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

---

## 2. Construir e Iniciar los Servicios

Desde la raíz del proyecto, donde se encuentra el archivo `docker-compose.yml`, ejecutar:

```bash
docker compose up --build
```

Para ejecutarlo en segundo plano:

```bash
docker compose up -d --build
```

Este comando realizará automáticamente:

- Construcción de la imagen de la aplicación.
- Levantamiento del contenedor Streamlit.
- Levantamiento del contenedor MongoDB.
- Creación del volumen persistente.
- Configuración de red entre contenedores.

---

## 3. Acceder a la Aplicación

Una vez iniciados los servicios, abre tu navegador en:

```text
http://localhost:8501
```

---

## 4. Verificar Contenedores Activos

Puedes verificar que ambos servicios estén ejecutándose con:

```bash
docker ps
```

Deberías visualizar algo similar a:

```text
logistock_app
logistock_db
```

---

## 5. Detener la Aplicación

Para detener todos los servicios:

```bash
docker compose down
```

---

## 6. Eliminar Contenedores y Volúmenes (Opcional)

Si deseas reiniciar completamente la base de datos:

```bash
docker compose down -v
```

⚠️ Este comando eliminará todos los datos almacenados en MongoDB.

---

# Persistencia de Datos

MongoDB utiliza un volumen persistente:

```yaml
volumes:
  mongo_data:
```

Esto garantiza que la información registrada no se pierda aunque el contenedor sea apagado o reconstruido.

---

# Variables de Entorno

Actualmente las variables de entorno son gestionadas directamente desde `docker-compose.yml`, por lo que **no es necesario un archivo `.env`** para la conexión con la base de datos.

```yaml
environment:
  - MONGO_URL=mongodb://mongodb:27017/
  - DB_NAME=cac_valleverde
```

---

# Desarrollo y Actualización

Si realizas cambios en el código fuente y necesitas reconstruir la imagen:

```bash
docker compose up --build
```

Para reconstrucción limpia:

```bash
docker compose build --no-cache
docker compose up
```

---

# Consideraciones Técnicas

- La aplicación Streamlit espera que MongoDB esté disponible antes de iniciar (`depends_on`).
- La comunicación entre servicios ocurre mediante la red interna de Docker.
- El hostname `mongodb` funciona como alias interno del contenedor de base de datos.
- La base de datos utilizada es:

```text
cac_valleverde
```

---

# Autor

Proyecto desarrollado para la gestión de acopio de cacao **LogiStock Cacao** 🍫