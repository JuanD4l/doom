"""
================================================================================
CAPA DE DOMINIO - PARTÍCULAS (Domain Layer - Particle)
================================================================================
"""

import math
import random

class Particle:
    def __init__(self, x, y, color, size, speed, life):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2.0 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    @property
    def alive(self):
        return self.life > 0
