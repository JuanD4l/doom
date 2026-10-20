# CYBER-DOOM 2099 // ARQUITECTURA DESACOPLADA (WEB + REST API)

> Videojuego retro-futurista 2.5D de disparos en primera persona (*Raycaster FPS*) con estética Cyberpunk Neón y sistema de telemetría analítica en tiempo real.
> El proyecto está desacoplado en dos capas independientes:
> - **Backend en Python (FastAPI / SQLite):** Lógica del servidor, procesamiento de métricas, validación y persistencia de puntuaciones (desplegable en **Render** como *Web Service*).
> - **Frontend en JavaScript, HTML5 y CSS3:** Renderizado 3D por raycasting en `<canvas>`, sintetizador de sonido procedural con *Web Audio API*, controles de puntería con *Pointer Lock API* y gráficos analíticos interactivos con **Chart.js** consumiendo la API mediante peticiones HTTP en formato JSON (desplegable en **Render** como *Static Site* o en **GitHub Pages**).

---

## 🏛️ 1. Estructura del Repositorio

El proyecto ha sido reorganizado separando de forma estricta las responsabilidades de Frontend y Backend:

```text
666/
├── backend/                       # SERVIDOR Y LÓGICA DE DATOS (PYTHON)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py             # Configuración y variables de entorno
│   │   ├── database.py           # Conexión SQLite con auto-inicialización y seed data
│   │   ├── main.py               # Servidor FastAPI / Fallback nativo con CORS y endpoints
│   │   └── schemas.py            # Esquemas de validación Pydantic
│   ├── Procfile                  # Comando de ejecución para Render / PaaS
│   ├── render.yaml               # Configuración individual de servicio backend
│   └── requirements.txt          # Dependencias (FastAPI, Uvicorn, Pydantic, etc.)
│
├── frontend/                      # CLIENTE WEB Y GRÁFICOS (HTML / JS / CSS)
│   ├── assets/                   # Sprites optimizados de enemigos (PNG)
│   ├── css/
│   │   └── style.css             # Estilos Cyberpunk Neón, HUD, Overlays y Modales
│   ├── js/
│   │   ├── audio.js              # Síntesis procedural de audio (Web Audio API)
│   │   ├── charts.js             # Gráficos de telemetría y analítica (Chart.js)
│   │   ├── config.js             # Detección dinámica y configuración de BACKEND_URL
│   │   ├── entities.js           # Entidades (Jugador, Proyectiles, Enemigos, Partículas)
│   │   ├── game.js               # Bucle principal, control de eventos y estados
│   │   ├── hud.js                # Dibujado del HUD estilo DOOM y Minimapa Radar
│   │   ├── map.js                # Matriz espacial del nivel
│   │   ├── raycaster.js          # Motor matemático de proyección DDA y Z-Buffer
│   │   └── textures.js           # Texturas procedurales en memoria
│   └── index.html                # Interfaz principal, canvas y CDN de Chart.js
│
├── legacy_desktop/               # CÓDIGO ARCHIVADO (Antigua versión de escritorio en Pygame)
├── render.yaml                   # BLUEPRINT GENERAL DE RENDER (Despliega Backend + Frontend)
└── README.md                     # Documentación técnica integral
```

---

## 🔍 2. Identificación de Componentes y Migración

| Componente Original (Python) | Rol Arquitectónico | Reemplazo en Nueva Arquitectura | Estado |
| :--- | :--- | :--- | :--- |
| `src/graphics/` & `src/engine/` (Pygame Surface / Raycaster) | **Frontend / Gráficos** | `<canvas>` de HTML5 + `raycaster.js` + `textures.js` en JavaScript nativo ejecutado en el navegador del cliente. | ✅ Migrado a JavaScript |
| Gráficos de Estadísticas y Visualización de Datos | **Frontend / Visualización** | **Chart.js** (`charts.js`) que consume `/api/analytics` y `/api/stats` vía peticiones `fetch()` en formato JSON. | ✅ Integrado con Chart.js |
| `src/audio/synthesizer.py` (NumPy / Pygame Mixer) | **Frontend / Audio** | **Web Audio API** (`audio.js`) sintetizando ondas sinusoidales, modulación FM y envolventes ADSR en tiempo real. | ✅ Migrado a JavaScript |
| `src/ui/hud.py` & Pantallas | **Frontend / Interfaz** | Consola Canvas 2D + DOM HTML5/CSS3 con tipografía futurista (*Orbitron*). | ✅ Migrado a HTML/CSS/JS |
| `cyberdoom_save.json` / Persistencia | **Backend / Base de Datos** | Base de datos SQLite (`cyberdoom.db`) gestionada por Python en el servidor. | ✅ Centralizado en Backend |
| Lógica de Rankings y Métricas Globales | **Backend / Lógica** | API REST en Python con FastAPI (`backend/app/main.py`) y endpoints estructurados. | ✅ Exclusivo en Python |

---

## 📌 3. Supuestos de la Arquitectura y los Datos

1. **Gráficos de Renderizado 3D vs. Gráficos Estadísticos:**
   - **Renderizado 3D del Juego:** Se trasladó completamente a la API 2D del Canvas de HTML5 mediante el algoritmo DDA (Raycasting) en JavaScript. De esta manera, el navegador del usuario se encarga de todo el dibujo a 60 FPS sin cargar el servidor con transmisión de frames o dependencias como Pygame.
   - **Visualización de Datos con Chart.js:** Para sustituir bibliotecas de gráficos de Python (como *matplotlib* o *plotly*), se incorporó **Chart.js**. El backend entrega exclusivamente datos crudos en JSON mediante el endpoint `/api/analytics`, y el frontend genera gráficos de barras (Top 10 Puntajes) y gráficos de líneas/área (Relación Bajas vs. Oleadas alcanzadas).
2. **Persistencia en el Nivel Gratuito de Render:**
   - Por defecto, el backend utiliza SQLite (`backend/cyberdoom.db`). En el plan gratuito (*Free Tier*) de Render, el disco del servicio web es efímero (se restablece si la instancia entra en reposo o tras un nuevo despliegue). El código incluye un auto-seeder en [database.py](file:///c:/Users/LEMUS/OneDrive/Desktop/ADSO/Montesinos/666/backend/app/database.py) para que siempre existan registros iniciales representativos en los gráficos. Si se requiere persistencia permanente sin reinicios, basta con conectar una base de datos PostgreSQL mediante la variable de entorno `DATABASE_URL`.
3. **Manejo Offline / Fallback Resiliente:**
   - Si el backend en Render tarda unos segundos en despertar (*spin-up* del Free Tier) o está fuera de línea, el cliente web guarda el puntaje en el `localStorage` del navegador y los gráficos muestran datos de respaldo para no interrumpir la experiencia de juego.

---

## 📡 4. Endpoints de la API REST (Backend Python)

| Método | Endpoint | Descripción | Respuesta |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Verificación de disponibilidad del servicio para Render. | `{"success": true, "status": "healthy"}` |
| `GET` | `/api/leaderboard` | Top 10 mejores registros de combate. | `{"success": true, "data": [...]}` |
| `POST` | `/api/scores` | Registra una nueva partida (`player_name`, `score`, `wave`, `kills`). | `{"success": true, "data": {"id": ...}}` |
| `GET` | `/api/stats` | Métricas agregadas (total partidas, total bajas, récord). | `{"success": true, "data": {...}}` |
| `GET` | `/api/analytics` | Datos tabulados listos para visualización en **Chart.js** (labels, series numéricas y promedios). | `{"success": true, "data": {"labels": [...], "scores": [...], ...}}` |

---

## 💻 5. Cómo Ejecutar en Local

### Paso 1: Iniciar el Servidor Backend (Python)

Abre una terminal (PowerShell o Bash) en la raíz del proyecto:

```powershell
# 1. (Opcional) Instalar dependencias si vas a usar FastAPI
pip install -r backend/requirements.txt

# 2. Iniciar el servidor API (puerto 8000 por defecto)
python backend/app/main.py
```
> *Nota:* El servidor cuenta con un modo dual inteligente: si no tienes instalado FastAPI/Uvicorn, arranca automáticamente un servidor nativo HTTP con SQLite para pruebas locales inmediatas.

Puedes verificar el backend abriendo en tu navegador:
`http://localhost:8000/api/health`

### Paso 2: Iniciar el Cliente Frontend (JavaScript / HTML)

En otra terminal separada, inicia un servidor estático para la carpeta `frontend/`:

```powershell
python -m http.server 8080 --directory frontend
```

Abre tu navegador en:
👉 **`http://localhost:8080`**

Al ingresar, el cliente web detectará automáticamente `http://localhost:8000` como servidor backend y verás el indicador en verde: `● Servidor Conectado`.

---

## ☁️ 6. Guía de Despliegue en Render

Tienes dos formas de desplegar el proyecto en Render:

### Opción A: Despliegue Automático con Blueprint (`render.yaml`) (Recomendado)

1. Sube este repositorio a tu cuenta de **GitHub**.
2. Ingresa a [dashboard.render.com](https://dashboard.render.com/).
3. Haz clic en **New +** > selecciona **Blueprint**.
4. Conecta tu repositorio de GitHub.
5. Render leerá automáticamente el archivo [render.yaml](file:///c:/Users/LEMUS/OneDrive/Desktop/ADSO/Montesinos/666/render.yaml) ubicado en la raíz y creará simultáneamente:
   - **`cyberdoom-api`**: Servicio Web Python para el Backend.
   - **`cyberdoom-frontend`**: Sitio Estático para el Frontend.
6. Haz clic en **Apply**.

---

### Opción B: Despliegue Manual (Paso a Paso)

#### 1. Desplegar el Backend (Python Web Service)
1. En Render, haz clic en **New +** > **Web Service**.
2. Conecta el repositorio de GitHub.
3. Completa los siguientes parámetros:
   - **Name:** `cyberdoom-api`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
4. Haz clic en **Create Web Service**.
5. Al finalizar el despliegue, copia la URL que te asigna Render, por ejemplo:
   `https://cyberdoom-api.onrender.com`

#### 2. Desplegar el Frontend (Static Site)
1. En Render, haz clic en **New +** > **Static Site**.
2. Conecta el mismo repositorio de GitHub.
3. Completa los parámetros:
   - **Name:** `cyberdoom-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** *(dejar en blanco)*
   - **Publish Directory:** `./`
4. Haz clic en **Create Static Site**.

---

## 🔗 7. Conexión entre Frontend y Backend en Producción

El cliente web incluye detección inteligente y configurable de la URL del backend mediante [frontend/js/config.js](file:///c:/Users/LEMUS/OneDrive/Desktop/ADSO/Montesinos/666/frontend/js/config.js):

1. **Mediante parámetro URL (Sin modificar código):**
   Puedes abrir tu frontend en Render o GitHub Pages agregando el parámetro `?api=`:
   `https://tu-frontend.onrender.com/?api=https://tu-api.onrender.com`
   *(El frontend guardará automáticamente la URL en `localStorage` para futuras sesiones).*

2. **Edición directa de configuración:**
   En el archivo [frontend/js/config.js](file:///c:/Users/LEMUS/OneDrive/Desktop/ADSO/Montesinos/666/frontend/js/config.js), actualiza la URL por defecto con la tuya:
   ```javascript
   : "https://tu-api-render.onrender.com";
   ```

---

## 🎮 Controles de Combate en el Navegador

| Acción | Control |
| :--- | :--- |
| **Giro y Puntería (*Mouse-Look*)** | Mover el Ratón (Activa *Pointer Lock*) |
| **Disparar Cyber-Shotgun** | **Click Izquierdo** del Ratón o **Barra Espaciadora** |
| **Desplazamiento** | Teclas `W`, `A`, `S`, `D` |
| **Sprint / Acelerar** | Tecla `Shift Izquierdo` |
| **Pausar / Liberar Puntero** | Tecla `Escape` |
| **Ver Telemetría / Gráficos** | Botón **📊 VER TELEMETRÍA Y GRÁFICOS (CHART.JS)** |
