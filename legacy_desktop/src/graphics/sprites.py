"""
================================================================================
CAPA DE GRÁFICOS Y SPRITES (Graphics Infrastructure - Sprites)
================================================================================
Genera los sprites de armas en primera persona (Cyber-Shotgun con manos y fogonazo)
y las 5 entidades tácticas del juego (Xyron, Brutus, Nyx, Florax y Volt)
según sus fichas técnicas de diseño pixel-art con paleta neón cyberpunk.
================================================================================
"""

import os
import math
import pygame
from src.config.settings import (
    DARK_METAL, NEON_CYAN, WHITE, NEON_MAGENTA, NEON_ORANGE,
    NEON_PURPLE, NEON_RED, NEON_YELLOW
)

def create_weapon_sprites():
    """Genera los cuadros de animación del Cyber-Shotgun en 1ra persona."""
    frames = []
    w, h = 320, 260

    # Frame 0: Reposo
    s_idle = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.polygon(s_idle, (20, 24, 34), [(40, 260), (70, 190), (105, 190), (90, 260)])
    pygame.draw.polygon(s_idle, (20, 24, 34), [(280, 260), (250, 190), (215, 190), (230, 260)])
    pygame.draw.line(s_idle, NEON_CYAN, (70, 195), (105, 195), 3)
    pygame.draw.line(s_idle, NEON_CYAN, (250, 195), (215, 195), 3)
    pygame.draw.polygon(s_idle, DARK_METAL, [(115, 260), (135, 75), (185, 75), (205, 260)])
    pygame.draw.rect(s_idle, (16, 20, 30), (138, 65, 44, 180))
    pygame.draw.circle(s_idle, (40, 48, 65), (148, 68), 12)
    pygame.draw.circle(s_idle, (10, 12, 16), (148, 68), 8)
    pygame.draw.circle(s_idle, (40, 48, 65), (172, 68), 12)
    pygame.draw.circle(s_idle, (10, 12, 16), (172, 68), 8)
    pygame.draw.line(s_idle, NEON_CYAN, (136, 80), (120, 255), 4)
    pygame.draw.line(s_idle, WHITE, (136, 85), (120, 250), 2)
    pygame.draw.line(s_idle, NEON_CYAN, (184, 80), (200, 255), 4)
    pygame.draw.line(s_idle, WHITE, (184, 85), (200, 250), 2)
    pygame.draw.circle(s_idle, NEON_CYAN, (160, 140), 16)
    pygame.draw.circle(s_idle, WHITE, (160, 140), 7)
    frames.append(s_idle)

    # Frame 1: Fogonazo explosivo (Muzzle Flash)
    s_fire = pygame.Surface((w, h), pygame.SRCALPHA)
    rec = 25
    pygame.draw.polygon(s_fire, (25, 30, 45), [(40, 260), (70, 190 + rec), (105, 190 + rec), (90, 260)])
    pygame.draw.polygon(s_fire, (25, 30, 45), [(280, 260), (250, 190 + rec), (215, 190 + rec), (230, 260)])
    pygame.draw.polygon(s_fire, DARK_METAL, [(115, 260), (135, 75 + rec), (185, 75 + rec), (205, 260)])
    pygame.draw.rect(s_fire, (35, 45, 65), (138, 65 + rec, 44, 180))
    pygame.draw.circle(s_fire, NEON_CYAN, (160, 55 + rec), 65)
    pygame.draw.circle(s_fire, WHITE, (160, 55 + rec), 35)
    for deg in range(0, 360, 30):
        rad = math.radians(deg)
        x2 = 160 + math.cos(rad) * 90
        y2 = (55 + rec) + math.sin(rad) * 60
        pygame.draw.line(s_fire, NEON_MAGENTA, (160, 55 + rec), (x2, y2), 5)
        pygame.draw.line(s_fire, WHITE, (160, 55 + rec), (x2, y2), 2)
    frames.append(s_fire)

    # Frame 2: Recuperación del retroceso
    s_recoil = pygame.Surface((w, h), pygame.SRCALPHA)
    rec2 = 12
    pygame.draw.polygon(s_recoil, (20, 24, 34), [(40, 260), (70, 190 + rec2), (105, 190 + rec2), (90, 260)])
    pygame.draw.polygon(s_recoil, (20, 24, 34), [(280, 260), (250, 190 + rec2), (215, 190 + rec2), (230, 260)])
    pygame.draw.polygon(s_recoil, DARK_METAL, [(115, 260), (135, 75 + rec2), (185, 75 + rec2), (205, 260)])
    pygame.draw.rect(s_recoil, (20, 25, 35), (138, 65 + rec2, 44, 180))
    pygame.draw.circle(s_recoil, NEON_ORANGE, (148, 68 + rec2), 10)
    pygame.draw.circle(s_recoil, NEON_ORANGE, (172, 68 + rec2), 10)
    pygame.draw.circle(s_recoil, WHITE, (148, 68 + rec2), 5)
    pygame.draw.circle(s_recoil, WHITE, (172, 68 + rec2), 5)
    frames.append(s_recoil)

    return frames

def _draw_xyron(sz):
    """
    XYRON - Explorador Alienígena
    Alienígena de piel azul turquesa, cabeza grande, ojos negros brillantes,
    armadura tecnológica oscura y rifle de energía a distancia.
    """
    surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
    c_skin = (35, 210, 225)
    c_skin_shadow = (20, 150, 170)
    c_armor = (24, 30, 42)
    c_armor_edge = (60, 80, 110)

    # Aura cian sutil
    for r in range(6, 0, -2):
        alpha = 25 + r * 8
        glow = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (0, 240, 255, alpha), (45 - r, 15 - r, 166 + r*2, 220 + r*2))
        surf.blit(glow, (0, 0))

    # Piernas ágiles
    pygame.draw.line(surf, c_skin_shadow, (108, 175), (88, 246), 11)
    pygame.draw.line(surf, c_skin_shadow, (148, 175), (168, 246), 11)
    pygame.draw.ellipse(surf, c_armor, (78, 238, 24, 12))
    pygame.draw.ellipse(surf, c_armor, (158, 238, 24, 12))

    # Torso y Armadura oscura
    pygame.draw.ellipse(surf, c_skin, (96, 105, 64, 75))
    pygame.draw.polygon(surf, c_armor, [(92, 110), (164, 110), (154, 165), (102, 165)])
    pygame.draw.polygon(surf, c_armor_edge, [(92, 110), (164, 110), (154, 165), (102, 165)], 2)
    pygame.draw.circle(surf, NEON_CYAN, (128, 135), 8)
    pygame.draw.circle(surf, WHITE, (128, 135), 4)

    # Cuello
    pygame.draw.rect(surf, c_skin, (116, 75, 24, 32))

    # Cabeza grande alienígena
    pygame.draw.ellipse(surf, c_skin, (50, 15, 156, 78))
    pygame.draw.ellipse(surf, c_skin_shadow, (50, 15, 156, 78), 3)

    # Ojos negros gigantes brillantes
    pygame.draw.ellipse(surf, (10, 12, 18), (68, 38, 38, 30))
    pygame.draw.ellipse(surf, (10, 12, 18), (150, 38, 38, 30))
    pygame.draw.circle(surf, WHITE, (78, 46), 6)
    pygame.draw.circle(surf, WHITE, (160, 46), 6)
    pygame.draw.circle(surf, NEON_CYAN, (84, 52), 3)
    pygame.draw.circle(surf, NEON_CYAN, (166, 52), 3)

    # Rifle tecnológico
    pygame.draw.rect(surf, (15, 18, 25), (40, 140, 130, 22), border_radius=4)
    pygame.draw.line(surf, NEON_CYAN, (45, 151), (165, 151), 3)
    pygame.draw.circle(surf, NEON_CYAN, (38, 151), 7)
    pygame.draw.circle(surf, WHITE, (38, 151), 3)

    # Manos
    pygame.draw.ellipse(surf, c_skin, (105, 145, 16, 14))
    pygame.draw.ellipse(surf, c_skin, (140, 145, 16, 14))

    return surf

def _draw_brutus(sz):
    """
    BRUTUS - Gólem de Chatarra
    Criatura enorme formada por placas oxidadas, cables, brazos colosales
    y un núcleo naranja luminoso en el pecho.
    """
    surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
    c_rust = (115, 75, 50)
    c_iron = (55, 60, 70)
    c_iron_dark = (35, 38, 45)

    # Aura térmica del núcleo
    for r in range(12, 0, -3):
        alpha = 25 + r * 6
        glow = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 140, 0, alpha), (128, 140), 45 + r * 3)
        surf.blit(glow, (0, 0))

    # Piernas metálicas pesadas
    pygame.draw.rect(surf, c_iron_dark, (68, 185, 48, 62), border_radius=6)
    pygame.draw.rect(surf, c_iron_dark, (140, 185, 48, 62), border_radius=6)
    pygame.draw.rect(surf, c_rust, (62, 235, 60, 18), border_radius=4)
    pygame.draw.rect(surf, c_rust, (134, 235, 60, 18), border_radius=4)

    # Torso masivo con placas
    pygame.draw.rect(surf, c_iron, (52, 95, 152, 95), border_radius=12)
    pygame.draw.rect(surf, c_rust, (62, 105, 132, 80), border_radius=8)

    # Cables expuestos
    pygame.draw.line(surf, NEON_RED, (60, 115), (75, 175), 4)
    pygame.draw.line(surf, NEON_YELLOW, (196, 115), (180, 175), 4)

    # Núcleo naranja incandescente (punto débil)
    pygame.draw.circle(surf, (40, 15, 0), (128, 142), 26)
    pygame.draw.circle(surf, (255, 100, 0), (128, 142), 22)
    pygame.draw.circle(surf, (255, 200, 30), (128, 142), 14)
    pygame.draw.circle(surf, WHITE, (128, 142), 7)

    # Cabeza/Visor de caldera
    pygame.draw.rect(surf, c_iron_dark, (100, 45, 56, 52), border_radius=6)
    pygame.draw.rect(surf, c_rust, (104, 49, 48, 44), 3, border_radius=4)
    pygame.draw.rect(surf, (255, 160, 0), (112, 62, 32, 14), border_radius=3)
    pygame.draw.circle(surf, WHITE, (128, 69), 4)

    # Brazos colosales con puños de martinete
    pygame.draw.ellipse(surf, c_rust, (10, 92, 54, 90))
    pygame.draw.ellipse(surf, c_rust, (192, 92, 54, 90))
    pygame.draw.rect(surf, c_iron_dark, (6, 170, 60, 68), border_radius=10)
    pygame.draw.rect(surf, c_iron_dark, (190, 170, 60, 68), border_radius=10)
    pygame.draw.circle(surf, NEON_ORANGE, (36, 200), 10)
    pygame.draw.circle(surf, NEON_ORANGE, (220, 200), 10)

    return surf

def _draw_nyx(sz):
    """
    NYX - Sombra Espectral
    Figura delgada y flotante, cubierta por una capa morada que se desintegra
    en partículas oscuras. Ojos violetas brillantes y dagas gemelas.
    """
    surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
    c_cloak = (60, 18, 92)
    c_cloak_light = (115, 38, 165)

    # Aura espectral violeta
    for r in range(12, 0, -3):
        alpha = 20 + r * 6
        glow = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (180, 40, 255, alpha), (40 - r, 20 - r, 176 + r*2, 210 + r*2))
        surf.blit(glow, (0, 0))

    # Capa inferior desintegrándose (partículas oscuras flotantes)
    for px, py, pw in [(75, 220, 16), (110, 235, 18), (145, 225, 20), (90, 242, 10), (160, 240, 12)]:
        pygame.draw.ellipse(surf, c_cloak, (px, py, pw, 18))
        pygame.draw.circle(surf, (150, 40, 210), (px + pw//2, py + 8), 3)

    # Silueta de capa/cuerpo espectral
    body_pts = [(128, 45), (170, 95), (185, 175), (165, 225), (128, 200), (91, 225), (71, 175), (86, 95)]
    pygame.draw.polygon(surf, c_cloak, body_pts)
    pygame.draw.polygon(surf, c_cloak_light, body_pts, 3)

    # Capucha
    pygame.draw.ellipse(surf, (30, 8, 48), (96, 32, 64, 68))
    pygame.draw.ellipse(surf, c_cloak_light, (96, 32, 64, 68), 2)

    # Ojos violetas brillantes
    pygame.draw.ellipse(surf, (255, 60, 240), (108, 58, 16, 10))
    pygame.draw.ellipse(surf, (255, 60, 240), (132, 58, 16, 10))
    pygame.draw.circle(surf, WHITE, (116, 63), 3)
    pygame.draw.circle(surf, WHITE, (140, 63), 3)

    # Dagas gemelas de plasma púrpura
    # Daga izquierda
    pygame.draw.line(surf, (20, 20, 20), (70, 145), (45, 195), 5)
    pygame.draw.polygon(surf, NEON_MAGENTA, [(45, 195), (30, 235), (42, 210)])
    pygame.draw.line(surf, WHITE, (45, 195), (33, 230), 2)

    # Daga derecha
    pygame.draw.line(surf, (20, 20, 20), (186, 145), (211, 195), 5)
    pygame.draw.polygon(surf, NEON_MAGENTA, [(211, 195), (226, 235), (214, 210)])
    pygame.draw.line(surf, WHITE, (211, 195), (223, 230), 2)

    return surf

def _draw_florax(sz):
    """
    FLORAX - Planta Mutante
    Planta monstruosa con raíces gruesas, espinas, boca carnívora con colmillos
    y una gran flor naranja en la cabeza.
    """
    surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
    c_stem = (28, 95, 38)
    c_stem_dark = (16, 58, 24)

    # Raíces y tentáculos vegetales basales
    root_curves = [
        ((60, 170), (25, 245), 14),
        ((90, 180), (65, 252), 12),
        ((128, 190), (128, 256), 14),
        ((166, 180), (191, 252), 12),
        ((196, 170), (231, 245), 14),
    ]
    for (x1, y1), (x2, y2), w in root_curves:
        pygame.draw.line(surf, c_stem_dark, (x1, y1), (x2, y2), w)
        pygame.draw.line(surf, c_stem, (x1, y1), (x2, y2), w - 4)

    # Espinas
    for sx, sy, dx, dy in [(50, 200, -12, -4), (206, 200, 12, -4), (80, 220, -10, 6), (176, 220, 10, 6)]:
        pygame.draw.polygon(surf, (190, 210, 60), [(sx, sy), (sx + dx, sy + dy), (sx, sy + 8)])

    # Tronco central carnoso
    pygame.draw.ellipse(surf, c_stem, (72, 85, 112, 110))
    pygame.draw.ellipse(surf, c_stem_dark, (72, 85, 112, 110), 3)

    # Gran Boca con dientes
    pygame.draw.ellipse(surf, (110, 15, 20), (84, 110, 88, 55))
    pygame.draw.ellipse(surf, (30, 0, 0), (90, 116, 76, 42))

    # Dientes afilados
    for tx in range(94, 162, 12):
        pygame.draw.polygon(surf, (240, 240, 220), [(tx, 116), (tx + 5, 130), (tx + 10, 116)])
        pygame.draw.polygon(surf, (240, 240, 220), [(tx, 158), (tx + 5, 144), (tx + 10, 158)])

    # Flor carnívora naranja superior (cabeza / debilidad)
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        px = 128 + math.cos(rad) * 36
        py = 55 + math.sin(rad) * 25
        pygame.draw.circle(surf, (255, 90, 20), (int(px), int(py)), 16)
        pygame.draw.circle(surf, (255, 175, 40), (int(px), int(py)), 10)

    # Núcleo de la flor
    pygame.draw.circle(surf, (200, 40, 10), (128, 55), 20)
    pygame.draw.circle(surf, (255, 220, 50), (128, 55), 12)
    pygame.draw.circle(surf, WHITE, (128, 55), 5)

    return surf

def _draw_volt(sz):
    """
    VOLT - Dron de Combate Aéreo
    Robot volador compacto de metal negro carbón, 3 propulsores azules
    y un cañón eléctrico amarillo.
    """
    surf = pygame.Surface((sz, sz), pygame.SRCALPHA)
    c_metal = (32, 38, 48)
    c_metal_light = (65, 75, 95)

    # Chispas y aura eléctrica
    for r in range(8, 0, -2):
        alpha = 20 + r * 7
        glow = pygame.Surface((sz, sz), pygame.SRCALPHA)
        pygame.draw.circle(glow, (0, 200, 255, alpha), (128, 110), 65 + r * 2)
        surf.blit(glow, (0, 0))

    # Chorro de plasma de los 3 propulsores
    thruster_x = [85, 128, 171]
    for tx in thruster_x:
        pygame.draw.rect(surf, c_metal, (tx - 10, 150, 20, 22), border_radius=4)
        # Llamarada cian neón
        pygame.draw.polygon(surf, NEON_CYAN, [(tx - 8, 172), (tx, 225), (tx + 8, 172)])
        pygame.draw.polygon(surf, WHITE, [(tx - 4, 172), (tx, 205), (tx + 4, 172)])

    # Chasis principal compacto esférico
    pygame.draw.ellipse(surf, c_metal, (60, 60, 136, 105))
    pygame.draw.ellipse(surf, c_metal_light, (60, 60, 136, 105), 3)

    # Visor central / Sensor óptico
    pygame.draw.rect(surf, (10, 15, 25), (86, 92, 84, 28), border_radius=6)
    pygame.draw.rect(surf, NEON_CYAN, (90, 96, 76, 20), border_radius=4)
    pygame.draw.circle(surf, WHITE, (128, 106), 6)

    # Cañón eléctrico amarillo frontal
    pygame.draw.rect(surf, (20, 22, 28), (175, 96, 45, 18), border_radius=3)
    pygame.draw.rect(surf, NEON_YELLOW, (185, 100, 35, 10), border_radius=2)
    pygame.draw.circle(surf, (255, 240, 100), (220, 105), 8)
    pygame.draw.circle(surf, WHITE, (220, 105), 4)

    return surf

def create_enemy_sprites():
    """
    Carga las texturas oficiales pixel-art extraídas para los 5 enemigos
    (Xyron, Brutus, Nyx, Florax, Volt) o recurre a los generadores procedurales.
    """
    sprites = {}
    sz = 256

    generators = {
        "xyron": _draw_xyron,
        "brutus": _draw_brutus,
        "nyx": _draw_nyx,
        "florax": _draw_florax,
        "volt": _draw_volt,
    }

    # 1. Cargar texturas de sprites (prioridad a los archivos extraídos oficiales)
    for name, gen in generators.items():
        png_path = os.path.join("assets", "sprites", f"{name}.png")
        if os.path.exists(png_path):
            try:
                loaded = pygame.image.load(png_path).convert_alpha()
                if loaded.get_size() != (sz, sz):
                    loaded = pygame.transform.scale(loaded, (sz, sz))
                sprites[name] = loaded
            except Exception:
                sprites[name] = gen(sz)
        else:
            sprites[name] = gen(sz)

    # 2. Aliases para compatibilidad con modos previos
    sprites["drone"] = sprites["volt"]
    sprites["imp"] = sprites["xyron"]
    sprites["baron"] = sprites["brutus"]

    # 3. Proyectiles
    p_play = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.circle(p_play, (0, 180, 220), (24, 24), 22)
    pygame.draw.circle(p_play, (0, 243, 255), (24, 24), 16)
    pygame.draw.circle(p_play, (100, 255, 255), (24, 24), 9)
    pygame.draw.circle(p_play, (240, 255, 255), (24, 24), 4)
    sprites["proj_player"] = p_play

    p_ene = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.circle(p_ene, (180, 0, 30),   (24, 24), 22)
    pygame.draw.circle(p_ene, (255, 30, 60),   (24, 24), 16)
    pygame.draw.circle(p_ene, (255, 120, 0),   (24, 24), 9)
    pygame.draw.circle(p_ene, (255, 240, 200), (24, 24), 4)
    sprites["proj_enemy"] = p_ene

    return sprites
