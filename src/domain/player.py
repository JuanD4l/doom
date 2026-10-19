"""
================================================================================
CAPA DE DOMINIO - JUGADOR (Domain Layer - Player)
================================================================================
"""

import math
import pygame
from src.engine.map import is_wall

class Player:
    def __init__(self, x=2.5, y=2.5, angle=0.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 4.2
        self.radius = 0.22  # Radio de colisión optimizado para libre movimiento
        self.mouse_sensitivity = 0.0028

        self.max_health = 100
        self.health = 100
        self.max_shield = 100
        self.shield = 50

        self.cooldown = 0.0
        self.weapon_frame = 0
        self.walk_bob = 0.0
        self.hurt_flash = 0.0
        self.screen_shake = 0.0
        self.hitmarker_time = 0.0

    def take_damage(self, amount, audio):
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed
        self.health = max(0, self.health - amount)
        self.hurt_flash = 0.45
        self.screen_shake = 0.25
        audio.play("hurt")

    def update(self, dt, keys, mouse_rel_x, audio):
        if self.cooldown > 0:
            self.cooldown -= dt
            if self.cooldown > 0.22:
                self.weapon_frame = 1
            elif self.cooldown > 0.10:
                self.weapon_frame = 2
            else:
                self.weapon_frame = 0
        else:
            self.weapon_frame = 0

        if self.hurt_flash > 0:
            self.hurt_flash = max(0.0, self.hurt_flash - dt * 2.2)
        if self.screen_shake > 0:
            self.screen_shake = max(0.0, self.screen_shake - dt * 2.5)
        if self.hitmarker_time > 0:
            self.hitmarker_time = max(0.0, self.hitmarker_time - dt * 5.0)

        # Mouse look
        if mouse_rel_x:
            self.angle += mouse_rel_x * self.mouse_sensitivity

        # Rotación con teclas
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.angle -= 3.5 * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_e]:
            self.angle += 3.5 * dt

        self.angle %= (2.0 * math.pi)

        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        dx, dy = 0.0, 0.0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dx += cos_a
            dy += sin_a
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dx -= cos_a
            dy -= sin_a
        if keys[pygame.K_a]:
            dx += sin_a
            dy -= cos_a
        if keys[pygame.K_d]:
            dx -= sin_a
            dy += cos_a

        length = math.hypot(dx, dy)
        if length > 0.001:
            move_spd = self.speed * dt
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                move_spd *= 1.45

            dx = (dx / length) * move_spd
            dy = (dy / length) * move_spd

            # Deslizamiento en ejes separados
            if not self._check_collision(self.x + dx, self.y):
                self.x += dx

            if not self._check_collision(self.x, self.y + dy):
                self.y += dy

            self.walk_bob += dt * 11.0
        else:
            self.walk_bob = 0.0

    def _check_collision(self, x, y):
        r = self.radius
        return (is_wall(x - r, y - r) or is_wall(x + r, y - r) or
                is_wall(x - r, y + r) or is_wall(x + r, y + r))
