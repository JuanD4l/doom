"""
================================================================================
CAPA DE MOTOR DE RENDERIZADO (Engine Layer - Raycaster)
================================================================================
Motor de renderizado DDA (Digital Differential Analyzer) 2.5D idéntico al motor
de DOOM clásico. Mapea columnas de textura y proyecta billboards en 3D con Z-Buffer.
================================================================================
"""

import math
import pygame
from src.config.settings import (
    SCREEN_WIDTH, VIEWPORT_HEIGHT, NUM_RAYS, RAY_WIDTH,
    MAX_DEPTH, HALF_FOV, FOV, DIST_PROJ, TEX_SIZE,
    COLOR_ABYSS, COLOR_CEILING, COLOR_FLOOR, NEON_RED
)
from src.engine.map import MAP_GRID, MAP_W, MAP_H

class RaycasterRenderer:
    def __init__(self, screen, wall_textures, sprites):
        self.screen = screen
        self.wall_textures = wall_textures
        self.sprites = sprites
        self.z_buffer = [MAX_DEPTH] * NUM_RAYS

    def render(self, player, enemies, projectiles, particles):
        self.z_buffer = [MAX_DEPTH] * NUM_RAYS  # Reiniciar buffer cada frame
        self._draw_floor_and_ceiling()
        self._cast_and_render_walls(player)
        self._render_sprites(player, enemies, projectiles, particles)

    def _draw_floor_and_ceiling(self):
        half_h = VIEWPORT_HEIGHT // 2

        # Degradado del techo
        for y in range(0, half_h, 8):
            factor = y / half_h
            r = int(COLOR_ABYSS[0] + (COLOR_CEILING[0] - COLOR_ABYSS[0]) * factor)
            g = int(COLOR_ABYSS[1] + (COLOR_CEILING[1] - COLOR_ABYSS[1]) * factor)
            b = int(COLOR_ABYSS[2] + (COLOR_CEILING[2] - COLOR_ABYSS[2]) * factor)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, SCREEN_WIDTH, 8))

        # Degradado del suelo
        for y in range(half_h, VIEWPORT_HEIGHT, 8):
            factor = (y - half_h) / half_h
            r = int(COLOR_FLOOR[0] + (COLOR_ABYSS[0] - COLOR_FLOOR[0]) * factor)
            g = int(COLOR_FLOOR[1] + (COLOR_ABYSS[1] - COLOR_FLOOR[1]) * factor)
            b = int(COLOR_FLOOR[2] + (COLOR_ABYSS[2] - COLOR_FLOOR[2]) * factor)
            pygame.draw.rect(self.screen, (r, g, b), (0, y, SCREEN_WIDTH, 8))

        pygame.draw.line(self.screen, (32, 24, 50), (0, half_h), (SCREEN_WIDTH, half_h), 2)

    def _cast_and_render_walls(self, player):
        start_angle = player.angle - HALF_FOV

        for r in range(NUM_RAYS):
            ray_angle = start_angle + (r / NUM_RAYS) * FOV
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            map_x = int(player.x)
            map_y = int(player.y)

            delta_dist_x = abs(1.0 / cos_a) if abs(cos_a) > 1e-6 else 1e30
            delta_dist_y = abs(1.0 / sin_a) if abs(sin_a) > 1e-6 else 1e30

            if cos_a < 0:
                step_x = -1
                side_dist_x = (player.x - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - player.x) * delta_dist_x

            if sin_a < 0:
                step_y = -1
                side_dist_y = (player.y - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - player.y) * delta_dist_y

            hit = False
            side = 0
            wall_type = 1

            while not hit:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                if 0 <= map_x < MAP_W and 0 <= map_y < MAP_H:
                    if MAP_GRID[map_y][map_x] > 0:
                        hit = True
                        wall_type = MAP_GRID[map_y][map_x]
                else:
                    hit = True
                    break

            if side == 0:
                perp_dist = (map_x - player.x + (1 - step_x) / 2.0) / cos_a
            else:
                perp_dist = (map_y - player.y + (1 - step_y) / 2.0) / sin_a

            perp_dist = max(0.05, perp_dist)
            self.z_buffer[r] = perp_dist

            if side == 0:
                wall_hit = player.y + perp_dist * sin_a
            else:
                wall_hit = player.x + perp_dist * cos_a
            wall_hit -= math.floor(wall_hit)
            tex_x = int(wall_hit * TEX_SIZE)
            tex_x = max(0, min(TEX_SIZE - 1, tex_x))

            proj_h = int((1.0 / perp_dist) * DIST_PROJ)
            top = (VIEWPORT_HEIGHT // 2) - (proj_h // 2)

            shade_level = min(6, int(perp_dist / 2.8))
            tex_surface = self.wall_textures[wall_type][side][shade_level]

            slice_surf = tex_surface.subsurface((tex_x, 0, 1, TEX_SIZE))
            col_w = int(RAY_WIDTH) + 1
            scaled_slice = pygame.transform.scale(slice_surf, (col_w, proj_h))

            col_x = int(r * RAY_WIDTH)
            self.screen.blit(scaled_slice, (col_x, top))

    def _render_sprites(self, player, enemies, projectiles, particles):
        renderables = []

        for enemy in enemies:
            if enemy.alive:
                dx = enemy.x - player.x
                dy = enemy.y - player.y
                dist = math.hypot(dx, dy)
                renderables.append({
                    "type": "enemy",
                    "obj": enemy,
                    "x": enemy.x,
                    "y": enemy.y,
                    "z_offset": math.sin(enemy.hover_timer) * 0.14 if (getattr(enemy, "is_aerial", False) or enemy.enemy_type in ("volt", "drone", "nyx")) else 0.0,
                    "dist": dist
                })

        for p in projectiles:
            if p.alive:
                dx = p.x - player.x
                dy = p.y - player.y
                dist = math.hypot(dx, dy)
                renderables.append({
                    "type": "projectile",
                    "obj": p,
                    "x": p.x,
                    "y": p.y,
                    "z_offset": 0.0,
                    "dist": dist
                })

        for part in particles:
            if part.alive:
                dx = part.x - player.x
                dy = part.y - player.y
                dist = math.hypot(dx, dy)
                renderables.append({
                    "type": "particle",
                    "obj": part,
                    "x": part.x,
                    "y": part.y,
                    "z_offset": 0.0,
                    "dist": dist
                })

        renderables.sort(key=lambda item: item["dist"], reverse=True)

        for item in renderables:
            dist = item["dist"]
            if dist < 0.05 or dist > MAX_DEPTH:
                continue

            dx = item["x"] - player.x
            dy = item["y"] - player.y

            inv_cos = math.cos(-player.angle)
            inv_sin = math.sin(-player.angle)
            trans_x = dx * inv_cos - dy * inv_sin
            trans_y = dx * inv_sin + dy * inv_cos

            # Umbral cercano optimizado para que los enemigos no desaparezcan al pasar a su lado
            if trans_x <= 0.05:
                continue

            screen_x = int((SCREEN_WIDTH / 2.0) + (trans_y / trans_x) * DIST_PROJ)
            scale = (1.0 / trans_x) * DIST_PROJ
            draw_y = int((VIEWPORT_HEIGHT / 2.0) - (scale * item["z_offset"]))

            if item["type"] == "enemy":
                enemy = item["obj"]
                sprite_surf = self.sprites.get(enemy.enemy_type, self.sprites.get("drone", list(self.sprites.values())[0]))

                # Orientación lateral / vista de costado:
                # Si el jugador ve al enemigo desde el flanco izquierdo (trans_y < 0), volteamos el sprite
                # para que mire hacia el jugador/centro, logrando perspectiva de perfil
                if trans_y < 0:
                    base_surf = pygame.transform.flip(sprite_surf, True, False)
                else:
                    base_surf = sprite_surf

                # Tamaños y factores de escala según arquetipo
                if enemy.enemy_type in ("brutus", "baron"):
                    min_sz = 160
                    size_mult = 2.4
                elif enemy.enemy_type == "florax":
                    min_sz = 140
                    size_mult = 2.1
                elif enemy.enemy_type in ("xyron", "imp"):
                    min_sz = 110
                    size_mult = 1.8
                elif enemy.enemy_type == "nyx":
                    min_sz = 100
                    size_mult = 1.7
                else:  # volt / drone
                    min_sz = 80
                    size_mult = 1.5

                # Cálculo de tamaño con compresión de perspectiva lateral (perfil de costado)
                proj_sz = int(scale * size_mult)
                target_h = max(min_sz, min(proj_sz, 520))
                
                # Efecto visual de costado (compresión sutil de anchura según el ángulo lateral)
                lateral_factor = abs(trans_y) / max(0.4, trans_x)
                width_ratio = max(0.72, min(1.0, 1.0 - (lateral_factor * 0.12)))
                target_w = int(target_h * width_ratio)

                scaled_surf = pygame.transform.scale(base_surf, (target_w, target_h))

                # Indicador visual de punto débil / ventana de vulnerabilidad
                if getattr(enemy, "is_vulnerable", False):
                    glow_pulse = int(120 + math.sin(pygame.time.get_ticks() * 0.012) * 60)
                    vuln_surf = scaled_surf.copy()
                    vuln_surf.fill((255, 210, 40, glow_pulse), special_flags=pygame.BLEND_RGBA_ADD)
                    scaled_surf = vuln_surf

                if enemy.hit_flash > 0:
                    flash = scaled_surf.copy()
                    flash.fill((255, 80, 80, 160), special_flags=pygame.BLEND_RGBA_ADD)
                    scaled_surf = flash

                # Dibujo en columnas billboard con z-buffer columna por columna
                # (garantiza que el enemigo sea visible aunque esté pasando de costado o cortado por el borde)
                self._draw_billboard(scaled_surf, screen_x, draw_y, trans_x)

                if enemy.hp < enemy.max_hp:
                    bar_w = max(35, target_w)
                    bar_h = max(6, target_h // 15)
                    bar_x = screen_x - bar_w // 2
                    bar_y = draw_y - target_h // 2 - bar_h - 6
                    col_idx = max(0, min(NUM_RAYS - 1, int(screen_x / RAY_WIDTH)))
                    if trans_x < self.z_buffer[col_idx] + 0.35:
                        pygame.draw.rect(self.screen, (15, 15, 15), (bar_x - 1, bar_y - 1, bar_w + 2, bar_h + 2))
                        pygame.draw.rect(self.screen, (20, 20, 20), (bar_x, bar_y, bar_w, bar_h))
                        fill_w = int((enemy.hp / enemy.max_hp) * bar_w)
                        hp_col = (0, 255, 80) if enemy.hp > enemy.max_hp * 0.5 else NEON_RED
                        pygame.draw.rect(self.screen, hp_col, (bar_x, bar_y, fill_w, bar_h))

            elif item["type"] == "projectile":
                proj = item["obj"]
                surf_name = "proj_player" if proj.is_player else "proj_enemy"
                sprite_surf = self.sprites[surf_name]
                proj_sz = max(7, int(scale * 0.28))
                scaled = pygame.transform.scale(sprite_surf, (proj_sz, proj_sz))
                self._draw_billboard(scaled, screen_x, draw_y, trans_x)

            elif item["type"] == "particle":
                part = item["obj"]
                part_sz = max(2, int(scale * 0.09 * (part.life / part.max_life)))
                col_idx = max(0, min(NUM_RAYS - 1, int(screen_x / RAY_WIDTH)))
                if trans_x < self.z_buffer[col_idx]:
                    pygame.draw.circle(self.screen, part.color, (screen_x, draw_y), part_sz)

    def _draw_billboard(self, surf, center_x, center_y, depth):
        w, h = surf.get_size()
        left = center_x - w // 2
        top = center_y - h // 2

        start_col = max(0, int(left / RAY_WIDTH))
        end_col = min(NUM_RAYS - 1, int((left + w) / RAY_WIDTH))

        for col in range(start_col, end_col + 1):
            if depth < self.z_buffer[col]:
                col_x = int(col * RAY_WIDTH)
                src_x = col_x - left
                src_w = int(RAY_WIDTH) + 1
                if 0 <= src_x < w:
                    sub_w = min(src_w, w - src_x)
                    slice_rect = pygame.Rect(src_x, 0, sub_w, h)
                    self.screen.blit(surf, (col_x, top), area=slice_rect)
