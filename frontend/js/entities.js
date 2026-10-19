/**
 * ENTIDADES DE DOMINIO: PLAYER, ENEMY, PROJECTILE, PARTICLE
 */

class Player {
    constructor(x = 2.5, y = 2.5, angle = 0.0) {
        this.x = x;
        this.y = y;
        this.angle = angle;
        this.speed = 4.2;
        this.radius = 0.22; // Radio de colisión ajustado para evitar cualquier atasco
        this.mouseSensitivity = 0.0028;

        this.maxHealth = 100;
        this.health = 100;
        this.maxShield = 100;
        this.shield = 50;

        this.cooldown = 0;
        this.weaponFrame = 0;
        this.walkBob = 0;
        this.hurtFlash = 0;
        this.screenShake = 0;
        this.hitmarkerTime = 0;
    }

    takeDamage(amount, audio) {
        if (this.shield > 0) {
            const absorbed = Math.min(this.shield, amount);
            this.shield -= absorbed;
            amount -= absorbed;
        }
        this.health = Math.max(0, this.health - amount);
        this.hurtFlash = 0.45;
        this.screenShake = 0.25;
        audio.playHurt();
    }

    update(dt, input, mouseRelX) {
        // Enfriamiento de arma
        if (this.cooldown > 0) {
            this.cooldown -= dt;
            if (this.cooldown > 0.22) {
                this.weaponFrame = 1; // Fogonazo
            } else if (this.cooldown > 0.10) {
                this.weaponFrame = 2; // Retroceso
            } else {
                this.weaponFrame = 0; // Reposo
            }
        } else {
            this.weaponFrame = 0;
        }

        if (this.hurtFlash > 0) this.hurtFlash = Math.max(0, this.hurtFlash - dt * 2.2);
        if (this.screenShake > 0) this.screenShake = Math.max(0, this.screenShake - dt * 2.5);
        if (this.hitmarkerTime > 0) this.hitmarkerTime = Math.max(0, this.hitmarkerTime - dt * 5.0);

        // Giro con ratón (Mouse-Look)
        if (mouseRelX) {
            this.angle += mouseRelX * this.mouseSensitivity;
        }

        const k = input.keys;

        // Giro con teclas de flecha y Q/E
        if (k["ArrowLeft"] || k["KeyQ"] || k["q"] || k["Q"]) this.angle -= 3.5 * dt;
        if (k["ArrowRight"] || k["KeyE"] || k["e"] || k["E"]) this.angle += 3.5 * dt;

        this.angle = (this.angle + Math.PI * 2) % (Math.PI * 2);

        // Desplazamiento WASD y flechas (soporta códigos de tecla y caracteres)
        const cos = Math.cos(this.angle);
        const sin = Math.sin(this.angle);
        let dx = 0, dy = 0;

        const isUp = k["KeyW"] || k["w"] || k["W"] || k["ArrowUp"];
        const isDown = k["KeyS"] || k["s"] || k["S"] || k["ArrowDown"];
        const isLeft = k["KeyA"] || k["a"] || k["A"];
        const isRight = k["KeyD"] || k["d"] || k["D"];

        if (isUp) { dx += cos; dy += sin; }
        if (isDown) { dx -= cos; dy -= sin; }
        if (isLeft) { dx += sin; dy -= cos; }
        if (isRight) { dx -= sin; dy += cos; }

        const len = Math.hypot(dx, dy);
        if (len > 0.001) {
            let spd = this.speed * dt;
            const isSprint = k["ShiftLeft"] || k["ShiftRight"] || k["Shift"];
            if (isSprint) spd *= 1.45;

            dx = (dx / len) * spd;
            dy = (dy / len) * spd;

            // Deslizamiento independiente en X e Y
            if (!this._checkCollision(this.x + dx, this.y)) {
                this.x += dx;
            }
            if (!this._checkCollision(this.x, this.y + dy)) {
                this.y += dy;
            }

            this.walkBob += dt * 11.0;
        } else {
            this.walkBob = 0;
        }
    }

    _checkCollision(x, y) {
        const r = this.radius;
        // Comprobar 4 esquinas del círculo de colisión
        return isWall(x - r, y - r) || isWall(x + r, y - r) ||
               isWall(x - r, y + r) || isWall(x + r, y + r);
    }
}

class Projectile {
    constructor(x, y, angle, speed, isPlayer = true, damage = 22) {
        this.x = x;
        this.y = y;
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.isPlayer = isPlayer;
        this.damage = damage;
        this.alive = true;
        this.lifeTime = 3.0;
    }

    update(dt) {
        this.lifeTime -= dt;
        if (this.lifeTime <= 0) {
            this.alive = false;
            return;
        }
        this.x += this.vx * dt;
        this.y += this.vy * dt;
        if (isWall(this.x, this.y)) {
            this.alive = false;
        }
    }
}

class Enemy {
    constructor(x, y, type = "drone") {
        this.x = x;
        this.y = y;
        this.type = type;
        this.alive = true;
        this.hitFlash = 0;
        this.attackTimer = 0.5 + Math.random() * 1.0;
        this.hoverTimer = Math.random() * 6.28;

        const specs = {
            "xyron":  { hp: 120, speed: 2.1, attackCooldown: 2.2, projSpeed: 7.0, damage: 12, radius: 0.42, scoreValue: 100, critMult: 1.5 },
            "brutus": { hp: 240, speed: 1.3, attackCooldown: 2.8, projSpeed: 4.0, damage: 45, radius: 0.60, scoreValue: 180, critMult: 2.0 },
            "nyx":    { hp: 90,  speed: 3.0, attackCooldown: 3.5, projSpeed: 0.0, damage: 55, radius: 0.38, scoreValue: 140, critMult: 2.0 },
            "florax": { hp: 150, speed: 1.2, attackCooldown: 3.0, projSpeed: 5.0, damage: 20, radius: 0.58, scoreValue: 120, critMult: 1.8 },
            "volt":   { hp: 110, speed: 2.9, attackCooldown: 2.0, projSpeed: 8.0, damage: 22, radius: 0.35, scoreValue: 130, critMult: 1.5 },
            "drone":  { hp: 35,  speed: 2.4, attackCooldown: 1.6, projSpeed: 6.0, damage: 10, radius: 0.35, scoreValue: 100, critMult: 1.5 },
            "imp":    { hp: 70,  speed: 1.9, attackCooldown: 2.0, projSpeed: 5.2, damage: 22, radius: 0.40, scoreValue: 250, critMult: 1.5 },
            "baron":  { hp: 190, speed: 1.25, attackCooldown: 2.4, projSpeed: 7.0, damage: 38, radius: 0.55, scoreValue: 600, critMult: 2.0 }
        };
        const s = specs[type] || specs["xyron"];
        this.hp = s.hp;
        this.maxHp = s.hp;
        this.speed = s.speed;
        this.attackCooldown = s.attackCooldown;
        this.projSpeed = s.projSpeed;
        this.damage = s.damage;
        this.radius = s.radius;
        this.scoreValue = s.scoreValue;
        this.critMultiplier = s.critMult;
    }

    update(dt, player, projectiles, audio) {
        if (!this.alive) return;
        if (this.hitFlash > 0) this.hitFlash = Math.max(0, this.hitFlash - dt * 3.5);

        this.hoverTimer += dt * 3.5;
        const dx = player.x - this.x;
        const dy = player.y - this.y;
        const dist = Math.hypot(dx, dy);
        const angle = Math.atan2(dy, dx);
        const hasLOS = checkLOS(this.x, this.y, player.x, player.y, dist);

        // Movimiento hacia el jugador
        if (dist > 0.8) {
            const moveSpd = this.speed * dt;
            let mx, my;
            if (this.type === "drone" && dist < 3.8 && hasLOS) {
                const strafeAng = angle + Math.PI / 2;
                mx = Math.cos(strafeAng) * moveSpd * 0.85;
                my = Math.sin(strafeAng) * moveSpd * 0.85;
            } else {
                mx = Math.cos(angle) * moveSpd;
                my = Math.sin(angle) * moveSpd;
            }

            if (!isWall(this.x + mx, this.y)) this.x += mx;
            if (!isWall(this.x, this.y + my)) this.y += my;
        }

        this.attackTimer -= dt;
        if (this.attackTimer <= 0 && hasLOS && dist < 12.0) {
            this.attackTimer = this.attackCooldown + (Math.random() * 0.5 - 0.25);
            projectiles.push(new Projectile(this.x, this.y, angle, this.projSpeed, false, this.damage));
            audio.playLaser();
        }
    }

    takeDamage(amount, audio) {
        this.hp -= amount;
        this.hitFlash = 0.28;
        if (this.hp <= 0) {
            this.alive = false;
            audio.playExplosion();
        }
    }
}

class Particle {
    constructor(x, y, color, size, speed, life) {
        this.x = x;
        this.y = y;
        const ang = Math.random() * Math.PI * 2;
        this.vx = Math.cos(ang) * speed;
        this.vy = Math.sin(ang) * speed;
        this.color = color;
        this.size = size;
        this.life = life;
        this.maxLife = life;
    }

    update(dt) {
        this.life -= dt;
        this.x += this.vx * dt;
        this.y += this.vy * dt;
    }

    get alive() {
        return this.life > 0;
    }
}
