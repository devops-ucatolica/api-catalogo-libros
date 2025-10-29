

````markdown
# 📚 API Catálogo de Libros — FastAPI + Azure App Service + GitHub Actions

**Ejercicio del Punto 11 del Manual de Buenas Prácticas DevOps para Entornos Académicos en Azure Student y GitHub (ISO/IEC/IEEE 29119).**  
Este proyecto implementa una **API REST** en **FastAPI**, desplegada automáticamente en **Azure App Service (Linux)** mediante **GitHub Actions (CI/CD)**, siguiendo las prácticas de seguridad, monitoreo y control de versiones propuestas en el manual.

---

## 🧠 Objetivo general

Aplicar los principios del **Capítulo 11: Casos prácticos de CI/CD, Seguridad y Monitoreo**, desarrollando un entorno DevOps académico funcional que integre:
- Desarrollo con **FastAPI**.
- Despliegue automático en **Azure App Service**.
- Pruebas unitarias y validación continua (**CI**).
- Despliegue continuo (**CD**).
- Verificación de salud (**Health Check**) y monitoreo activo.
- Manejo seguro de secretos (**GitHub Secrets / Azure Key Vault**).

---

## ⚙️ Arquitectura DevOps aplicada

```text
Desarrollador → Commit / Push (branch: develop)
     ↓
GitHub Actions (CI: pruebas + linting + build)
     ↓
Pull Request → merge a main
     ↓
GitHub Actions (CD: Deploy a Azure App Service)
     ↓
Azure App Service (Linux) + Application Insights (monitoring)
````

Cada componente sigue los lineamientos de la norma **ISO/IEC/IEEE 29119**, enfocándose en la trazabilidad de versiones, automatización de despliegues y aseguramiento de la calidad.

---

## 🗂️ Estructura del proyecto

```
api-libros-demo/
│
├── app/
│   └── main.py              # Punto de entrada de la API
│
├── tests/
│   └── test_main.py         # Prueba unitaria mínima
│
├── requirements.txt         # Dependencias Python
├── startup.sh               # Script de inicio (Gunicorn + Uvicorn)
├── .github/
│   └── workflows/
│       ├── ci.yml           # Integración continua (lint + pytest)
│       ├── cd-azure.yml     # Despliegue continuo (Azure Web App)
│       └── healthcheck.yml  # Verificación horaria de /health
└── README.md
```

---

## ▶️ Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate      # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Endpoints:**

* Base: `http://127.0.0.1:8000`
* Swagger UI: `http://127.0.0.1:8000/docs`
* Health: `http://127.0.0.1:8000/health`

---

## 🚀 Despliegue en Azure App Service

### 1️⃣ Configuración inicial

1. Crear un **App Service (Linux)** en Azure Portal.
2. Descargar el **Publish Profile (.PublishSettings)**.
3. En el repositorio GitHub, ir a **Settings → Secrets → Actions** y agregar:

   ```
   AZURE_WEBAPP_PUBLISH_PROFILE = <contenido XML del Publish Profile>
   ```

### 2️⃣ Pipeline de CD (`.github/workflows/cd-azure.yml`)

El pipeline empaqueta el código, instala dependencias y publica el artefacto en Azure mediante **Zip Deploy**:

```yaml
env:
  AZURE_WEBAPP_NAME: api-libros-demo
  PYTHON_VERSION: "3.10"
```

Azure usará el `startup.sh` para iniciar el servicio:

```bash
#!/usr/bin/env bash
export PORT=${PORT:-8000}
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT app.main:app
```

En el portal de Azure → App Service → Configuración general, establecer:

```
Startup Command: bash startup.sh
```

### 3️⃣ Despliegue automático

Cada **push o merge a `main`** activa el flujo de despliegue:

* Instala dependencias.
* Crea paquete `deploy_package`.
* Despliega automáticamente usando el secreto seguro `AZURE_WEBAPP_PUBLISH_PROFILE`.

---

## 🔐 Seguridad y manejo de secretos

De acuerdo con el **Capítulo 9 del manual**, la gestión segura de credenciales es esencial:

* Nunca subir el archivo `.PublishSettings` al repositorio.
* Usar **GitHub Secrets** para CI/CD.
* Para entornos productivos, implementar **Azure Key Vault** con rotación automática de claves.
* Habilitar escaneo de seguridad estático (SAST) y dinámico (DAST) con CodeQL y ZAP Baseline.

> Esta práctica cumple con los principios de **DevSecOps académico**, integrando seguridad en todas las fases del ciclo de vida del software.

---

## ❤️ Health Check y monitoreo

El workflow `healthcheck.yml` realiza una verificación horaria de disponibilidad:

```bash
curl -s -o /dev/null -w "%{http_code}" https://api-libros-demo-<id>.chilecentral-01.azurewebsites.net/health
```

* Si devuelve código distinto de 200 → falla el job.
* Permite medir disponibilidad y detectar caídas tempranas.
* Puede integrarse con **Application Insights** para métricas extendidas.

---

## 🧪 Pruebas automáticas (CI)

Archivo: `.github/workflows/ci.yml`

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - run: pip install -r requirements.txt
      - run: pytest -v
```

Las pruebas aseguran estabilidad antes del despliegue (principio **Shift-Left Testing** del manual).

---

## ✅ Checklist de validación (Punto 11)

* [x] Repositorio en GitHub (`develop` + `main`)
* [x] CI/CD implementado (`ci.yml`, `cd-azure.yml`)
* [x] Despliegue funcional en Azure App Service (Linux)
* [x] Secretos gestionados correctamente (GitHub Secrets / Key Vault)
* [x] Health-check operativo
* [x] Documentación conforme al Manual DevOps (Punto 11)

---

## 🧾 Referencias bibliográficas (Manual DevOps)

* **Capítulo 11:** Casos prácticos de CI/CD, Seguridad y Monitoreo.
* **Capítulo 9:** Seguridad y Gestión de Secretos en Entornos DevOps.
* **Capítulo 6:** Control de versiones, testing e integración continua (ISO/IEC/IEEE 29119).
* **Capítulo 7:** Despliegue continuo en Azure y buenas prácticas con GitHub Actions.

---

**Autor:** Cristian Andrés Sierra Páez
**Universidad Católica de Colombia – Ingeniería de Sistemas**
**Proyecto académico:** DevOps y Computación en la Nube 2025
**Manual base:** *Manual de Buenas Prácticas DevOps para Entornos Académicos en Azure Student y GitHub (ISO/IEC/IEEE 29119)*

```

---

¿Quieres que le agregue los **badges de estado** (✅ build passing, ☁️ deploy success y ❤️ health ok) en la parte superior del README?  
Puedo generarte los enlaces exactos de GitHub Actions para mostrarlos dinámicamente.
```

