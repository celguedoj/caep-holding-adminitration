# CAEP Holding Administration

Este proyecto es una API para la gestion y administracion de una holding. Una
holding es una organizacion que agrupa y controla varias empresas; se puede
entender como una estructura parecida a una franquicia o grupo empresarial,
donde existen companias relacionadas, y cada una puede tener sus propios
departamentos, empleados y productos.

La API fue construida por Carlos Elguedo como parte de la prueba tecnica de
RSG. La idea principal es ofrecer una base clara, sencilla y mantenible para
administrar la informacion principal de una holding usando Python, FastAPI,
PostgreSQL, Docker y autenticacion con JWT.

## Indice

- [Descripcion del proyecto](#descripcion-del-proyecto)
- [Tecnologias usadas](#tecnologias-usadas)
- [Arquitectura](#arquitectura)
- [Ejecucion con Docker](#ejecucion-con-docker)
- [Base de datos](#base-de-datos)
- [Autenticacion](#autenticacion)
- [Probar con Postman](#probar-con-postman)
- [Endpoints](#endpoints)
- [Pruebas](#pruebas)

## Descripcion del proyecto

El sistema permite administrar los recursos principales de una holding:

- Companias: empresas que pertenecen al grupo.
- Departamentos: areas internas asociadas a una compania.
- Empleados: personas que trabajan dentro de una compania y, opcionalmente, en
  un departamento.
- Productos: productos o servicios asociados a una compania.

Existe un endpoint publico para consultar las companias de la holding. El resto
de operaciones de creacion, edicion, eliminacion y consulta privada requieren
autenticacion mediante JWT.

## Tecnologias usadas

- Python 3.11
- FastAPI
- Pydantic
- SQLAlchemy async
- PostgreSQL
- Docker y Docker Compose
- JWT con `python-jose`
- Uvicorn

## Arquitectura

El proyecto esta organizado siguiendo una idea simple de Clean Architecture:

- `domain`: reglas y entidades del negocio, sin depender de FastAPI ni base de
  datos.
- `infrastructure`: configuracion y acceso a recursos externos, como
  PostgreSQL.
- `presentation`: routers, schemas y endpoints HTTP.
- `core`: configuracion general y seguridad.

La intencion es separar la logica del dominio de los detalles tecnicos, para que
el proyecto sea mas facil de mantener y extender.

## Ejecucion con Docker

1. Crea el archivo de entorno:

```bash
cp .env.example .env
```

En Windows PowerShell tambien puedes usar:

```powershell
Copy-Item .env.example .env
```

2. Levanta la API y la base de datos:

```bash
docker compose up --build
```

3. Verifica que la API este funcionando:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/db
```

La documentacion interactiva de FastAPI queda disponible en:

```text
http://localhost:8000/docs
```

Para levantar solo PostgreSQL:

```bash
docker compose up -d db
```

Para apagar los servicios:

```bash
docker compose down
```

## Base de datos

PostgreSQL se ejecuta en Docker. La configuracion por defecto es:

- Host local: `localhost`
- Host desde Docker: `db`
- Puerto: `5432`
- Base de datos: `caep_holding`
- Usuario: `caep`
- Password: `caep`

La API crea las tablas automaticamente al iniciar. Para esta prueba tecnica se
evito agregar migraciones para mantener el proyecto sencillo y facil de probar.

## Autenticacion

El login devuelve un token JWT:

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

Credenciales por defecto:

- Usuario: `admin`
- Password: `admin123`

Luego envia el token en los endpoints privados:

```bash
curl http://localhost:8000/companies \
  -H "Authorization: Bearer <token>"
```

El endpoint publico no requiere token:

```bash
curl http://localhost:8000/public/companies
```

## Probar con Postman

El proyecto incluye una coleccion de Postman lista para importar:

```text
postman_collection.json
```

Pasos para importarla:

1. Abre Postman.
2. Haz clic en `Import`.
3. Selecciona `Files`.
4. Elige el archivo `postman_collection.json` desde la raiz del proyecto.
5. Importa la coleccion `CAEP Holding Administration API`.

La coleccion ya trae la variable `base_url` con este valor:

```text
http://localhost:8000
```

Para probar el flujo completo:

1. Ejecuta `Auth / Login`.
2. El token se guarda automaticamente en la variable `token`.
3. Ejecuta `Companies / Create Company`.
4. La coleccion guarda automaticamente `company_id`.
5. Con esa compania creada puedes probar departamentos, empleados y productos.

## Endpoints

Sistema:

- `GET /health`
- `GET /health/db`

Autenticacion:

- `POST /auth/token`

Publico:

- `GET /public/companies`

Companias:

- `GET /companies`
- `POST /companies`
- `GET /companies/{id}`
- `PATCH /companies/{id}`
- `DELETE /companies/{id}`
- `GET /companies/{id}/departments`
- `GET /companies/{id}/employees`
- `GET /companies/{id}/products`

Departamentos:

- `GET /departments`
- `POST /departments`
- `GET /departments/{id}`
- `PATCH /departments/{id}`
- `DELETE /departments/{id}`

Empleados:

- `GET /employees`
- `POST /employees`
- `GET /employees/{id}`
- `PATCH /employees/{id}`
- `DELETE /employees/{id}`

Productos:

- `GET /products`
- `POST /products`
- `GET /products/{id}`
- `PATCH /products/{id}`
- `DELETE /products/{id}`

## Pruebas

Para ejecutar las pruebas unitarias disponibles:

```bash
python -m unittest discover -s tests
```
