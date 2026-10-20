"""
================================================================================
CAPA DE GRÁFICOS Y TEXTURAS (Graphics Infrastructure - Textures)
================================================================================
Genera las texturas procedurales de 64x64 de los muros cyberpunk y precalcula
las tablas LUT de sombreado (iluminación de caras X/Y y niebla de distancia).
================================================================================
"""

import pygame
from src.config.settings import (
    TEX_SIZE, NEON_CYAN, NEON_MAGENTA, NEON_YELLOW, NEON_RED,
    NEON_ORANGE, WHITE
)

def create_wall_textures():
    raw_textures = {}

    # TEXTURA 1: Placa Cyber-Matrix
    t1 = pygame.Surface((TEX_SIZE, TEX_SIZE))
    t1.fill((22, 28, 40))
    pygame.draw.rect(t1, (35, 45, 65), (2, 2, 60, 60), 2)
    pygame.draw.line(t1, (12, 16, 24), (0, 32), (64, 32), 2)
    for cx, cy in [(6, 6), (58, 6), (6, 58), (58, 58), (6, 30), (58, 30)]:
        pygame.draw.circle(t1, (80, 95, 125), (cx, cy), 2)
    pygame.draw.line(t1, NEON_CYAN, (20, 4), (20, 60), 3)
    pygame.draw.line(t1, WHITE, (20, 8), (20, 56), 1)
    pygame.draw.line(t1, NEON_CYAN, (44, 4), (44, 60), 3)
    pygame.draw.line(t1, WHITE, (44, 8), (44, 56), 1)
    raw_textures[1] = t1

    # TEXTURA 2: Núcleo Cyber-Core
    t2 = pygame.Surface((TEX_SIZE, TEX_SIZE))
    t2.fill((30, 14, 36))
    pygame.draw.rect(t2, (45, 20, 55), (4, 4, 56, 56))
    pygame.draw.rect(t2, (18, 8, 24), (8, 8, 48, 48))
    pygame.draw.lines(t2, NEON_MAGENTA, False, [(12, 12), (24, 24), (24, 44), (40, 44), (52, 52)], 2)
    pygame.draw.lines(t2, NEON_MAGENTA, False, [(52, 12), (40, 24), (40, 36), (28, 36)], 2)
    pygame.draw.rect(t2, NEON_CYAN, (26, 26, 12, 12))
    pygame.draw.rect(t2, WHITE, (29, 29, 6, 6))
    raw_textures[2] = t2

    # TEXTURA 3: Blindaje Industrial con Peligro
    t3 = pygame.Surface((TEX_SIZE, TEX_SIZE))
    t3.fill((32, 34, 40))
    pygame.draw.rect(t3, (45, 48, 56), (0, 0, 64, 64), 3)
    pygame.draw.rect(t3, (20, 20, 22), (0, 18, 64, 28))
    for x in range(-20, 80, 12):
        pygame.draw.polygon(t3, NEON_YELLOW, [(x, 18), (x + 8, 18), (x - 6, 46), (x - 14, 46)])
    pygame.draw.line(t3, (120, 130, 145), (4, 54), (60, 54), 4)
    pygame.draw.line(t3, (70, 75, 85), (4, 10), (60, 10), 4)
    raw_textures[3] = t3

    # TEXTURA 4: Bio-Mecánica Demoníaca
    t4 = pygame.Surface((TEX_SIZE, TEX_SIZE))
    t4.fill((38, 16, 22))
    pygame.draw.rect(t4, (24, 10, 14), (2, 2, 60, 60))
    pygame.draw.polygon(t4, (60, 25, 35), [(22, 18), (42, 18), (46, 36), (32, 48), (18, 36)])
    pygame.draw.circle(t4, NEON_RED, (26, 26), 4)
    pygame.draw.circle(t4, WHITE, (26, 26), 2)
    pygame.draw.circle(t4, NEON_RED, (38, 26), 4)
    pygame.draw.circle(t4, WHITE, (38, 26), 2)
    pygame.draw.line(t4, NEON_ORANGE, (28, 38), (36, 38), 2)
    pygame.draw.line(t4, NEON_RED, (6, 6), (16, 28), 2)
    pygame.draw.line(t4, NEON_RED, (58, 6), (48, 28), 2)
    raw_textures[4] = t4

    # Tablas de Sombreado LUT
    shaded_library = {}
    factors = [1.0, 0.85, 0.68, 0.52, 0.38, 0.24, 0.12]

    for tid, base_tex in raw_textures.items():
        shaded_library[tid] = {0: [], 1: []}
        for f in factors:
            # Cara X
            s_x = base_tex.copy()
            val_x = int(255 * f)
            dark_x = pygame.Surface((TEX_SIZE, TEX_SIZE))
            dark_x.fill((val_x, val_x, val_x))
            s_x.blit(dark_x, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            shaded_library[tid][0].append(s_x)

            # Cara Y (sombreado lateral)
            s_y = base_tex.copy()
            val_y = int(185 * f)
            dark_y = pygame.Surface((TEX_SIZE, TEX_SIZE))
            dark_y.fill((val_y, val_y, val_y))
            s_y.blit(dark_y, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            shaded_library[tid][1].append(s_y)

    return shaded_library
