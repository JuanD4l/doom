/**
 * MOTOR DE RENDERIZADO RAYCASTING 2.5D DDA CON MUROS TEXTURIZADOS Y Z-BUFFER
 */

class RaycasterRenderer {
    constructor(canvas, textures, sprites) {
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");
        this.textures = textures;
        this.sprites = sprites;
        this.zBuffer = new Float32Array(CONFIG.NUM_RAYS);
    }

    render(player, enemies, projectiles, particles) {
        this._drawFloorAndCeiling();
        this._castAndRenderWalls(player);
        this._renderSprites(player, enemies, projectiles, particles);
    }

    _drawFloorAndCeiling() {
        const ctx = this.ctx;
        const W = CONFIG.SCREEN_WIDTH;
        const halfH = CONFIG.VIEWPORT_HEIGHT / 2;

        // Techo gradiente
        const gradC = ctx.createLinearGradient(0, 0, 0, halfH);
        gradC.addColorStop(0, CONFIG.COLORS.ABYSS);
        gradC.addColorStop(1, CONFIG.COLORS.CEILING);
        ctx.fillStyle = gradC;
        ctx.fillRect(0, 0, W, halfH);

        // Suelo gradiente
        const gradF = ctx.createLinearGradient(0, halfH, 0, CONFIG.VIEWPORT_HEIGHT);
        gradF.addColorStop(0, CONFIG.COLORS.FLOOR);
        gradF.addColorStop(1, CONFIG.COLORS.ABYSS);
        ctx.fillStyle = gradF;
        ctx.fillRect(0, halfH, W, halfH);

        // Línea de horizonte
        ctx.strokeStyle = "#1e142e";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(0, halfH); ctx.lineTo(W, halfH);
        ctx.stroke();
    }

    _castAndRenderWalls(player) {
        const ctx = this.ctx;
        const W = CONFIG.SCREEN_WIDTH;
        const VH = CONFIG.VIEWPORT_HEIGHT;
        const numRays = CONFIG.NUM_RAYS;
        const rayW = W / numRays;
        const fov = CONFIG.FOV;
        const halfFOV = fov / 2;
        const distProj = (W / 2) / Math.tan(halfFOV);
        const startAng = player.angle - halfFOV;
        const S = CONFIG.TEX_SIZE;

        for (let r = 0; r < numRays; r++) {
            const rayAngle = startAng + (r / numRays) * fov;
            const cosA = Math.cos(rayAngle);
            const sinA = Math.sin(rayAngle);

            let mapX = Math.floor(player.x);
            let mapY = Math.floor(player.y);

            const deltaDistX = Math.abs(cosA) > 1e-6 ? Math.abs(1 / cosA) : 1e30;
            const deltaDistY = Math.abs(sinA) > 1e-6 ? Math.abs(1 / sinA) : 1e30;

            let stepX, sideDistX;
            if (cosA < 0) {
                stepX = -1;
                sideDistX = (player.x - mapX) * deltaDistX;
            } else {
                stepX = 1;
                sideDistX = (mapX + 1.0 - player.x) * deltaDistX;
            }

            let stepY, sideDistY;
            if (sinA < 0) {
                stepY = -1;
                sideDistY = (player.y - mapY) * deltaDistY;
            } else {
                stepY = 1;
                sideDistY = (mapY + 1.0 - player.y) * deltaDistY;
            }

            let hit = false;
            let side = 0;
            let wallType = 1;

            while (!hit) {
                if (sideDistX < sideDistY) {
                    sideDistX += deltaDistX;
                    mapX += stepX;
                    side = 0;
                } else {
                    sideDistY += deltaDistY;
                    mapY += stepY;
                    side = 1;
                }

                if (mapX >= 0 && mapX < MAP_W && mapY >= 0 && mapY < MAP_H) {
                    if (GAME_MAP[mapY][mapX] > 0) {
                        hit = true;
                        wallType = GAME_MAP[mapY][mapX];
                    }
                } else {
                    hit = true;
                    break;
                }
            }

            let perpDist;
            if (side === 0) {
                perpDist = (mapX - player.x + (1 - stepX) / 2) / cosA;
            } else {
                perpDist = (mapY - player.y + (1 - stepY) / 2) / sinA;
            }
            perpDist = Math.max(0.05, perpDist);
            this.zBuffer[r] = perpDist;

            let wallHit;
            if (side === 0) {
                wallHit = player.y + perpDist * sinA;
            } else {
                wallHit = player.x + perpDist * cosA;
            }
            wallHit -= Math.floor(wallHit);
            let texX = Math.floor(wallHit * S);
            texX = Math.max(0, Math.min(S - 1, texX));

            const projH = (1.0 / perpDist) * distProj;
            const top = (VH / 2) - (projH / 2);
            const colX = r * rayW;
            const colW = rayW + 0.5;

            // Dibujar columna texturizada desde el canvas en memoria
            const texCanvas = this.textures[wallType] || this.textures[1];
            ctx.drawImage(texCanvas, texX, 0, 1, S, colX, top, colW, projH);

            // Sombreado de cara lateral (Y) y niebla de distancia
            const fogFactor = Math.min(0.92, (perpDist / CONFIG.MAX_DEPTH));
            const sideDark = side === 1 ? 0.25 : 0.0;
            const darkAlpha = Math.min(0.95, fogFactor + sideDark);

            if (darkAlpha > 0.05) {
                ctx.fillStyle = `rgba(6, 8, 14, ${darkAlpha.toFixed(2)})`;
                ctx.fillRect(colX, top, colW, projH);
            }
        }
    }

    _renderSprites(player, enemies, projectiles, particles) {
        const ctx = this.ctx;
        const W = CONFIG.SCREEN_WIDTH;
        const VH = CONFIG.VIEWPORT_HEIGHT;
        const distProj = (W / 2) / Math.tan(CONFIG.FOV / 2);
        const rayW = W / CONFIG.NUM_RAYS;

        const renderables = [];

        for (const e of enemies) {
            if (e.alive) {
                const dist = Math.hypot(e.x - player.x, e.y - player.y);
                renderables.push({
                    type: "enemy", obj: e, x: e.x, y: e.y,
                    zOffset: (e.type === "volt" || e.type === "drone" || e.type === "nyx") ? Math.sin(e.hoverTimer) * 0.14 : 0,
                    dist: dist
                });
            }
        }

        for (const p of projectiles) {
            if (p.alive) {
                renderables.push({
                    type: "projectile", obj: p, x: p.x, y: p.y, zOffset: 0,
                    dist: Math.hypot(p.x - player.x, p.y - player.y)
                });
            }
        }

        for (const part of particles) {
            if (part.alive) {
                renderables.push({
                    type: "particle", obj: part, x: part.x, y: part.y, zOffset: 0,
                    dist: Math.hypot(part.x - player.x, part.y - player.y)
                });
            }
        }

        // Ordenamiento por profundidad descendente
        renderables.sort((a, b) => b.dist - a.dist);

        for (const item of renderables) {
            const dist = item.dist;
            if (dist < 0.2 || dist > CONFIG.MAX_DEPTH) continue;

            const dx = item.x - player.x;
            const dy = item.y - player.y;

            const invCos = Math.cos(-player.angle);
            const invSin = Math.sin(-player.angle);
            const transX = dx * invCos - dy * invSin;
            const transY = dx * invSin + dy * invCos;

            if (transX <= 0.05) continue;

            const screenX = (W / 2) + (transY / transX) * distProj;
            const scale = Math.min(VH * 2.2, (1.0 / transX) * distProj);
            const drawY = (VH / 2) - (scale * item.zOffset);

            if (item.type === "enemy") {
                const enemy = item.obj;
                const spriteCanvas = this.sprites[enemy.type] || this.sprites["xyron"] || this.sprites["drone"];
                let mult = 0.90;
                if (enemy.type === "brutus" || enemy.type === "baron") mult = 1.25;
                else if (enemy.type === "florax") mult = 1.10;
                else if (enemy.type === "xyron") mult = 0.95;
                else if (enemy.type === "nyx") mult = 0.88;
                else if (enemy.type === "volt" || enemy.type === "drone") mult = 0.80;
                const targetH = scale * mult;
                const lateralFactor = Math.abs(transY) / Math.max(0.4, transX);
                const widthRatio = Math.max(0.72, Math.min(1.0, 1.0 - (lateralFactor * 0.12)));
                const targetW = targetH * widthRatio;

                const left = screenX - targetW / 2;
                const top = drawY - targetH / 2;

                const startCol = Math.max(0, Math.floor(left / rayW));
                const endCol = Math.min(CONFIG.NUM_RAYS - 1, Math.floor((left + targetW) / rayW));

                for (let col = startCol; col <= endCol; col++) {
                    if (col >= 0 && col < CONFIG.NUM_RAYS && transX < this.zBuffer[col]) {
                        const colX = col * rayW;
                        let srcX = ((colX - left) / targetW) * spriteCanvas.width;
                        let srcW = (rayW / targetW) * spriteCanvas.width;

                        // Clamping estricto para evitar IndexSizeError en la API Canvas2D
                        if (srcX < 0) {
                            srcW += srcX;
                            srcX = 0;
                        }
                        if (srcX + srcW > spriteCanvas.width) {
                            srcW = spriteCanvas.width - srcX;
                        }

                        if (srcW > 0.5 && srcX >= 0 && spriteCanvas.width > 0 && spriteCanvas.height > 0) {
                            try {
                                ctx.drawImage(spriteCanvas, srcX, 0, srcW, spriteCanvas.height, colX, top, rayW + 0.5, targetH);
                            } catch (err) {}
                        }
                    }
                }

                // Destello blanco al recibir daño
                if (enemy.hitFlash > 0) {
                    const colIdx = Math.max(0, Math.min(CONFIG.NUM_RAYS - 1, Math.floor(screenX / rayW)));
                    if (transX < this.zBuffer[colIdx]) {
                        ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
                        ctx.fillRect(left, top, targetW, targetH);
                    }
                }

                // Barra de vida flotante
                if (enemy.hp < enemy.maxHp) {
                    const barW = Math.max(24, scale * 0.65);
                    const barH = Math.max(5, scale * 0.08);
                    const barX = screenX - barW / 2;
                    const barY = top - barH - 6;
                    const colIdx = Math.max(0, Math.min(CONFIG.NUM_RAYS - 1, Math.floor(screenX / rayW)));
                    if (transX < this.zBuffer[colIdx]) {
                        ctx.fillStyle = "#141414";
                        ctx.fillRect(barX, barY, barW, barH);
                        ctx.fillStyle = CONFIG.COLORS.RED;
                        ctx.fillRect(barX, barY, (enemy.hp / enemy.maxHp) * barW, barH);
                    }
                }
            } else if (item.type === "projectile") {
                const proj = item.obj;
                const pCanvas = this.sprites[proj.isPlayer ? "proj_player" : "proj_enemy"];
                const pSz = Math.max(12, Math.min(60, scale * 0.16));
                const colIdx = Math.max(0, Math.min(CONFIG.NUM_RAYS - 1, Math.floor(screenX / rayW)));
                if (transX < this.zBuffer[colIdx]) {
                    if (pCanvas && pCanvas.width > 0) {
                        try {
                            ctx.drawImage(pCanvas, screenX - pSz / 2, drawY - pSz / 2, pSz, pSz);
                        } catch (e) {}
                    } else {
                        // Respaldo visual orbe luminoso
                        ctx.fillStyle = proj.isPlayer ? CONFIG.COLORS.CYAN : CONFIG.COLORS.RED;
                        ctx.beginPath();
                        ctx.arc(screenX, drawY, pSz / 2, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.fillStyle = "#ffffff";
                        ctx.beginPath();
                        ctx.arc(screenX, drawY, pSz / 4, 0, Math.PI * 2);
                        ctx.fill();
                    }
                }
            } else if (item.type === "particle") {
                const part = item.obj;
                const partSz = Math.max(2, scale * 0.09 * (part.life / part.maxLife));
                const colIdx = Math.max(0, Math.min(CONFIG.NUM_RAYS - 1, Math.floor(screenX / rayW)));
                if (transX < this.zBuffer[colIdx]) {
                    ctx.fillStyle = part.color;
                    ctx.beginPath();
                    ctx.arc(screenX, drawY, partSz, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        }
    }
}
