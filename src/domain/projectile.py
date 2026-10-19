"""
================================================================================
CAPA DE DOMINIO - PROYECTILES (Domain Layer - Projectile)
================================================================================
"""

import math
from src.engine.map import is_wall

class Projectile:
    def __init__(self, x, y, angle, speed, is_player=True, damage=22):
        self.x = x
        self.y = y
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.is_player = is_player
        self.damage = damage
        self.alive = True
        self.life_time = 3.0

    def update(self, dt):
        self.life_time -= dt
        if self.life_time <= 0:
            self.alive = False
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        if is_wall(self.x, self.y):
            self.alive = False
