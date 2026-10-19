"""
================================================================================
CAPA DE INTERFAZ DE USUARIO - PANTALLAS (UI Layer - Screens)
================================================================================
Pantalla de inicio Cyberpunk, superposición de pausa y pantalla de Game Over.
================================================================================
"""

import math
import pygame
from src.config.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_ABYSS,
    NEON_MAGENTA, NEON_CYAN, NEON_YELLOW, NEON_GREEN, NEON_RED,
    WHITE, LIGHT_STEEL
)

class UIScreens:
    @staticmethod
    def draw_title(screen, high_score):
        screen.fill(COLOR_ABYSS)
        time_tick = pygame.time.get_ticks() / 1000.0

        for y in range(0, SCREEN_HEIGHT, 40):
            offset = int(math.sin(time_tick + y * 0.02) * 10)
            pygame.draw.line(screen, (22, 28, 48), (0, y + offset), (SCREEN_WIDTH, y + offset), 1)

        font_huge = pygame.font.SysFont("Consolas", 66, bold=True)
        txt_title_glow = font_huge.render("CYBER - DOOM 2099", True, NEON_MAGENTA)
        txt_title = font_huge.render("CYBER - DOOM 2099", True, NEON_CYAN)
        screen.blit(txt_title_glow, (SCREEN_WIDTH // 2 - txt_title_glow.get_width() // 2 + 4, 114))
        screen.blit(txt_title, (SCREEN_WIDTH // 2 - txt_title.get_width() // 2, 110))

        font_sub = pygame.font.SysFont("Consolas", 23, bold=True)
        txt_sub = font_sub.render("// TRUE FIRST-PERSON SHOOTER RAYCASTER //", True, NEON_YELLOW)
        screen.blit(txt_sub, (SCREEN_WIDTH // 2 - txt_sub.get_width() // 2, 195))

        # Panel de Controles
        ctrl_w, ctrl_h = 600, 230
        cx = (SCREEN_WIDTH - ctrl_w) // 2
        cy = 250
        pygame.draw.rect(screen, (15, 20, 32), (cx, cy, ctrl_w, ctrl_h), border_radius=8)
        pygame.draw.rect(screen, NEON_CYAN, (cx, cy, ctrl_w, ctrl_h), 2, border_radius=8)

        font_ctrl = pygame.font.SysFont("Consolas", 18)
        controls = [
            ("RATÓN (MOUSE-LOOK)", "Giro de cámara y apuntado FPS libre"),
            ("CLICK IZQUIERDO / ESPACIO", "Disparar Cyber-Shotgun de plasma"),
            ("W, A, S, D", "Moverse y desplazarse (Strafe lateral)"),
            ("SHIFT IZQUIERDO", "Correr / Sprint táctico"),
            ("ESCAPE", "Pausar / Liberar ratón")
        ]
        for idx, (k, desc) in enumerate(controls):
            t_k = font_ctrl.render(k, True, NEON_GREEN)
            t_d = font_ctrl.render(desc, True, WHITE)
            screen.blit(t_k, (cx + 25, cy + 22 + idx * 40))
            screen.blit(t_d, (cx + 285, cy + 22 + idx * 40))

        if int(time_tick * 2.5) % 2 == 0:
            font_prompt = pygame.font.SysFont("Consolas", 22, bold=True)
            txt_start = font_prompt.render("[ CLICK O PRESIONA ENTER PARA INICIAR ]", True, WHITE)
            screen.blit(txt_start, (SCREEN_WIDTH // 2 - txt_start.get_width() // 2, 520))

        txt_rec = font_ctrl.render(f"MEJOR RECORD GUARDADO: {high_score:06d}", True, LIGHT_STEEL)
        screen.blit(txt_rec, (SCREEN_WIDTH // 2 - txt_rec.get_width() // 2, 580))

    @staticmethod
    def draw_pause(screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((5, 8, 14))
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        font_p = pygame.font.SysFont("Consolas", 48, bold=True)
        txt = font_p.render("PAUSA // SISTEMA EN ESPERA", True, NEON_YELLOW)
        screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2, 260))

        font_sub = pygame.font.SysFont("Consolas", 22)
        txt_sub = font_sub.render("CLICK O PRESIONA 'P' / ESC PARA CONTINUAR", True, WHITE)
        screen.blit(txt_sub, (SCREEN_WIDTH // 2 - txt_sub.get_width() // 2, 330))

    @staticmethod
    def draw_gameover(screen, wave, kills, score, high_score):
        screen.fill((12, 5, 10))
        font_go = pygame.font.SysFont("Consolas", 58, bold=True)
        txt_go = font_go.render("SISTEMA COMPROMETIDO", True, NEON_RED)
        txt_sub = font_go.render("M.I.A. / GAME OVER", True, WHITE)
        screen.blit(txt_go, (SCREEN_WIDTH // 2 - txt_go.get_width() // 2, 110))
        screen.blit(txt_sub, (SCREEN_WIDTH // 2 - txt_sub.get_width() // 2, 180))

        box_w, box_h = 490, 200
        bx = (SCREEN_WIDTH - box_w) // 2
        by = 260
        pygame.draw.rect(screen, (22, 14, 26), (bx, by, box_w, box_h), border_radius=8)
        pygame.draw.rect(screen, NEON_RED, (bx, by, box_w, box_h), 2, border_radius=8)

        font_res = pygame.font.SysFont("Consolas", 22)
        stats = [
            f"OLEADA ALCANZADA:    #{wave:02d}",
            f"ENEMIGOS ELIMINADOS: {kills}",
            f"PUNTUACIÓN FINAL:    {score:06d}",
            f"MEJOR RECORD:        {high_score:06d}"
        ]
        for i, s in enumerate(stats):
            color = NEON_YELLOW if i == 2 else WHITE
            t = font_res.render(s, True, color)
            screen.blit(t, (bx + 35, by + 28 + i * 40))

        time_tick = pygame.time.get_ticks() / 1000.0
        if int(time_tick * 2) % 2 == 0:
            font_restart = pygame.font.SysFont("Consolas", 22, bold=True)
            txt_rst = font_restart.render("[ PRESIONA 'R', ESPACIO O CLICK PARA REINICIAR ]", True, NEON_GREEN)
            screen.blit(txt_rst, (SCREEN_WIDTH // 2 - txt_rst.get_width() // 2, 520))
