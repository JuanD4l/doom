"""
================================================================================
CAPA DE CONFIGURACIÓN Y CONSTANTES (Config Layer)
================================================================================
Define las propiedades globales del juego, resolución, constantes físicas,
parámetros del motor de raycasting, paleta de colores neón y rutas de guardado.
================================================================================
"""

import os
import math

# Dimensiones de la Ventana y Viewport
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 680
VIEWPORT_HEIGHT = 550
HUD_HEIGHT = SCREEN_HEIGHT - VIEWPORT_HEIGHT
FPS = 60

# Parámetros del Motor de Raycasting 2.5D
FOV = math.pi / 3           # 60 grados de campo de visión
NUM_RAYS = 240              # Rayos horizontales proyectados
RAY_WIDTH = SCREEN_WIDTH / NUM_RAYS
MAX_DEPTH = 20.0            # Alcance máximo de visión en celdas
HALF_FOV = FOV / 2.0
DIST_PROJ = (SCREEN_WIDTH / 2.0) / math.tan(HALF_FOV)
TEX_SIZE = 64               # Resolución de las texturas de muros (64x64)

# Paleta Cromática Cyberpunk Neón
COLOR_ABYSS = (5, 6, 12)
COLOR_CEILING = (14, 8, 26)
COLOR_FLOOR = (10, 14, 24)

NEON_CYAN = (0, 243, 255)
NEON_MAGENTA = (255, 0, 127)
NEON_PURPLE = (157, 78, 221)
NEON_GREEN = (57, 255, 20)
NEON_YELLOW = (255, 214, 10)
NEON_ORANGE = (255, 120, 0)
NEON_RED = (255, 30, 60)
DARK_METAL = (24, 28, 38)
LIGHT_STEEL = (170, 185, 205)
WHITE = (245, 245, 255)

# Archivo de persistencia de récord
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAVE_FILE = os.path.join(BASE_DIR, "cyberdoom_save.json")
