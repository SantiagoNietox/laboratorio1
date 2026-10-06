# Sistema de Gestión de Usuarios con FastAPI, PostgreSQL, Prometheus y Grafana

Este proyecto consiste en una arquitectura de microservicios contenerizada con Docker y Docker Compose para la gestión y monitorización en tiempo real de usuarios.

---

## 1. Justificación y Explicación del Proyecto

El sistema fue diseñado integrando herramientas modernas para garantizar escalabilidad, aislamiento y observabilidad:

* **FastAPI**: Backend desarrollado en Python de alto rendimiento y bajo consumo. Se encarga de gestionar las operaciones CRUD de los usuarios y exponer el endpoint de métricas de Prometheus de forma nativa.
* **PostgreSQL**: Motor de base de datos relacional robusto que asegura la persistencia e integridad de los datos. Se encuentra configurado con volúmenes en Docker para evitar pérdida de información al reiniciar los contenedores.
* **Prometheus**: Sistema de monitorización basado en recolección por sondeo (*pull*). Realiza consultas periódicas cada 5 segundos al endpoint `/metrics` del backend para recolectar el estado operativo y el uso del sistema sin saturar la red.
* **Grafana**: Herramienta visual conectada a Prometheus para representar el comportamiento del servicio en tiempo real mediante tableros interactivos (conteo de usuarios registrados y tasa de peticiones).
* **Docker y Docker Compose**: Permite la orquestación, portabilidad y aislamiento completo de cada componente en una red bridge virtual, facilitando el levantamiento total de la infraestructura con un solo comando.

---

## 2. Estructura del Directorio

```text
user-crud-monitoring/
├── app/
│   ├── database.py       # Configuración de SQLAlchemy y conexión a PostgreSQL
│   ├── Dockerfile        # Imagen Docker para el backend de FastAPI
│   ├── main.py           # Endpoints CRUD y definición de métricas
│   ├── models.py         # Modelo relacional de la tabla usuarios
│   └── requirements.txt  # Dependencias y librerías de Python
├── prometheus/
│   └── prometheus.yml    # Configuración del scrapeo hacia la API
├── docker-compose.yml    # Orquestación de contenedores y redes
└── README.md             # Documentación del proyecto