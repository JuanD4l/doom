/**
 * CONTROLADOR PRINCIPAL DEL JUEGO WEB (Game Manager & Web Loop)
 */

class CyberDoomGame {
    constructor() {
        this.canvas = document.getElementById("gameCanvas");
        this.ctx = this.canvas.getContext("2d");

        this.titleScreen = document.getElementById("title-screen");
        this.pauseScreen = document.getElementById("pause-screen");
        this.gameOverScreen = document.getElementById("gameover-screen");
        this.playerNameInput = document.getElementById("playerName");
        this.backendStatus = document.getElementById("backendStatus");

        this.audio = new SoundSynthesizer();
        this.wallTextures = AssetGenerator.createWallTextures();
        this.weaponSprites = AssetGenerator.createWeaponSprites();
        this.enemySprites = AssetGenerator.createEnemySprites();

        this.renderer = new RaycasterRenderer(this.canvas, this.wallTextures, this.enemySprites);
        this.hud = new CyberHUD(this.ctx);

        this.state = "title"; // title, playing, paused, gameover
        this.highScore = this._loadLocalHighScore();
        this.lastTime = performance.now();

        this.input = {
            keys: {},
            mouseRelX: 0
        };

        this._setupEventListeners();
        this._checkBackendHealth();
        this._resetGame();

        // Iniciar loop de animación
        requestAnimationFrame((t) => this._loop(t));
    }

    _loadLocalHighScore() {
        return parseInt(localStorage.getItem("cyberdoom_highscore") || "0", 10);
    }

    _saveLocalHighScore() {
        localStorage.setItem("cyberdoom_highscore", String(this.highScore));
    }

    async _checkBackendHealth() {
        try {
            const res = await fetch(`${CONFIG.BACKEND_URL}/api/health`, { method: "GET" });
            if (res.ok) {
                const data = await res.json();
                this.backendStatus.textContent = `● Servidor Conectado: ${data.service || "Online"}`;
                this.backendStatus.style.color = CONFIG.COLORS.GREEN;
            } else {
                throw new Error("Offline");
            }
        } catch (e) {
            this.backendStatus.textContent = "○ Servidor Desconectado (Guardado Local Activo)";
            this.backendStatus.style.color = CONFIG.COLORS.YELLOW;
        }
    }

    _resetGame() {
        // Posición de inicio despejada y segura
        this.player = new Player(2.5, 2.5, 0.0);
        this.projectiles = [];
        this.enemies = [];
        this.particles = [];
        this.wave = 1;
        this.kills = 0;
        this.score = 0;
        this.waveBanner = 3.0;
        this._spawnWave();
    }

    _spawnWave() {
        this.enemies = [];
        this.spawnQueue = [];
        this.spawnTimer = 2.5;

        let initial = [];
        if (this.wave === 1) {
            // Oleada 1 (Dificultad Básica): Volt y Xyron
            this.maxSimultaneous = 2;
            initial = [["volt", 6.5, 2.5], ["xyron", 8.0, 3.5]];
            this.spawnQueue = ["volt", "xyron"];
            this.bannerText = `>> OLEADA #${this.wave}: PRIMER CONTACTO (VOLT / XYRON) <<`;
        } else if (this.wave === 2) {
            // Oleada 2 (Dificultad Media-Baja): Se introduce Florax
            this.maxSimultaneous = 3;
            initial = [["xyron", 6.5, 2.5], ["volt", 8.0, 3.5]];
            this.spawnQueue = ["florax", "xyron", "volt", "florax"];
            this.bannerText = `>> OLEADA #${this.wave}: ZONA MUTADA (FLORAX DETECTADA) <<`;
        } else if (this.wave === 3) {
            // Oleada 3 (Dificultad Media-Alta): Se introduce Nyx
            this.maxSimultaneous = 3;
            initial = [["xyron", 6.5, 2.5], ["florax", 5.5, 5.0]];
            this.spawnQueue = ["nyx", "volt", "nyx", "florax", "xyron"];
            this.bannerText = `>> OLEADA #${this.wave}: AMENAZA ESPECTRAL (NYX ACECHANDO) <<`;
        } else if (this.wave === 4) {
            // Oleada 4 (Dificultad Alta / Mini-Jefe): ¡Aparece el Gólem Tanque Brutus!
            this.maxSimultaneous = 4;
            initial = [["xyron", 6.5, 2.5], ["volt", 8.0, 3.5]];
            this.spawnQueue = ["brutus", "nyx", "florax", "xyron", "brutus"];
            this.bannerText = `>> ¡ALERTA JEFE OLEADA #${this.wave}: TITÁN BRUTUS! <<`;
        } else {
            // Oleadas 5+ (Supervivencia Pesadilla)
            this.maxSimultaneous = Math.min(5, 3 + Math.floor(this.wave / 2));
            initial = [["xyron", 6.5, 2.5], ["nyx", 8.0, 3.5]];
            const total = 4 + (this.wave * 2);
            const roster = ["xyron", "brutus", "nyx", "florax", "volt"];
            this.spawnQueue = [];
            for (let i = 0; i < total; i++) {
                this.spawnQueue.push(roster[Math.floor(Math.random() * roster.length)]);
            }
            this.bannerText = `>> ¡SUPERVIVENCIA CYBER-DOOM OLEADA #${this.wave}! <<`;
        }

        for (const [t, sx, sy] of initial) {
            this.enemies.push(new Enemy(sx, sy, t));
        }

        this.waveBanner = 2.8;
        this.audio.playWaveFanfare();
    }

    _setupEventListeners() {
        // Capturar todas las variantes de teclado
        window.addEventListener("keydown", (e) => {
            this.input.keys[e.code] = true;
            this.input.keys[e.key] = true;
            if (e.key) this.input.keys[e.key.toLowerCase()] = true;

            if (e.code === "Escape") {
                if (this.state === "playing") {
                    this.state = "paused";
                    if (document.exitPointerLock) document.exitPointerLock();
                    this.pauseScreen.classList.add("active");
                } else if (this.state === "paused") {
                    this._resumeGame();
                }
            } else if (e.code === "KeyR" && this.state === "gameover") {
                this._restartGame();
            } else if (e.code === "Space") {
                if (this.state === "playing") {
                    this._playerShoot();
                } else if (this.state === "title") {
                    this._startGame();
                }
            }
        });

        window.addEventListener("keyup", (e) => {
            this.input.keys[e.code] = false;
            this.input.keys[e.key] = false;
            if (e.key) this.input.keys[e.key.toLowerCase()] = false;
        });

        // Pointer Lock y Mouse Look
        this.canvas.addEventListener("click", () => {
            if (this.state === "playing") {
                try {
                    this.canvas.requestPointerLock();
                } catch (e) {}
            }
        });

        // IMPORTANTE: Si se pierde el pointer lock NO pausamos automáticamente,
        // permitimos seguir jugando con teclado y ratón libre sin interrupciones.
        window.addEventListener("mousemove", (e) => {
            if (this.state === "playing") {
                this.input.mouseRelX += e.movementX;
            }
        });

        window.addEventListener("mousedown", (e) => {
            if (e.button === 0 && this.state === "playing") {
                this._playerShoot();
            }
        });

        // Botones de la interfaz
        document.getElementById("btn-start").addEventListener("click", () => this._startGame());
        document.getElementById("btn-resume").addEventListener("click", () => this._resumeGame());
        document.getElementById("btn-restart").addEventListener("click", () => this._restartGame());
    }

    _startGame() {
        this.audio.init();
        this.state = "playing";
        this.titleScreen.classList.remove("active");
        this.pauseScreen.classList.remove("active");
        this.gameOverScreen.classList.remove("active");
        this._resetGame();
        try {
            this.canvas.requestPointerLock();
        } catch (e) {}
    }

    _resumeGame() {
        this.state = "playing";
        this.pauseScreen.classList.remove("active");
        try {
            this.canvas.requestPointerLock();
        } catch (e) {}
    }

    _restartGame() {
        this.state = "playing";
        this.gameOverScreen.classList.remove("active");
        this._resetGame();
        try {
            this.canvas.requestPointerLock();
        } catch (e) {}
    }

    _playerShoot() {
        if (this.player.cooldown <= 0) {
            this.player.cooldown = 0.30;
            this.player.screenShake = 0.16;
            this.audio.playShotgun();

            // Disparo en abanico de 5 perdigones de plasma
            const spreads = [-0.07, -0.035, 0, 0.035, 0.07];
            spreads.forEach((s) => {
                this.projectiles.push(new Projectile(this.player.x, this.player.y, this.player.angle + s, 14.0, true, 18));
            });

            const fx = this.player.x + Math.cos(this.player.angle) * 0.45;
            const fy = this.player.y + Math.sin(this.player.angle) * 0.45;
            for (let i = 0; i < 8; i++) {
                this.particles.push(new Particle(fx, fy, CONFIG.COLORS.CYAN, 5, 3.2, 0.18));
            }
        }
    }

    _loop(timestamp) {
        let dt = (timestamp - this.lastTime) / 1000;
        this.lastTime = timestamp;
        dt = Math.min(0.05, dt);

        if (this.state === "playing") {
            this._update(dt);
            this._draw(dt);
        }

        // Limpiar delta de ratón consumido
        this.input.mouseRelX = 0;

        requestAnimationFrame((t) => this._loop(t));
    }

    _update(dt) {
        this.player.update(dt, this.input, this.input.mouseRelX);

        // Actualizar proyectiles
        for (let i = this.projectiles.length - 1; i >= 0; i--) {
            const p = this.projectiles[i];
            p.update(dt);
            if (!p.alive) {
                this.projectiles.splice(i, 1);
                continue;
            }

            if (!p.isPlayer) {
                // Impacto en jugador
                if (Math.hypot(p.x - this.player.x, p.y - this.player.y) < this.player.radius + 0.22) {
                    p.alive = false;
                    this.player.takeDamage(p.damage, this.audio);
                    for (let k = 0; k < 8; k++) {
                        this.particles.push(new Particle(this.player.x, this.player.y, CONFIG.COLORS.RED, 5, 3.5, 0.22));
                    }
                    if (this.player.health <= 0) {
                        this._handleGameOver();
                    }
                }
            } else {
                // Impacto en enemigos
                for (const e of this.enemies) {
                    if (e.alive && Math.hypot(p.x - e.x, p.y - e.y) < e.radius + 0.28) {
                        p.alive = false;
                        e.takeDamage(p.damage, this.audio);
                        this.player.hitmarkerTime = 0.15;
                        this.audio.playHitmarker();

                        for (let k = 0; k < 6; k++) {
                            this.particles.push(new Particle(e.x, e.y, CONFIG.COLORS.MAGENTA, 5, 3.8, 0.25));
                        }

                        if (!e.alive) {
                            this.kills++;
                            this.score += e.scoreValue;
                            this.player.shield = Math.min(this.player.maxShield, this.player.shield + 12);
                            for (let k = 0; k < 22; k++) {
                                this.particles.push(new Particle(e.x, e.y, CONFIG.COLORS.CYAN, 6, 6.0, 0.45));
                            }
                        }
                        break;
                    }
                }
            }
        }

        // Manejo de refuerzos escalonados
        let aliveCount = this.enemies.filter(e => e.alive).length;
        if (this.spawnQueue && this.spawnQueue.length > 0 && aliveCount < this.maxSimultaneous) {
            this.spawnTimer -= dt;
            if (this.spawnTimer <= 0 || aliveCount < 2) {
                this.spawnTimer = 3.2 + Math.random() * 1.4;
                const nextType = this.spawnQueue.shift();

                const validSpawns = [];
                for (let y = 1; y < MAP_H - 1; y++) {
                    for (let x = 1; x < MAP_W - 1; x++) {
                        if (GAME_MAP[y][x] === 0) {
                            const d = Math.hypot(x + 0.5 - this.player.x, y + 0.5 - this.player.y);
                            if (d >= 4.0 && d <= 11.0) {
                                validSpawns.push({ x: x + 0.5, y: y + 0.5 });
                            }
                        }
                    }
                }

                if (validSpawns.length > 0) {
                    const s = validSpawns[Math.floor(Math.random() * validSpawns.length)];
                    this.enemies.push(new Enemy(s.x, s.y, nextType));
                    this.audio.playLaser();
                    const pCol = nextType === "brutus" ? CONFIG.COLORS.ORANGE : (nextType === "nyx" ? CONFIG.COLORS.MAGENTA : CONFIG.COLORS.CYAN);
                    for (let k = 0; k < 15; k++) {
                        this.particles.push(new Particle(s.x, s.y, pCol, 6, 4.0, 0.35));
                    }
                }
            }
        }

        // Actualizar enemigos
        for (const e of this.enemies) {
            if (e.alive) {
                e.update(dt, this.player, this.projectiles, this.audio);
            }
        }

        // Actualizar partículas
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const part = this.particles[i];
            part.update(dt);
            if (!part.alive) this.particles.splice(i, 1);
        }

        // Comprobar fin de oleada (requiere que no haya enemigos activos NI en cola)
        aliveCount = this.enemies.filter(e => e.alive).length;
        if (aliveCount === 0 && (!this.spawnQueue || this.spawnQueue.length === 0)) {
            this.wave++;
            this.score += 600;
            this.player.health = Math.min(this.player.maxHealth, this.player.health + 30);
            this._spawnWave();
        }

        if (this.waveBanner > 0) {
            this.waveBanner = Math.max(0, this.waveBanner - dt);
        }
    }

    _draw(dt) {
        // 1. Renderizado 3D de escena
        this.renderer.render(this.player, this.enemies, this.projectiles, this.particles);

        // 2. Arma en primera persona
        const weaponImg = this.weaponSprites[this.player.weaponFrame];
        const bobX = Math.cos(this.player.walkBob) * 12;
        const bobY = Math.abs(Math.sin(this.player.walkBob)) * 16;
        const shakeX = (Math.random() * 2 - 1) * 8 * this.player.screenShake;
        const shakeY = (Math.random() * 2 - 1) * 8 * this.player.screenShake;

        const wx = (CONFIG.SCREEN_WIDTH / 2) - (weaponImg.width / 2) + bobX + shakeX;
        const wy = CONFIG.VIEWPORT_HEIGHT - weaponImg.height + bobY + shakeY;
        this.ctx.drawImage(weaponImg, wx, wy);

        // 3. Retícula y Hitmarker
        const cx = CONFIG.SCREEN_WIDTH / 2;
        const cy = CONFIG.VIEWPORT_HEIGHT / 2;
        const retColor = this.player.cooldown > 0.1 ? CONFIG.COLORS.RED : CONFIG.COLORS.CYAN;

        this.ctx.strokeStyle = retColor;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, 5, 0, Math.PI * 2);
        this.ctx.moveTo(cx - 15, cy); this.ctx.lineTo(cx - 6, cy);
        this.ctx.moveTo(cx + 6, cy); this.ctx.lineTo(cx + 15, cy);
        this.ctx.moveTo(cx, cy - 15); this.ctx.lineTo(cx, cy - 6);
        this.ctx.moveTo(cx, cy + 6); this.ctx.lineTo(cx, cy + 15);
        this.ctx.stroke();

        if (this.player.hitmarkerTime > 0) {
            const hsz = 9;
            this.ctx.strokeStyle = CONFIG.COLORS.RED;
            this.ctx.lineWidth = 3;
            this.ctx.beginPath();
            this.ctx.moveTo(cx - hsz, cy - hsz); this.ctx.lineTo(cx - 4, cy - 4);
            this.ctx.moveTo(cx + 4, cy + 4); this.ctx.lineTo(cx + hsz, cy + hsz);
            this.ctx.moveTo(cx + hsz, cy - hsz); this.ctx.lineTo(cx + 4, cy - 4);
            this.ctx.moveTo(cx - hsz, cy + hsz); this.ctx.lineTo(cx - 4, cy + 4);
            this.ctx.stroke();
        }

        // 4. Destello rojo por daño
        if (this.player.hurtFlash > 0) {
            this.ctx.fillStyle = `rgba(255, 0, 40, ${(this.player.hurtFlash * 0.6).toFixed(2)})`;
            this.ctx.fillRect(0, 0, CONFIG.SCREEN_WIDTH, CONFIG.VIEWPORT_HEIGHT);
        }

        // 5. Banner de oleada
        if (this.waveBanner > 0) {
            this.ctx.fillStyle = "rgba(10, 15, 25, 0.88)";
            this.ctx.fillRect(CONFIG.SCREEN_WIDTH / 2 - 240, 50, 480, 55);
            this.ctx.strokeStyle = CONFIG.COLORS.YELLOW;
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(CONFIG.SCREEN_WIDTH / 2 - 240, 50, 480, 55);

            this.ctx.fillStyle = CONFIG.COLORS.YELLOW;
            this.ctx.font = "bold 24px 'Orbitron', sans-serif";
            this.ctx.textAlign = "center";
            this.ctx.fillText(`>> ¡OLEADA #${this.wave} DESPLEGADA! <<`, CONFIG.SCREEN_WIDTH / 2, 86);
            this.ctx.textAlign = "start";
        }

        // 6. Consola HUD con información de enemigos en el radar
        this.hud.draw(this.player, this.wave, this.kills, this.score, this.highScore, this.enemies, dt);
    }

    _handleGameOver() {
        this.state = "gameover";
        if (document.exitPointerLock) document.exitPointerLock();

        if (this.score > this.highScore) {
            this.highScore = this.score;
            this._saveLocalHighScore();
        }

        document.getElementById("go-wave").textContent = String(this.wave).padStart(2, '0');
        document.getElementById("go-kills").textContent = String(this.kills).padStart(2, '0');
        document.getElementById("go-score").textContent = String(this.score).padStart(6, '0');
        document.getElementById("go-highscore").textContent = String(this.highScore).padStart(6, '0');

        this.gameOverScreen.classList.add("active");
        this._submitScoreToBackend();
    }

    async _submitScoreToBackend() {
        const playerName = (this.playerNameInput.value || "CYBER_MARINE").trim().toUpperCase();
        const payload = {
            player_name: playerName,
            score: this.score,
            wave: this.wave,
            kills: this.kills
        };

        try {
            await fetch(`${CONFIG.BACKEND_URL}/api/scores`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
        } catch (e) {
            console.warn("Backend offline. Guardando localmente:", e);
        }

        this._fetchLeaderboard();
    }

    async _fetchLeaderboard() {
        const listEl = document.getElementById("leaderboard-list");
        try {
            const res = await fetch(`${CONFIG.BACKEND_URL}/api/leaderboard`);
            if (res.ok) {
                const data = await res.json();
                const scores = data.data || [];
                if (scores.length > 0) {
                    listEl.innerHTML = scores.map((s, idx) => `
                        <li>
                            <span>${idx + 1}. ${s.player_name} (Oleada ${s.wave})</span>
                            <b style="color: ${CONFIG.COLORS.YELLOW}">${s.score} PTS</b>
                        </li>
                    `).join("");
                    return;
                }
            }
        } catch (e) {}

        listEl.innerHTML = `
            <li><span>1. ${this.playerNameInput.value}</span> <b style="color: ${CONFIG.COLORS.YELLOW}">${this.score} PTS</b></li>
            <li><span>2. LOCAL_RECORD</span> <b style="color: ${CONFIG.COLORS.YELLOW}">${this.highScore} PTS</b></li>
        `;
    }
}

// Inicializar juego al cargar la página
window.addEventListener("DOMContentLoaded", () => {
    window.game = new CyberDoomGame();
});
