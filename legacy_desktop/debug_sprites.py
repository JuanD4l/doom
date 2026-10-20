"""
Script de diagnóstico: simula el cálculo de proyección de sprites
para detectar por qué los enemigos no se ven.
"""
import math

SCREEN_WIDTH = 960
VIEWPORT_HEIGHT = 550
FOV = math.pi / 3
NUM_RAYS = 240
RAY_WIDTH = SCREEN_WIDTH / NUM_RAYS
MAX_DEPTH = 20.0
HALF_FOV = FOV / 2.0
DIST_PROJ = (SCREEN_WIDTH / 2.0) / math.tan(HALF_FOV)

print(f"DIST_PROJ = {DIST_PROJ:.2f}")
print(f"RAY_WIDTH = {RAY_WIDTH:.2f}")
print()

# Simular jugador en (2.5, 2.5) mirando al este (angle=0)
# Enemigo drone en (6.5, 2.5) -> directamente enfrente
player_x, player_y, player_angle = 2.5, 2.5, 0.0
enemies = [
    ("drone",  6.5, 2.5),
    ("imp",    8.0, 3.5),
    ("imp",    5.5, 5.0),
    ("baron", 10.0, 4.5),
]

for etype, ex, ey in enemies:
    dx = ex - player_x
    dy = ey - player_y
    dist = math.hypot(dx, dy)

    inv_cos = math.cos(-player_angle)
    inv_sin = math.sin(-player_angle)
    trans_x = dx * inv_cos - dy * inv_sin   # profundidad
    trans_y = dx * inv_sin + dy * inv_cos   # lateral

    if trans_x <= 0.15:
        print(f"[{etype}] SKIP: trans_x={trans_x:.3f} (detrás del jugador)")
        continue

    screen_x = int((SCREEN_WIDTH / 2.0) + (trans_y / trans_x) * DIST_PROJ)
    scale = min(4.5, (1.0 / trans_x) * DIST_PROJ)
    factor = 1.15 if etype == "baron" else 0.85
    target_w = int(scale * factor)
    target_h = int(scale * factor)
    draw_y = int(VIEWPORT_HEIGHT / 2.0)

    top = draw_y - target_h // 2
    left = screen_x - target_w // 2

    print(f"[{etype}] dist={dist:.2f}  trans_x={trans_x:.2f}  scale={scale:.1f}")
    print(f"         target={target_w}x{target_h}  screen_x={screen_x}  top={top}  left={left}")
    visible = (target_w > 0 and target_h > 0 and
               0 <= screen_x <= SCREEN_WIDTH and top < VIEWPORT_HEIGHT)
    print(f"         -> {'✓ VISIBLE' if visible else '✗ NO VISIBLE'}")
    print()
