# CYBER-DOOM 2099 // ARQUITECTURA POR CAPAS (LAYERED ARCHITECTURE)

> Proyecto desarrollado bajo la metodología de **Arquitectura Limpia**, **Cero Mocks** y **Desarrollo Modular** (adaptación de `skill_arquitecto_de_software_pro.md` y `plantilla_de_fases_general.md`).

---

## 🏛️ Estructura y Distribución en Capas

El proyecto ha sido completamente desacoplado y organizado en **7 capas de arquitectura de software**:

```text
666/
├── main.py                          # Punto de entrada principal
├── doom_cyberpunk.py                # Acceso directo modular compatible
├── README_CYBERDOOM.md              # Documentación técnica
└── src/
    ├── config/                      # 1. CAPA DE CONFIGURACIÓN Y CONSTANTES
    │   ├── __init__.py
    │   └── settings.py              # Resolución, constantes de raycasting, paleta neón
    │
    ├── audio/                       # 2. CAPA DE INFRAESTRUCTURA DE AUDIO
    │   ├── __init__.py
    │   └── synthesizer.py           # Síntesis matemática de audio 16-bit PCM en memoria
    │
    ├── graphics/                    # 3. CAPA DE INFRAESTRUCTURA GRÁFICA
    │   ├── __init__.py
    │   ├── textures.py              # Texturas de muros 64x64 y tablas LUT de sombreado
    │   └── sprites.py               # Rig de arma en 1ra persona y sprites 3D de enemigos
    │
    ├── domain/                      # 4. CAPA DE DOMINIO Y ENTIDADES
    │   ├── __init__.py
    │   ├── player.py                # Entidad Jugador, colisión, salud, escudo y Mouse-Look
    │   ├── enemy.py                 # Entidad Enemigo con IA táctica y Raycast LOS
    │   ├── projectile.py            # Entidad Proyectil de plasma
    │   └── particle.py              # Entidad Partícula y chispas neón
    │
    ├── engine/                      # 5. CAPA DE MOTOR 3D Y MUNDO
    │   ├── __init__.py
    │   ├── map.py                   # Matriz espacial del nivel y detección de muros
    │   └── raycaster.py             # Algoritmo DDA, mapeo de texturas y Z-Buffer
    │
    ├── ui/                          # 6. CAPA DE PRESENTACIÓN E INTERFAZ
    │   ├── __init__.py
    │   ├── hud.py                   # Consola DOOM inferior, avatar reactivo y minimapa radar
    │   └── screens.py               # Pantalla de inicio, menú de pausa y Game Over
    │
    └── core/                        # 7. CAPA DE APLICACIÓN Y ORQUESTACIÓN
        ├── __init__.py
        └── game_manager.py          # Bucle principal, máquina de estados y persistencia
```

---

## 📦 Detalle de Responsabilidad de Cada Capa

### 1. Capa de Configuración (`src/config/`)
- **`settings.py`**: Centraliza todas las constantes del sistema para evitar números mágicos: dimensiones (`SCREEN_WIDTH = 960`, `SCREEN_HEIGHT = 680`, `VIEWPORT_HEIGHT = 550`), parámetros de raycasting (`FOV = 60°`, `NUM_RAYS = 240`), paleta cromática cyber-neón y rutas de persistencia.

### 2. Capa de Audio (`src/audio/`)
- **`synthesizer.py`**: Aísla el subsistema de sonido. Genera proceduralmente las ondas sinusoidales, ruidos filtrados y envolventes ADSR para escopeta, impactos, disparos láser, alarmas de oleada y daño sin requerir archivos `.wav` externos.

### 3. Capa Gráfica (`src/graphics/`)
- **`textures.py`**: Genera proceduralmente las 4 texturas de 64x64 de los muros y precalcula matrices de brillo LUT para optimizar el sombreado a más de 800 FPS.
- **`sprites.py`**: Genera las superficies del arma en primera persona con retroceso y fogonazo (*muzzle flash*), los 3 tipos de enemigos y los proyectiles.

### 4. Capa de Dominio (`src/domain/`)
- **`player.py`**: Modela el estado del jugador, consumo de energía/escudo, física de colisión elástica en dos ejes y cálculo de ángulo por *Mouse-Look*.
- **`enemy.py`**: Modela la máquina de estados de los enemigos (`Drone`, `Imp`, `Baron`), comprobación de línea de visión directa (*Raycast LOS*) y comportamiento de disparo.
- **`projectile.py`** y **`particle.py`**: Controlan la trayectoria, tiempo de vida y colisión de proyectiles y chispas.

### 5. Capa de Motor 3D (`src/engine/`)
- **`map.py`**: Almacena la matriz bidimensional del nivel y las funciones de consulta espacial.
- **`raycaster.py`**: Implementa el algoritmo DDA, la corrección de distorsión ojo de pez, el renderizado vertical de texturas con distancia y la proyección de billboards contra el *Z-Buffer*.

### 6. Capa de Presentación (`src/ui/`)
- **`hud.py`**: Dibuja la consola inferior clásica estilo DOOM con el rostro del Cyber-Marine que reacciona al daño/disparo, los indicadores de barras de energía y el minimapa radar en tiempo real.
- **`screens.py`**: Gestiona las pantallas de presentación (Título, Pausa con liberación de cursor y Game Over con récord).

### 7. Capa de Aplicación (`src/core/`)
- **`game_manager.py`**: Inyecta las dependencias de todas las capas, controla el Game Loop a 60 FPS, procesa eventos de entrada, administra las oleadas dinámicas y persiste la puntuación en disco (`cyberdoom_save.json`).

---

## 🎮 Controles del Juego

| Acción | Control |
| :--- | :--- |
| **Mirar y Apuntar (*Mouse-Look*)** | **Mover el Ratón** |
| **Disparar Cyber-Shotgun** | **Click Izquierdo** del Ratón o **Barra Espaciadora** |
| **Moverse Adelante / Atrás** | `W` / `S` |
| **Desplazamiento Lateral (*Strafe*)** | `A` / `D` |
| **Sprint / Correr** | `Shift Izquierdo` |
| **Pausar / Liberar Ratón** | `Escape` |
| **Reiniciar Partida** | `R`, `Espacio` o **Click** |

---

## 🚀 Cómo Ejecutar

Puedes ejecutar el juego a través de cualquiera de los dos puntos de entrada:

```powershell
# Opción 1 (Punto de entrada oficial por capas):
python main.py

# Opción 2 (Acceso directo compatible):
python doom_cyberpunk.py
```
