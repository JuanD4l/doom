"""
================================================================================
CAPA DE INTERFAZ DE USUARIO - HUD (UI Layer - HUD)
================================================================================
"""

import math
import pygame
from src.config.settings import (
    SCREEN_WIDTH, VIEWPORT_HEIGHT, HUD_HEIGHT,
    NEON_CYAN, NEON_GREEN, NEON_YELLOW, NEON_MAGENTA, NEON_RED,
    DARK_METAL, LIGHT_STEEL, WHITE
)
from src.engine.map import MAP_GRID, MAP_W, MAP_H

class CyberHUD:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.SysFont("Consolas", 30, bold=True)
        self.font_med = pygame.font.SysFont("Consolas", 19, bold=True)
        self.font_small = pygame.font.SysFont("Consolas", 14)
        self.avatar_blink = 0.0

    def draw(self, player, wave, kills, score, score_high, enemies, dt, spawn_queue=None):
        hud_top = VIEWPORT_HEIGHT
        self.avatar_blink += dt

        # Fondo del panel inferior
        pygame.draw.rect(self.screen, (10, 12, 18), (0, hud_top, SCREEN_WIDTH, HUD_HEIGHT))
        pygame.draw.line(self.screen, NEON_CYAN, (0, hud_top), (SCREEN_WIDTH, hud_top), 3)

        # 1. SALUD Y ESCUDO
        pygame.draw.rect(self.screen, (22, 28, 40), (25, hud_top + 20, 200, 38), border_radius=4)
        hp_ratio = max(0.0, player.health / player.max_health)
        hp_color = NEON_GREEN if hp_ratio > 0.4 else (NEON_YELLOW if hp_ratio > 0.2 else NEON_RED)
        pygame.draw.rect(self.screen, hp_color, (28, hud_top + 23, int(194 * hp_ratio), 32), border_radius=3)
        txt_hp = self.font_med.render(f"SALUD  {int(player.health)}%", True, WHITE)
        self.screen.blit(txt_hp, (40, hud_top + 29))

        pygame.draw.rect(self.screen, (22, 28, 40), (25, hud_top + 70, 200, 38), border_radius=4)
        sh_ratio = max(0.0, player.shield / player.max_shield)
        pygame.draw.rect(self.screen, NEON_CYAN, (28, hud_top + 73, int(194 * sh_ratio), 32), border_radius=3)
        txt_sh = self.font_med.render(f"ESCUDO {int(player.shield)}%", True, WHITE)
        self.screen.blit(txt_sh, (40, hud_top + 79))

        # 2. AVATAR DOOM MARINE REACTIVO
        av_x = 265
        av_y = hud_top + 14
        pygame.draw.rect(self.screen, (18, 22, 34), (av_x, av_y, 105, 102), border_radius=6)
        pygame.draw.rect(self.screen, NEON_CYAN, (av_x, av_y, 105, 102), 2, border_radius=6)

        center_x = av_x + 52
        center_y = av_y + 50
        pygame.draw.circle(self.screen, DARK_METAL, (center_x, center_y), 34)

        visor_color = NEON_CYAN
        if player.health < 30:
            visor_color = NEON_RED if (int(self.avatar_blink * 4) % 2 == 0) else (90, 15, 20)
        elif player.weapon_frame > 0:
            visor_color = NEON_YELLOW

        pygame.draw.ellipse(self.screen, visor_color, (center_x - 24, center_y - 12, 48, 20))
        pygame.draw.line(self.screen, WHITE, (center_x - 18, center_y - 2), (center_x + 18, center_y - 2), 2)

        pygame.draw.polygon(self.screen, (14, 16, 24), [
            (center_x - 16, center_y + 10),
            (center_x + 16, center_y + 10),
            (center_x + 10, center_y + 26),
            (center_x - 10, center_y + 26)
        ])
        txt_av = self.font_small.render("CYBER-MARINE", True, NEON_CYAN)
        self.screen.blit(txt_av, (av_x + 9, av_y + 86))

        # 3. PUNTUACIÓN Y ESTADÍSTICAS
        stats_x = 410
        txt_score = self.font_large.render(f"PUNTOS: {score:06d}", True, NEON_YELLOW)
        self.screen.blit(txt_score, (stats_x, hud_top + 18))

        txt_wave = self.font_med.render(f"OLEADA: #{wave:02d}", True, NEON_MAGENTA)
        self.screen.blit(txt_wave, (stats_x, hud_top + 52))

        alive_count = len([e for e in enemies if e.alive]) if enemies else 0
        queue_count = len(spawn_queue) if spawn_queue else 0
        if queue_count > 0:
            txt_enemies = self.font_med.render(f"ENEMIGOS: {alive_count:02d} [+{queue_count}]", True, NEON_RED)
        else:
            txt_enemies = self.font_med.render(f"ENEMIGOS: {alive_count:02d}", True, NEON_RED)
        self.screen.blit(txt_enemies, (stats_x, hud_top + 80))

        txt_kills = self.font_small.render(f"BAJAS:  {kills:03d}", True, NEON_CYAN)
        self.screen.blit(txt_kills, (stats_x + 200, hud_top + 54))

        txt_record = self.font_small.render(f"RECORD: {score_high:06d}", True, LIGHT_STEEL)
        self.screen.blit(txt_record, (stats_x + 200, hud_top + 80))

        # 4. RADAR TÁCTICO CON BLIPS DE ENEMIGOS
        self._draw_radar(player, enemies, hud_top)

    def _draw_radar(self, player, enemies, hud_top):
        radar_size = 114
        rx = SCREEN_WIDTH - radar_size - 22
        ry = hud_top + 8

        pygame.draw.rect(self.screen, (6, 10, 16), (rx, ry, radar_size, radar_size), border_radius=6)
        pygame.draw.rect(self.screen, NEON_GREEN, (rx, ry, radar_size, radar_size), 2, border_radius=6)

        scale_x = radar_size / MAP_W
        scale_y = radar_size / MAP_H

        for my in range(MAP_H):
            for mx in range(MAP_W):
                if MAP_GRID[my][mx] > 0:
                    px = rx + int(mx * scale_x)
                    py = ry + int(my * scale_y)
                    pygame.draw.rect(self.screen, (22, 55, 40), (px, py, math.ceil(scale_x), math.ceil(scale_y)))

        # Blips de enemigos
        if enemies:
            for e in enemies:
                if e.alive:
                    ex = rx + int(e.x * scale_x)
                    ey = ry + int(e.y * scale_y)
                    color = NEON_YELLOW if e.enemy_type == "baron" else (NEON_RED if e.enemy_type == "imp" else NEON_MAGENTA)
                    rad = 4 if e.enemy_type == "baron" else 3
                    pygame.draw.circle(self.screen, color, (ex, ey), rad)

        # Jugador y cono de visión
        pj_x = rx + int(player.x * scale_x)
        pj_y = ry + int(player.y * scale_y)
        pygame.draw.circle(self.screen, NEON_GREEN, (pj_x, pj_y), 3)

        cos_a = math.cos(player.angle) * 12
        sin_a = math.sin(player.angle) * 12
        pygame.draw.line(self.screen, NEON_CYAN, (pj_x, pj_y), (int(pj_x + cos_a), int(pj_y + sin_a)), 2)

        txt_radar = self.font_small.render("RADAR-SCAN", True, NEON_GREEN)
        self.screen.blit(txt_radar, (rx + 18, ry + radar_size - 16))
