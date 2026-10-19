"""
================================================================================
CAPA DE DOMINIO - ENEMIGOS (Domain Layer - Enemy AI & Specifications)
================================================================================
Inteligencia artificial enemiga, patrones de ataque táctico, máquina de estados,
ventanas de debilidad y gestión de daño para los 5 arquetipos:
- Xyron (Tirador Alienígena)
- Brutus (Gólem Tanque)
- Nyx (Sombra Asesina)
- Florax (Planta Controladora)
- Volt (Dron Aéreo)
================================================================================
"""

import math
import random
from src.engine.map import is_wall
from src.domain.projectile import Projectile

# Matriz técnica y configuración de balance de entidades
ENEMY_SPECS = {
    "xyron": {
        "name": "Xyron",
        "role": "Tirador",
        "hp": 120,
        "speed": 2.1,
        "radius": 0.42,
        "damage": 12,
        "burst_count": 3,
        "burst_interval": 0.14,
        "cooldown": 2.2,
        "proj_speed": 7.0,
        "weak_duration": 1.2,
        "crit_multiplier": 1.5,
        "score": 100,
        "is_aerial": False,
        "reward": {"type": "energy_ammo", "amount": 0.20}
    },
    "brutus": {
        "name": "Brutus",
        "role": "Tanque",
        "hp": 240,
        "speed": 1.3,
        "radius": 0.60,
        "damage": 45,
        "burst_count": 1,
        "burst_interval": 0.0,
        "cooldown": 2.8,
        "proj_speed": 4.0,
        "weak_duration": 1.8,
        "crit_multiplier": 2.0,
        "score": 180,
        "is_aerial": False,
        "reward": {"type": "coins", "amount": 15}
    },
    "nyx": {
        "name": "Nyx",
        "role": "Asesino",
        "hp": 90,
        "speed": 3.0,
        "radius": 0.38,
        "damage": 55,
        "burst_count": 1,
        "burst_interval": 0.0,
        "cooldown": 3.5,
        "proj_speed": 0.0,
        "weak_duration": 1.5,
        "crit_multiplier": 2.0,
        "score": 140,
        "is_aerial": False,
        "reward": {"type": "shadow_gem", "amount": 0.10}
    },
    "florax": {
        "name": "Florax",
        "role": "Controlador",
        "hp": 150,
        "speed": 1.2,
        "radius": 0.58,
        "damage": 20,
        "burst_count": 1,
        "burst_interval": 0.0,
        "cooldown": 3.0,
        "proj_speed": 5.0,
        "weak_duration": 2.0,
        "crit_multiplier": 1.8,
        "score": 120,
        "is_aerial": False,
        "reward": {"type": "healing_seed", "amount": 0.25}
    },
    "volt": {
        "name": "Volt",
        "role": "Aéreo",
        "hp": 110,
        "speed": 2.9,
        "radius": 0.35,
        "damage": 22,
        "burst_count": 2,
        "burst_interval": 0.16,
        "cooldown": 2.0,
        "proj_speed": 8.0,
        "weak_duration": 1.6,
        "crit_multiplier": 1.5,
        "score": 130,
        "is_aerial": True,
        "reward": {"type": "coins", "amount": 10}
    },
    # Compatibilidad retroactiva con versiones previas
    "drone": {
        "name": "Drone",
        "role": "Aéreo",
        "hp": 35,
        "speed": 2.5,
        "radius": 0.35,
        "damage": 10,
        "burst_count": 1,
        "burst_interval": 0.0,
        "cooldown": 1.7,
        "proj_speed": 6.2,
        "weak_duration": 1.0,
        "crit_multiplier": 1.5,
        "score": 100,
        "is_aerial": True,
        "reward": {"type": "energy_ammo", "amount": 0.10}
    },
    "imp": {
        "name": "Imp",
        "role": "Hostigador",
        "hp": 70,
        "speed": 1.9,
        "radius": 0.40,
        "damage": 22,
        "burst_count": 1,
        "burst_interval": 0.0,
        "cooldown": 2.1,
        "proj_speed": 5.4,
        "weak_duration": 1.2,
        "crit_multiplier": 1.5,
        "score": 250,
        "is_aerial": False,
        "reward": {"type": "coins", "amount": 10}
    },
    "baron": {
        "name": "Baron",
        "role": "Tanque",
        "hp": 190,
        "speed": 1.25,
        "radius": 0.55,
        "damage": 38,
        "burst_count": 1,
        "burst_interval": 0.0,
        "cooldown": 2.6,
        "proj_speed": 7.0,
        "weak_duration": 1.5,
        "crit_multiplier": 2.0,
        "score": 600,
        "is_aerial": False,
        "reward": {"type": "coins", "amount": 25}
    }
}


class Enemy:
    def __init__(self, x, y, enemy_type="xyron"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type.lower()
        if self.enemy_type not in ENEMY_SPECS:
            self.enemy_type = "xyron"

        spec = ENEMY_SPECS[self.enemy_type]
        self.name = spec["name"]
        self.role = spec["role"]
        self.hp = spec["hp"]
        self.max_hp = spec["hp"]
        self.speed = spec["speed"]
        self.radius = spec["radius"]
        self.damage = spec["damage"]
        self.burst_count = spec.get("burst_count", 1)
        self.burst_interval = spec.get("burst_interval", 0.0)
        self.attack_cooldown = spec["cooldown"]
        self.proj_speed = spec["proj_speed"]
        self.weak_duration = spec["weak_duration"]
        self.crit_multiplier = spec["crit_multiplier"]
        self.score_value = spec["score"]
        self.is_aerial = spec.get("is_aerial", False)
        self.reward = spec.get("reward", {})

        self.alive = True
        self.hit_flash = 0.0
        self.attack_timer = random.uniform(0.6, 1.8)
        self.hover_timer = random.uniform(0.0, 6.28)

        # Sistema de debilidad y ráfagas
        self.is_vulnerable = False
        self.vulnerable_timer = 0.0
        self.burst_remaining = 0
        self.burst_timer = 0.0
        self.teleport_cooldown = 0.0

    def update(self, dt, player, projectiles, audio):
        if not self.alive:
            return

        if self.hit_flash > 0:
            self.hit_flash = max(0.0, self.hit_flash - dt * 3.5)

        # Contador de vulnerabilidad / debilidad
        if self.vulnerable_timer > 0:
            self.vulnerable_timer = max(0.0, self.vulnerable_timer - dt)
            self.is_vulnerable = (self.vulnerable_timer > 0)
        else:
            self.is_vulnerable = False

        self.hover_timer += dt * 3.5
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        angle_to_player = math.atan2(dy, dx)
        has_los = self._check_los(player.x, player.y, dist)

        # -------------------------------------------------------------
        # 1. Comportamiento de Movimiento según Tipo
        # -------------------------------------------------------------
        # Si Nyx está inerte por debilidad, o Brutus recuperándose, no se mueve
        can_move = not (self.is_vulnerable and self.enemy_type in ("nyx", "brutus"))
        current_spd = self.speed
        if self.is_vulnerable and self.enemy_type == "xyron":
            current_spd *= 0.45  # Xyron ralentizado tras disparar

        if can_move and dist > 0.6:
            move_spd = current_spd * dt

            # Comportamiento Aéreo / Flanqueo (Volt & Drone)
            if (self.is_aerial or self.enemy_type == "drone") and dist < 4.2 and has_los:
                strafe_ang = angle_to_player + (math.pi / 2 if math.sin(self.hover_timer) > 0 else -math.pi / 2)
                mx = math.cos(strafe_ang) * move_spd * 0.9
                my = math.sin(strafe_ang) * move_spd * 0.9
            # Comportamiento Tirador Distante / Kiting (Xyron)
            elif self.enemy_type == "xyron" and dist < 3.2:
                # Mantener distancia retrocediendo si está demasiado cerca
                mx = -math.cos(angle_to_player) * move_spd * 0.8
                my = -math.sin(angle_to_player) * move_spd * 0.8
            # Comportamiento Asesino de Teletransporte (Nyx)
            elif self.enemy_type == "nyx" and self.teleport_cooldown <= 0.0 and dist > 3.0 and has_los:
                # Intentar teletransportarse al flanco o espalda del jugador
                tp_ang = player.angle + random.choice([math.pi * 0.8, -math.pi * 0.8])
                tp_x = player.x + math.cos(tp_ang) * 1.8
                tp_y = player.y + math.sin(tp_ang) * 1.8
                if not is_wall(tp_x, tp_y):
                    self.x = tp_x
                    self.y = tp_y
                    self.teleport_cooldown = 5.0
                    audio.play("laser")
                    # Tras teletransportarse queda expuesto e inmóvil
                    self.is_vulnerable = True
                    self.vulnerable_timer = self.weak_duration
                mx, my = 0, 0
            # Movimiento estándar / Agresivo directo
            else:
                mx = math.cos(angle_to_player) * move_spd
                my = math.sin(angle_to_player) * move_spd

            # Aplicar movimiento con comprobación de muros
            if not is_wall(self.x + mx, self.y):
                self.x += mx
            if not is_wall(self.x, self.y + my):
                self.y += my

        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= dt

        # -------------------------------------------------------------
        # 2. Manejo de Ráfagas Activas
        # -------------------------------------------------------------
        if self.burst_remaining > 0:
            self.burst_timer -= dt
            if self.burst_timer <= 0:
                self.burst_remaining -= 1
                self.burst_timer = self.burst_interval
                spread = random.uniform(-0.06, 0.06)
                proj = Projectile(
                    self.x, self.y, angle_to_player + spread,
                    self.proj_speed, is_player=False, damage=self.damage
                )
                projectiles.append(proj)
                audio.play("laser")

                # Si terminó la ráfaga, activar debilidad
                if self.burst_remaining == 0:
                    self.is_vulnerable = True
                    self.vulnerable_timer = self.weak_duration

        # -------------------------------------------------------------
        # 3. Lógica de Ataque Principal
        # -------------------------------------------------------------
        self.attack_timer -= dt
        if self.attack_timer <= 0.0 and has_los:
            # Ataque de Melé / Onda de Choque (Brutus)
            if self.enemy_type == "brutus":
                if dist <= 2.2:
                    player.take_damage(self.damage, audio)
                    audio.play("explosion")
                    self.attack_timer = self.attack_cooldown
                    # Núcleo expuesto tras el golpe
                    self.is_vulnerable = True
                    self.vulnerable_timer = self.weak_duration
            # Ataque con Dagas (Nyx)
            elif self.enemy_type == "nyx":
                if dist <= 1.5:
                    player.take_damage(self.damage, audio)
                    audio.play("laser")
                    self.attack_timer = self.attack_cooldown
                    self.is_vulnerable = True
                    self.vulnerable_timer = self.weak_duration
            # Ataque con Proyectiles / Ráfaga a Distancia (Xyron, Volt, Florax)
            elif dist < 12.0:
                self.attack_timer = self.attack_cooldown + random.uniform(-0.2, 0.3)
                if self.burst_count > 1:
                    # Iniciar ráfaga
                    self.burst_remaining = self.burst_count - 1
                    self.burst_timer = self.burst_interval
                else:
                    self.is_vulnerable = True
                    self.vulnerable_timer = self.weak_duration

                proj = Projectile(
                    self.x, self.y, angle_to_player,
                    self.proj_speed, is_player=False, damage=self.damage
                )
                projectiles.append(proj)
                audio.play("laser")

    def _check_los(self, target_x, target_y, dist):
        steps = int(dist * 5)
        if steps == 0:
            return True
        step_x = (target_x - self.x) / steps
        step_y = (target_y - self.y) / steps
        curr_x, curr_y = self.x, self.y
        for _ in range(steps):
            curr_x += step_x
            curr_y += step_y
            if is_wall(curr_x, curr_y):
                return False
        return True

    def take_damage(self, amount, audio):
        # Si el enemigo está en su ventana de debilidad, recibe daño crítico
        applied_dmg = amount
        if self.is_vulnerable:
            applied_dmg = int(amount * self.crit_multiplier)

        self.hp -= applied_dmg
        self.hit_flash = 0.30
        if self.hp <= 0:
            self.alive = False
            audio.play("explosion")
        return applied_dmg
