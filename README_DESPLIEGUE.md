# GUÍA DE DESPLIEGUE GRATUITO // CYBER-DOOM 2099

Esta guía detalla cómo probar el juego inmediatamente en tu navegador y cómo desplegar el **Frontend en GitHub Pages** y el **Backend en Render** de forma **100% gratuita**.

---

## 🚀 1. PROBAR EN EL NAVEGADOR AHORA MISMO (Local)

El servidor web local ya se encuentra activo en tu máquina. Solo debes abrir tu navegador favorito (Chrome, Edge, Firefox, Brave):

👉 **Abre la URL:** `http://localhost:8080`

### Si necesitas reiniciar el servidor en cualquier momento:
```powershell
# Desde la carpeta 666:
python -m http.server 8080 --directory frontend
```

### Para iniciar la API Backend local (Opcional):
```powershell
# En otra terminal:
python backend/app/main.py
```

---

## 🌐 2. DESPLIEGUE DEL FRONTEND EN GITHUB PAGES (100% GRATIS)

GitHub Pages permite alojar aplicaciones estáticas (HTML5, Canvas, JavaScript, Web Audio) sin límite de tiempo y sin costo.

### Pasos:
1. **Crear Repositorio en GitHub:**
   - Ve a [github.com/new](https://github.com/new).
   - Nómbralo por ejemplo `cyberdoom-2099` (debe ser Público para GitHub Pages gratuito).
2. **Subir los Archivos del Frontend:**
   - Sube el contenido de la carpeta `frontend/` (es decir, `index.html`, la carpeta `css/` y la carpeta `js/`) directamente en la rama principal (`main`).
   ```bash
   cd frontend
   git init
   git add .
   git commit -m "feat: Cyber-Doom 2099 Web FPS"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/cyberdoom-2099.git
   git push -u origin main
   ```
3. **Activar GitHub Pages:**
   - En tu repositorio de GitHub, ve a **Settings** (Configuración) > pestaña **Pages** (en el menú lateral izquierdo).
   - En **Build and deployment > Source**, selecciona `Deploy from a branch`.
   - En **Branch**, selecciona `main` y la carpeta `/ (root)`. Haz clic en **Save**.
4. **¡Listo!**
   - En 1-2 minutos tu juego estará publicado en:
     `https://TU_USUARIO.github.io/cyberdoom-2099/`

---

## ⚙️ 3. DESPLIEGUE DEL BACKEND EN RENDER (100% GRATIS)

Render ofrece un nivel gratuito (*Free Tier*) de Web Services en la nube perfecto para APIs en Python.

### Pasos:
1. **Subir la Carpeta `backend/` a GitHub:**
   - Crea un repositorio nuevo en GitHub llamado `cyberdoom-backend`.
   - Sube los archivos de la carpeta `backend/` (`Procfile`, `requirements.txt`, `render.yaml`, carpeta `app/`):
   ```bash
   cd backend
   git init
   git add .
   git commit -m "feat: Cyber-Doom REST API"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/cyberdoom-backend.git
   git push -u origin main
   ```
2. **Crear el Servicio en Render.com:**
   - Ve a [render.com](https://render.com) e inicia sesión con tu cuenta de GitHub.
   - Haz clic en **New +** > selecciona **Web Service**.
   - Conecta tu repositorio `cyberdoom-backend`.
   - Configuración:
     - **Name:** `cyberdoom-api`
     - **Runtime:** `Python 3`
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Plan Type:** Selecciona **Free** ($0 / month).
   - Haz clic en **Create Web Service**.
3. **Copiar tu URL Pública de Render:**
   - Al terminar de compilar, Render te dará una URL HTTPS pública, por ejemplo:
     `https://cyberdoom-api.onrender.com`

---

## 🔗 4. CONECTAR FRONTEND Y BACKEND

Una vez que tengas tu URL de Render:
1. Abre el archivo `frontend/js/config.js`.
2. Actualiza la variable `BACKEND_URL`:
   ```javascript
   BACKEND_URL: "https://cyberdoom-api.onrender.com"
   ```
3. Haz un commit y push a GitHub Pages:
   ```bash
   git add js/config.js
   git commit -m "chore: connect frontend to Render backend"
   git push
   ```

A partir de ese momento, tu juego en GitHub Pages guardará y cargará las puntuaciones globales directamente desde tu API gratuita en Render con base de datos SQLite persistente.
