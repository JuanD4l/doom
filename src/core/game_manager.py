"""
================================================================================
CAPA CENTRAL DE GESTIÓN Y ORQUESTACIÓN (Core / Application Layer)
================================================================================
"""

import sys
import os
import math
import random
import json
import pygame

from src.config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, VIEWPORT_HEIGHT, FPS, SAVE_FILE,
    NEON_CYAN, NEON_RED, NEON_MAGENTA, NEON_YELLOW, NEON_ORANGE, NEON_GREEN, NEON_PURPLE
)
from src.audio.synthesizer import SoundSynthesizer
from src.graphics.textures import create_wall_textures
from src.graphics.sprites import create_weapon_sprites, create_enemy_sprites
from src.engine.map import MAP_GRID, MAP_W, MAP_H
from src.engine.raycaster import RaycasterRenderer
from src.domain.player import Player
from src.domain.enemy import Enemy
from src.domain.projectile import Projectile
from src.domain.particle import Particle
from src.ui.hud import CyberHUD
from src.ui.screens import UIScreens

class CyberDoomGameManager:
    STATE_TITLE = "title"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAMEOVER = "gameover"

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("CYBER-DOOM 2099 // FPS Raycaster Engine")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.audio = SoundSynthesizer()
        self.wall_textures = create_wall_textures()
        self.weapon_sprites = create_weapon_sprites()
        self.enemy_sprites = create_enemy_sprites()
        self.renderer = RaycasterRenderer(self.screen, self.wall_textures, self.enemy_sprites)
        self.hud = CyberHUD(self.screen)

        self.state = self.STATE_TITLE
        self.high_score = self._load_high_score()
        self.mouse_captured = False
        self._reset_game()

    def _load_high_score(self):
        try:
            if os.path.exists(SAVE_FILE):
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except Exception:
            pass
        return 0

    def _save_high_score(self):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception:
            pass

    def _reset_game(self):
        self.player = Player(x=2.5, y=2.5, angle=0.0)
        self.projectiles = []
        self.enemies = []
        self.particles = []
        self.spawn_queue = []
        self.spawn_timer = 0.0
        self.max_simultaneous = 2
        self.wave = 1
        self.kills = 0
        self.score = 0
        self.wave_banner = 3.0
        self.banner_text = ""
        self._spawn_wave()

    def _capture_mouse(self, capture):
        self.mouse_captured = capture
        pygame.mouse.set_visible(not capture)
        pygame.event.set_grab(capture)

    def _spawn_wave(self):
        self.enemies = []
        self.spawn_queue = []
        self.spawn_timer = 2.5

        if self.wave == 1:
            # Oleada 1 (Dificultad Básica): Solo Dron Volt y Tirador Xyron
            # Empiezan solo 2 enemigos; los demás entran como refuerzos escalonados
            self.max_simultaneous = 2
            initial = [("volt", 6.5, 2.5), ("xyron", 9.5, 2.0)]
            self.spawn_queue = ["volt", "xyron"]
            self.banner_text = f">> OLEADA #{self.wave}: PRIMER CONTACTO (VOLT / XYRON) <<"
        elif self.wave == 2:
            # Oleada 2 (Dificultad Media-Baja): Se introduce Florax (Planta Mutante)
            self.max_simultaneous = 3
            initial = [("xyron", 6.5, 2.5), ("volt", 7.5, 1.5)]
            self.spawn_queue = ["florax", "xyron", "volt", "florax"]
            self.banner_text = f">> OLEADA #{self.wave}: ZONA MUTADA (FLORAX DETECTADA) <<"
        elif self.wave == 3:
            # Oleada 3 (Dificultad Media-Alta): Se introduce la Asesina Nyx (Teletransporte)
            self.max_simultaneous = 3
            initial = [("xyron", 6.5, 2.5), ("florax", 6.5, 4.5)]
            self.spawn_queue = ["nyx", "volt", "nyx", "florax", "xyron"]
            self.banner_text = f">> OLEADA #{self.wave}: AMENAZA ESPECTRAL (NYX ACECHANDO) <<"
        elif self.wave == 4:
            # Oleada 4 (Dificultad Alta / Mini-Jefe): ¡Aparece el Gólem Tanque Brutus!
            self.max_simultaneous = 4
            initial = [("xyron", 6.5, 2.5), ("volt", 7.5, 1.5)]
            # Brutus entra como refuerzo pesado tras unos segundos
            self.spawn_queue = ["brutus", "nyx", "florax", "xyron", "brutus"]
            self.banner_text = f">> ¡ALERTA JEFE OLEADA #{self.wave}: TITÁN BRUTUS! <<"
        else:
            # Oleadas 5+ (Supervivencia Infinita Escalar): Desafío progresivo sin fin hasta morir
            self.max_simultaneous = min(6, 3 + self.wave // 3)
            initial = [("xyron", 6.5, 2.5), ("nyx", 7.5, 1.5)]
            total_reinforcements = 4 + min(18, self.wave * 2)
            roster = ["xyron", "brutus", "nyx", "florax", "volt"]
            brutus_w = min(0.35, 0.20 + (self.wave * 0.015))
            nyx_w = min(0.30, 0.20 + (self.wave * 0.012))
            weights = [0.20, brutus_w, nyx_w, 0.15, max(0.08, 0.15 - self.wave * 0.005)]
            self.spawn_queue = random.choices(roster, weights=weights, k=total_reinforcements)
            self.banner_text = f">> ¡SUPERVIVENCIA INFINITA // OLEADA #{self.wave}! <<"

        for etype, sx, sy in initial:
            self.enemies.append(Enemy(sx, sy, etype))

        self.wave_banner = 2.8
        self.audio.play("wave")

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(0.05, dt)

            mouse_rel_x = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == self.STATE_PLAYING:
                            self.state = self.STATE_PAUSED
                            self._capture_mouse(False)
                        elif self.state == self.STATE_PAUSED:
                            self.state = self.STATE_PLAYING
                            self._capture_mouse(True)
                        else:
                            running = False
                    self._handle_keydown(event.key)
                elif event.type == pygame.MOUSEMOTION:
                    if self.state == self.STATE_PLAYING and self.mouse_captured:
                        mouse_rel_x += event.rel[0]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.state == self.STATE_PLAYING:
                            if not self.mouse_captured:
                                self._capture_mouse(True)
                            self._player_shoot()
                        elif self.state == self.STATE_TITLE:
                            self.state = self.STATE_PLAYING
                            self._reset_game()
                            self._capture_mouse(True)
                        elif self.state == self.STATE_PAUSED:
                            self.state = self.STATE_PLAYING
                            self._capture_mouse(True)
                        elif self.state == self.STATE_GAMEOVER:
                            self.state = self.STATE_PLAYING
                            self._reset_game()
                            self._capture_mouse(True)

            keys = pygame.key.get_pressed()

            if self.state == self.STATE_TITLE:
                UIScreens.draw_title(self.screen, self.high_score)
            elif self.state == self.STATE_PLAYING:
                self._update_playing(dt, keys, mouse_rel_x)
                self._draw_playing(dt)
            elif self.state == self.STATE_PAUSED:
                self._draw_playing(dt)
                UIScreens.draw_pause(self.screen)
            elif self.state == self.STATE_GAMEOVER:
                UIScreens.draw_gameover(self.screen, self.wave, self.kills, self.score, self.high_score)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_keydown(self, key):
        if self.state == self.STATE_TITLE:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.STATE_PLAYING
                self._reset_game()
                self._capture_mouse(True)
        elif self.state == self.STATE_PLAYING:
            if key == pygame.K_SPACE:
                self._player_shoot()
        elif self.state == self.STATE_PAUSED:
            if key in (pygame.K_p, pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.STATE_PLAYING
                self._capture_mouse(True)
        elif self.state == self.STATE_GAMEOVER:
            if key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                self.state = self.STATE_PLAYING
                self._reset_game()
                self._capture_mouse(True)

    def _player_shoot(self):
        if self.player.cooldown <= 0.0:
            self.player.cooldown = 0.30
            self.audio.play("shotgun")
            self.player.screen_shake = 0.16

            spreads = [-0.07, -0.035, 0.0, 0.035, 0.07]
            for s_ang in spreads:
                proj = Projectile(self.player.x, self.player.y, self.player.angle + s_ang, speed=14.0, is_player=True, damage=18)
                self.projectiles.append(proj)

            fx = self.player.x + math.cos(self.player.angle) * 0.45
            fy = self.player.y + math.sin(self.player.angle) * 0.45
            for _ in range(8):
                self.particles.append(Particle(fx, fy, NEON_CYAN, size=5, speed=3.2, life=0.18))

    def _update_playing(self, dt, keys, mouse_rel_x):
        self.player.update(dt, keys, mouse_rel_x, self.audio)

        for p in self.projectiles[:]:
            p.update(dt)
            if not p.alive:
                self.projectiles.remove(p)
                continue

            if not p.is_player:
                if math.hypot(p.x - self.player.x, p.y - self.player.y) < self.player.radius + 0.22:
                    p.alive = False
                    self.player.take_damage(p.damage, self.audio)
                    for _ in range(8):
                        self.particles.append(Particle(self.player.x, self.player.y, NEON_RED, size=5, speed=3.5, life=0.22))
                    if self.player.health <= 0:
                        self.state = self.STATE_GAMEOVER
                        self._capture_mouse(False)
                        if self.score > self.high_score:
                            self.high_score = self.score
                            self._save_high_score()
            else:
                for enemy in self.enemies:
                    if enemy.alive and math.hypot(p.x - enemy.x, p.y - enemy.y) < enemy.radius + 0.28:
                        p.alive = False
                        enemy.take_damage(p.damage, self.audio)
                        self.player.hitmarker_time = 0.15
                        self.audio.play("hitmarker")

                        for _ in range(6):
                            self.particles.append(Particle(enemy.x, enemy.y, NEON_MAGENTA, size=5, speed=3.8, life=0.25))

                        if not enemy.alive:
                            self.kills += 1
                            self.score += enemy.score_value
                            # Recompensa específica de la ficha técnica
                            if hasattr(enemy, "reward") and enemy.reward:
                                rew_t = enemy.reward.get("type")
                                if rew_t == "healing_seed":
                                    self.player.health = min(self.player.max_health, self.player.health + 25)
                                elif rew_t == "energy_ammo":
                                    self.player.shield = min(self.player.max_shield, self.player.shield + 20)
                                elif rew_t == "coins":
                                    self.score += enemy.reward.get("amount", 10) * 10
                            else:
                                self.player.shield = min(self.player.max_shield, self.player.shield + 12)

                            for _ in range(22):
                                self.particles.append(Particle(enemy.x, enemy.y, NEON_CYAN, size=6, speed=6.0, life=0.45))
                        break

        # Manejo de refuerzos escalonados (evita soltar todos los enemigos de golpe)
        alive_count = len([e for e in self.enemies if e.alive])
        if self.spawn_queue and alive_count < self.max_simultaneous:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0.0 or alive_count < 2:
                self.spawn_timer = random.uniform(3.2, 4.6)
                next_etype = self.spawn_queue.pop(0)

                valid_spawns = []
                for y in range(1, MAP_H - 1):
                    for x in range(1, MAP_W - 1):
                        if MAP_GRID[y][x] == 0:
                            d = math.hypot(x + 0.5 - self.player.x, y + 0.5 - self.player.y)
                            if 4.0 <= d <= 11.0:
                                valid_spawns.append((x + 0.5, y + 0.5))

                if valid_spawns:
                    sx, sy = random.choice(valid_spawns)
                    new_enemy = Enemy(sx, sy, next_etype)
                    self.enemies.append(new_enemy)

                    # Efecto de teletransporte / warp de refuerzo
                    self.audio.play("wave" if next_etype == "brutus" else "laser")
                    p_col = NEON_ORANGE if next_etype == "brutus" else (NEON_MAGENTA if next_etype == "nyx" else NEON_CYAN)
                    for _ in range(16):
                        self.particles.append(Particle(sx, sy, p_col, size=6, speed=4.5, life=0.35))

        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(dt, self.player, self.projectiles, self.audio)

        for part in self.particles[:]:
            part.update(dt)
            if not part.alive:
                self.particles.remove(part)

        # La oleada se supera cuando no quedan enemigos activos NI refuerzos pendientes
        alive_count = len([e for e in self.enemies if e.alive])
        if alive_count == 0 and len(self.spawn_queue) == 0:
            self.wave += 1
            self.score += 500 + self.wave * 100
            # Bonificación de supervivencia infinita: curación y recarga de escudo para seguir batallando
            self.player.health = min(self.player.max_health, self.player.health + 35)
            self.player.shield = min(self.player.max_shield, self.player.shield + 25)
            self._spawn_wave()

        if self.wave_banner > 0:
            self.wave_banner = max(0.0, self.wave_banner - dt)

    def _draw_playing(self, dt):
        self.renderer.render(self.player, self.enemies, self.projectiles, self.particles)

        weapon_surf = self.weapon_sprites[self.player.weapon_frame]
        bob_x = math.cos(self.player.walk_bob) * 12
        bob_y = abs(math.sin(self.player.walk_bob)) * 16

        shake_x = (random.random() * 2.0 - 1.0) * 8 * self.player.screen_shake
        shake_y = (random.random() * 2.0 - 1.0) * 8 * self.player.screen_shake

        weapon_x = (SCREEN_WIDTH // 2) - (weapon_surf.get_width() // 2) + int(bob_x + shake_x)
        weapon_y = VIEWPORT_HEIGHT - weapon_surf.get_height() + int(bob_y + shake_y)
        self.screen.blit(weapon_surf, (weapon_x, weapon_y))

        cx, cy = SCREEN_WIDTH // 2, VIEWPORT_HEIGHT // 2
        ret_color = NEON_RED if self.player.cooldown > 0.1 else NEON_CYAN
        pygame.draw.circle(self.screen, ret_color, (cx, cy), 5, 1)
        pygame.draw.line(self.screen, ret_color, (cx - 15, cy), (cx - 6, cy), 2)
        pygame.draw.line(self.screen, ret_color, (cx + 6, cy), (cx + 15, cy), 2)
        pygame.draw.line(self.screen, ret_color, (cx, cy - 15), (cx, cy - 6), 2)
        pygame.draw.line(self.screen, ret_color, (cx, cy + 6), (cx, cy + 15), 2)

        if self.player.hitmarker_time > 0:
            hm_sz = 9
            pygame.draw.line(self.screen, NEON_RED, (cx - hm_sz, cy - hm_sz), (cx - 4, cy - 4), 3)
            pygame.draw.line(self.screen, NEON_RED, (cx + 4, cy + 4), (cx + hm_sz, cy + hm_sz), 3)
            pygame.draw.line(self.screen, NEON_RED, (cx + hm_sz, cy - hm_sz), (cx + 4, cy - 4), 3)
            pygame.draw.line(self.screen, NEON_RED, (cx - hm_sz, cy + hm_sz), (cx - 4, cy + 4), 3)

        if self.player.hurt_flash > 0:
            flash_surf = pygame.Surface((SCREEN_WIDTH, VIEWPORT_HEIGHT))
            flash_surf.fill((255, 0, 40))
            flash_alpha = int(self.player.hurt_flash * 150)
            flash_surf.set_alpha(flash_alpha)
            self.screen.blit(flash_surf, (0, 0))

        if self.wave_banner > 0:
            font_banner = pygame.font.SysFont("Consolas", 28, bold=True)
            txt_b = font_banner.render(getattr(self, "banner_text", f">> ¡OLEADA #{self.wave} DESPLEGADA! <<"), True, NEON_YELLOW)
            bx = SCREEN_WIDTH // 2 - txt_b.get_width() // 2
            by = 65
            pygame.draw.rect(self.screen, (10, 15, 25), (bx - 20, by - 10, txt_b.get_width() + 40, txt_b.get_height() + 20), border_radius=6)
            pygame.draw.rect(self.screen, NEON_YELLOW, (bx - 20, by - 10, txt_b.get_width() + 40, txt_b.get_height() + 20), 2, border_radius=6)
            self.screen.blit(txt_b, (bx, by))

        self.hud.draw(self.player, self.wave, self.kills, self.score, self.high_score, self.enemies, dt, self.spawn_queue)
