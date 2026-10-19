/**
 * CONSOLA INFERIOR HUD ESTILO DOOM (Web Canvas HUD)
 */

class CyberHUD {
    constructor(ctx) {
        this.ctx = ctx;
        this.avatarBlink = 0;
    }

    draw(player, wave, kills, score, scoreHigh, enemies, dt) {
        const ctx = this.ctx;
        const W = CONFIG.SCREEN_WIDTH;
        const hudTop = CONFIG.VIEWPORT_HEIGHT;
        const hudH = CONFIG.HUD_HEIGHT;
        this.avatarBlink += dt;

        // Fondo del panel metálico
        ctx.fillStyle = "#0a0c12";
        ctx.fillRect(0, hudTop, W, hudH);
        ctx.strokeStyle = CONFIG.COLORS.CYAN;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(0, hudTop); ctx.lineTo(W, hudTop);
        ctx.stroke();

        // 1. SALUD Y ESCUDO
        ctx.fillStyle = "#161c28";
        ctx.fillRect(25, hudTop + 20, 200, 38);
        const hpRatio = Math.max(0, player.health / player.maxHealth);
        ctx.fillStyle = hpRatio > 0.4 ? CONFIG.COLORS.GREEN : (hpRatio > 0.2 ? CONFIG.COLORS.YELLOW : CONFIG.COLORS.RED);
        ctx.fillRect(28, hudTop + 23, 194 * hpRatio, 32);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 18px 'Share Tech Mono', monospace";
        ctx.fillText(`SALUD  ${Math.floor(player.health)}%`, 45, hudTop + 45);

        ctx.fillStyle = "#161c28";
        ctx.fillRect(25, hudTop + 70, 200, 38);
        const shRatio = Math.max(0, player.shield / player.maxShield);
        ctx.fillStyle = CONFIG.COLORS.CYAN;
        ctx.fillRect(28, hudTop + 73, 194 * shRatio, 32);
        ctx.fillStyle = "#ffffff";
        ctx.fillText(`ESCUDO ${Math.floor(player.shield)}%`, 45, hudTop + 95);

        // 2. AVATAR DOOM MARINE REACTIVO
        const avX = 265;
        const avY = hudTop + 14;
        ctx.fillStyle = "#121622";
        ctx.fillRect(avX, avY, 105, 102);
        ctx.strokeStyle = CONFIG.COLORS.CYAN;
        ctx.lineWidth = 2;
        ctx.strokeRect(avX, avY, 105, 102);

        const centerX = avX + 52;
        const centerY = avY + 50;
        ctx.fillStyle = CONFIG.COLORS.DARK_METAL;
        ctx.beginPath();
        ctx.arc(centerX, centerY, 34, 0, Math.PI * 2);
        ctx.fill();

        let visorColor = CONFIG.COLORS.CYAN;
        if (player.health < 30) {
            visorColor = Math.floor(this.avatarBlink * 4) % 2 === 0 ? CONFIG.COLORS.RED : "#5a0f14";
        } else if (player.weaponFrame > 0) {
            visorColor = CONFIG.COLORS.YELLOW;
        }

        ctx.fillStyle = visorColor;
        ctx.beginPath();
        ctx.ellipse(centerX, centerY - 2, 24, 10, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(centerX - 18, centerY - 2); ctx.lineTo(centerX + 18, centerY - 2);
        ctx.stroke();

        ctx.fillStyle = "#0e1018";
        ctx.beginPath();
        ctx.moveTo(centerX - 16, centerY + 10);
        ctx.lineTo(centerX + 16, centerY + 10);
        ctx.lineTo(centerX + 10, centerY + 26);
        ctx.lineTo(centerX - 10, centerY + 26);
        ctx.fill();

        ctx.fillStyle = CONFIG.COLORS.CYAN;
        ctx.font = "12px 'Share Tech Mono', monospace";
        ctx.fillText("CYBER-MARINE", avX + 12, avY + 95);

        // 3. PUNTUACIÓN Y ESTADÍSTICAS
        const statsX = 410;
        ctx.fillStyle = CONFIG.COLORS.YELLOW;
        ctx.font = "bold 26px 'Share Tech Mono', monospace";
        ctx.fillText(`PUNTOS: ${String(score).padStart(6, '0')}`, statsX, hudTop + 36);

        ctx.fillStyle = CONFIG.COLORS.MAGENTA;
        ctx.font = "bold 17px 'Share Tech Mono', monospace";
        ctx.fillText(`OLEADA: #${String(wave).padStart(2, '0')}`, statsX, hudTop + 65);

        // Contador de enemigos activos
        const aliveEnemies = enemies ? enemies.filter(e => e.alive).length : 0;
        ctx.fillStyle = CONFIG.COLORS.RED;
        ctx.fillText(`ENEMIGOS ACTIVOS: ${aliveEnemies}`, statsX, hudTop + 90);

        ctx.fillStyle = CONFIG.COLORS.CYAN;
        ctx.font = "15px 'Share Tech Mono', monospace";
        ctx.fillText(`BAJAS: ${String(kills).padStart(3, '0')}`, statsX + 200, hudTop + 65);

        ctx.fillStyle = CONFIG.COLORS.LIGHT_STEEL;
        ctx.font = "14px 'Share Tech Mono', monospace";
        ctx.fillText(`RECORD: ${String(scoreHigh).padStart(6, '0')}`, statsX + 200, hudTop + 90);

        // 4. RADAR TÁCTICO CON BLIPS DE ENEMIGOS
        this._drawRadar(player, enemies, hudTop);
    }

    _drawRadar(player, enemies, hudTop) {
        const ctx = this.ctx;
        const radarSize = 114;
        const rx = CONFIG.SCREEN_WIDTH - radarSize - 22;
        const ry = hudTop + 8;

        ctx.fillStyle = "#060a10";
        ctx.fillRect(rx, ry, radarSize, radarSize);
        ctx.strokeStyle = CONFIG.COLORS.GREEN;
        ctx.lineWidth = 2;
        ctx.strokeRect(rx, ry, radarSize, radarSize);

        const scaleX = radarSize / MAP_W;
        const scaleY = radarSize / MAP_H;

        // Dibujar muros en radar
        ctx.fillStyle = "#163728";
        for (let my = 0; my < MAP_H; my++) {
            for (let mx = 0; mx < MAP_W; mx++) {
                if (GAME_MAP[my][mx] > 0) {
                    ctx.fillRect(rx + mx * scaleX, ry + my * scaleY, scaleX + 0.5, scaleY + 0.5);
                }
            }
        }

        // Dibujar blips rojos/púrpuras parpadeantes para cada enemigo vivo
        if (enemies) {
            for (const e of enemies) {
                if (e.alive) {
                    const ex = rx + e.x * scaleX;
                    const ey = ry + e.y * scaleY;
                    ctx.fillStyle = e.type === "baron" ? CONFIG.COLORS.YELLOW : (e.type === "imp" ? CONFIG.COLORS.RED : CONFIG.COLORS.MAGENTA);
                    ctx.beginPath();
                    ctx.arc(ex, ey, e.type === "baron" ? 3.5 : 2.5, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        }

        // Dibujar Jugador en radar (punto verde y cono de visión)
        const pjX = rx + player.x * scaleX;
        const pjY = ry + player.y * scaleY;
        ctx.fillStyle = CONFIG.COLORS.GREEN;
        ctx.beginPath();
        ctx.arc(pjX, pjY, 3.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = CONFIG.COLORS.CYAN;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(pjX, pjY);
        ctx.lineTo(pjX + Math.cos(player.angle) * 14, pjY + Math.sin(player.angle) * 14);
        ctx.stroke();

        ctx.fillStyle = CONFIG.COLORS.GREEN;
        ctx.font = "11px 'Share Tech Mono', monospace";
        ctx.fillText("RADAR-SCAN", rx + 24, ry + radarSize - 6);
    }
}
