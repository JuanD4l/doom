/**
 * GENERADOR PROCEDURAL DE TEXTURAS Y SPRITES PARA CANVAS
 */
class AssetGenerator {
    static createWallTextures() {
        const S = CONFIG.TEX_SIZE;
        const textures = {};

        // 1. CYBER-MATRIX (Placa con rieles neón cian)
        const c1 = document.createElement("canvas");
        c1.width = S; c1.height = S;
        const ctx1 = c1.getContext("2d");
        ctx1.fillStyle = "#161c28";
        ctx1.fillRect(0, 0, S, S);
        ctx1.strokeStyle = "#232d41";
        ctx1.lineWidth = 2;
        ctx1.strokeRect(2, 2, S - 4, S - 4);
        ctx1.strokeStyle = CONFIG.COLORS.CYAN;
        ctx1.lineWidth = 3;
        ctx1.beginPath();
        ctx1.moveTo(20, 4); ctx1.lineTo(20, 60);
        ctx1.moveTo(44, 4); ctx1.lineTo(44, 60);
        ctx1.stroke();
        ctx1.strokeStyle = "#ffffff";
        ctx1.lineWidth = 1;
        ctx1.beginPath();
        ctx1.moveTo(20, 8); ctx1.lineTo(20, 56);
        ctx1.moveTo(44, 8); ctx1.lineTo(44, 56);
        ctx1.stroke();
        textures[1] = c1;

        // 2. CYBER-CORE (Núcleo y pistas magenta)
        const c2 = document.createElement("canvas");
        c2.width = S; c2.height = S;
        const ctx2 = c2.getContext("2d");
        ctx2.fillStyle = "#1e0e24";
        ctx2.fillRect(0, 0, S, S);
        ctx2.fillStyle = "#2d1437";
        ctx2.fillRect(6, 6, S - 12, S - 12);
        ctx2.strokeStyle = CONFIG.COLORS.MAGENTA;
        ctx2.lineWidth = 2;
        ctx2.beginPath();
        ctx2.moveTo(12, 12); ctx2.lineTo(24, 24); ctx2.lineTo(24, 44); ctx2.lineTo(40, 44);
        ctx2.moveTo(52, 12); ctx2.lineTo(40, 24); ctx2.lineTo(40, 36);
        ctx2.stroke();
        ctx2.fillStyle = CONFIG.COLORS.CYAN;
        ctx2.fillRect(26, 26, 12, 12);
        ctx2.fillStyle = "#ffffff";
        ctx2.fillRect(29, 29, 6, 6);
        textures[2] = c2;

        // 3. HAZARD (Franjas industriales de peligro)
        const c3 = document.createElement("canvas");
        c3.width = S; c3.height = S;
        const ctx3 = c3.getContext("2d");
        ctx3.fillStyle = "#202228";
        ctx3.fillRect(0, 0, S, S);
        ctx3.fillStyle = "#141416";
        ctx3.fillRect(0, 18, S, 28);
        ctx3.fillStyle = CONFIG.COLORS.YELLOW;
        for (let x = -20; x < 80; x += 12) {
            ctx3.beginPath();
            ctx3.moveTo(x, 18);
            ctx3.lineTo(x + 8, 18);
            ctx3.lineTo(x - 6, 46);
            ctx3.lineTo(x - 14, 46);
            ctx3.fill();
        }
        ctx3.strokeStyle = "#788291";
        ctx3.lineWidth = 3;
        ctx3.beginPath();
        ctx3.moveTo(4, 54); ctx3.lineTo(60, 54);
        ctx3.stroke();
        textures[3] = c3;

        // 4. DEMONIC (Biometal corrupto con cráneo cyber)
        const c4 = document.createElement("canvas");
        c4.width = S; c4.height = S;
        const ctx4 = c4.getContext("2d");
        ctx4.fillStyle = "#261016";
        ctx4.fillRect(0, 0, S, S);
        ctx4.fillStyle = "#3c1923";
        ctx4.beginPath();
        ctx4.moveTo(22, 18); ctx4.lineTo(42, 18); ctx4.lineTo(46, 36); ctx4.lineTo(32, 48); ctx4.lineTo(18, 36);
        ctx4.fill();
        ctx4.fillStyle = CONFIG.COLORS.RED;
        ctx4.beginPath();
        ctx4.arc(26, 26, 4, 0, Math.PI * 2);
        ctx4.arc(38, 26, 4, 0, Math.PI * 2);
        ctx4.fill();
        ctx4.fillStyle = "#ffffff";
        ctx4.beginPath();
        ctx4.arc(26, 26, 2, 0, Math.PI * 2);
        ctx4.arc(38, 26, 2, 0, Math.PI * 2);
        ctx4.fill();
        textures[4] = c4;

        return textures;
    }

    static createWeaponSprites() {
        const frames = [];
        const w = 320, h = 260;

        // Frame 0: Reposo
        const c0 = document.createElement("canvas");
        c0.width = w; c0.height = h;
        const ctx0 = c0.getContext("2d");
        this._drawHands(ctx0, 0);
        this._drawGun(ctx0, 0, false);
        frames.push(c0);

        // Frame 1: Fogonazo y retroceso
        const c1 = document.createElement("canvas");
        c1.width = w; c1.height = h;
        const ctx1 = c1.getContext("2d");
        this._drawHands(ctx1, 24);
        this._drawGun(ctx1, 24, true);
        frames.push(c1);

        // Frame 2: Recuperación
        const c2 = document.createElement("canvas");
        c2.width = w; c2.height = h;
        const ctx2 = c2.getContext("2d");
        this._drawHands(ctx2, 12);
        this._drawGun(ctx2, 12, false, true);
        frames.push(c2);

        return frames;
    }

    static _drawHands(ctx, rec) {
        ctx.fillStyle = "#141822";
        ctx.beginPath();
        ctx.moveTo(40, 260); ctx.lineTo(70, 190 + rec); ctx.lineTo(105, 190 + rec); ctx.lineTo(90, 260);
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(280, 260); ctx.lineTo(250, 190 + rec); ctx.lineTo(215, 190 + rec); ctx.lineTo(230, 260);
        ctx.fill();
        ctx.strokeStyle = CONFIG.COLORS.CYAN;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(70, 195 + rec); ctx.lineTo(105, 195 + rec);
        ctx.moveTo(250, 195 + rec); ctx.lineTo(215, 195 + rec);
        ctx.stroke();
    }

    static _drawGun(ctx, rec, isFiring, isHot = false) {
        // Chasis del cañón
        ctx.fillStyle = CONFIG.COLORS.DARK_METAL;
        ctx.beginPath();
        ctx.moveTo(115, 260); ctx.lineTo(135, 75 + rec); ctx.lineTo(185, 75 + rec); ctx.lineTo(205, 260);
        ctx.fill();
        ctx.fillStyle = "#10141e";
        ctx.fillRect(138, 65 + rec, 44, 180);

        // Cañones dobles
        ctx.fillStyle = "#283041";
        ctx.beginPath();
        ctx.arc(148, 68 + rec, 12, 0, Math.PI * 2);
        ctx.arc(172, 68 + rec, 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#0a0c10";
        ctx.beginPath();
        ctx.arc(148, 68 + rec, 8, 0, Math.PI * 2);
        ctx.arc(172, 68 + rec, 8, 0, Math.PI * 2);
        ctx.fill();

        // Rieles de energía neón
        ctx.strokeStyle = CONFIG.COLORS.CYAN;
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(136, 80 + rec); ctx.lineTo(120, 255);
        ctx.moveTo(184, 80 + rec); ctx.lineTo(200, 255);
        ctx.stroke();

        if (isFiring) {
            // Fogonazo masivo de plasma
            ctx.fillStyle = CONFIG.COLORS.CYAN;
            ctx.beginPath();
            ctx.arc(160, 55 + rec, 60, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(160, 55 + rec, 32, 0, Math.PI * 2);
            ctx.fill();
            // Rayos
            ctx.strokeStyle = CONFIG.COLORS.MAGENTA;
            ctx.lineWidth = 4;
            for (let deg = 0; deg < 360; deg += 30) {
                const rad = (deg * Math.PI) / 180;
                ctx.beginPath();
                ctx.moveTo(160, 55 + rec);
                ctx.lineTo(160 + Math.cos(rad) * 85, 55 + rec + Math.sin(rad) * 60);
                ctx.stroke();
            }
        } else if (isHot) {
            ctx.fillStyle = CONFIG.COLORS.ORANGE;
            ctx.beginPath();
            ctx.arc(148, 68 + rec, 7, 0, Math.PI * 2);
            ctx.arc(172, 68 + rec, 7, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    static createEnemySprites() {
        const sprites = {};
        const sz = 128;

        // 1. XYRON (Tirador Alienígena Turquesa)
        const cXyron = document.createElement("canvas");
        cXyron.width = sz; cXyron.height = sz;
        const ctxX = cXyron.getContext("2d");
        // Cabeza alienígena turquesa
        ctxX.fillStyle = "#20d0e0";
        ctxX.beginPath(); ctxX.ellipse(64, 38, 38, 22, 0, 0, Math.PI * 2); ctxX.fill();
        ctxX.strokeStyle = "#1098a8"; ctxX.lineWidth = 2; ctxX.stroke();
        // Ojos negros grandes
        ctxX.fillStyle = "#0c0e14";
        ctxX.beginPath(); ctxX.ellipse(50, 38, 10, 8, -0.2, 0, Math.PI * 2); ctxX.fill();
        ctxX.beginPath(); ctxX.ellipse(78, 38, 10, 8, 0.2, 0, Math.PI * 2); ctxX.fill();
        ctxX.fillStyle = "#fff";
        ctxX.beginPath(); ctxX.arc(52, 36, 3, 0, Math.PI * 2); ctxX.arc(80, 36, 3, 0, Math.PI * 2); ctxX.fill();
        // Armadura oscura y rifle
        ctxX.fillStyle = "#161c28";
        ctxX.fillRect(48, 60, 32, 40);
        ctxX.strokeStyle = CONFIG.COLORS.CYAN; ctxX.lineWidth = 2; ctxX.strokeRect(48, 60, 32, 40);
        ctxX.fillStyle = "#1e2434";
        ctxX.fillRect(26, 75, 76, 12);
        ctxX.fillStyle = CONFIG.COLORS.CYAN;
        ctxX.fillRect(20, 78, 10, 6);
        // Piernas
        ctxX.strokeStyle = "#20d0e0"; ctxX.lineWidth = 5;
        ctxX.beginPath(); ctxX.moveTo(54, 100); ctxX.lineTo(46, 124); ctxX.moveTo(74, 100); ctxX.lineTo(82, 124); ctxX.stroke();
        sprites["xyron"] = cXyron;

        // 2. BRUTUS (Gólem de Chatarra Tanque)
        const cBrutus = document.createElement("canvas");
        cBrutus.width = sz; cBrutus.height = sz;
        const ctxB = cBrutus.getContext("2d");
        ctxB.fillStyle = "#65402c";
        ctxB.fillRect(28, 48, 72, 54);
        ctxB.strokeStyle = "#8c5638"; ctxB.lineWidth = 3; ctxB.strokeRect(28, 48, 72, 54);
        // Brazos gigantes
        ctxB.fillStyle = "#3c404c";
        ctxB.fillRect(8, 52, 22, 60); ctxB.fillRect(98, 52, 22, 60);
        // Núcleo naranja brillante
        ctxB.fillStyle = CONFIG.COLORS.ORANGE;
        ctxB.beginPath(); ctxB.arc(64, 75, 14, 0, Math.PI * 2); ctxB.fill();
        ctxB.fillStyle = CONFIG.COLORS.YELLOW;
        ctxB.beginPath(); ctxB.arc(64, 75, 7, 0, Math.PI * 2); ctxB.fill();
        // Cabeza con visor
        ctxB.fillStyle = "#22252e";
        ctxB.fillRect(50, 22, 28, 26);
        ctxB.fillStyle = CONFIG.COLORS.ORANGE;
        ctxB.fillRect(54, 30, 20, 8);
        sprites["brutus"] = cBrutus;

        // 3. NYX (Sombra Espectral)
        const cNyx = document.createElement("canvas");
        cNyx.width = sz; cNyx.height = sz;
        const ctxN = cNyx.getContext("2d");
        ctxN.fillStyle = "#4a156e";
        ctxN.beginPath();
        ctxN.moveTo(64, 18); ctxN.lineTo(88, 50); ctxN.lineTo(92, 105); ctxN.lineTo(64, 95); ctxN.lineTo(36, 105); ctxN.lineTo(40, 50);
        ctxN.fill();
        ctxN.strokeStyle = CONFIG.COLORS.MAGENTA; ctxN.lineWidth = 2; ctxN.stroke();
        // Ojos violetas
        ctxN.fillStyle = CONFIG.COLORS.MAGENTA;
        ctxN.beginPath(); ctxN.arc(56, 36, 4, 0, Math.PI * 2); ctxN.arc(72, 36, 4, 0, Math.PI * 2); ctxN.fill();
        ctxN.fillStyle = "#fff";
        ctxN.beginPath(); ctxN.arc(57, 36, 1.5, 0, Math.PI * 2); ctxN.arc(73, 36, 1.5, 0, Math.PI * 2); ctxN.fill();
        // Dagas gemelas neón
        ctxN.fillStyle = CONFIG.COLORS.MAGENTA;
        ctxN.beginPath(); ctxN.moveTo(24, 70); ctxN.lineTo(14, 115); ctxN.lineTo(26, 95); ctxN.fill();
        ctxN.beginPath(); ctxN.moveTo(104, 70); ctxN.lineTo(114, 115); ctxN.lineTo(102, 95); ctxN.fill();
        sprites["nyx"] = cNyx;

        // 4. FLORAX (Planta Mutante Controladora)
        const cFlorax = document.createElement("canvas");
        cFlorax.width = sz; cFlorax.height = sz;
        const ctxF = cFlorax.getContext("2d");
        // Raíces y tallo
        ctxF.strokeStyle = "#1a5e26"; ctxF.lineWidth = 8;
        ctxF.beginPath();
        ctxF.moveTo(35, 124); ctxF.lineTo(50, 80); ctxF.lineTo(64, 60); ctxF.lineTo(78, 80); ctxF.lineTo(93, 124);
        ctxF.stroke();
        // Boca carnívora
        ctxF.fillStyle = "#8a141b";
        ctxF.beginPath(); ctxF.ellipse(64, 68, 30, 18, 0, 0, Math.PI * 2); ctxF.fill();
        ctxF.fillStyle = "#fff";
        for (let tx = 44; tx <= 84; tx += 8) {
            ctxF.fillRect(tx, 62, 4, 5);
            ctxF.fillRect(tx, 71, 4, 5);
        }
        // Flor naranja superior
        ctxF.fillStyle = CONFIG.COLORS.ORANGE;
        ctxF.beginPath(); ctxF.arc(64, 30, 20, 0, Math.PI * 2); ctxF.fill();
        ctxF.fillStyle = CONFIG.COLORS.YELLOW;
        ctxF.beginPath(); ctxF.arc(64, 30, 9, 0, Math.PI * 2); ctxF.fill();
        sprites["florax"] = cFlorax;

        // 5. VOLT (Dron de Combate Aéreo)
        const cVolt = document.createElement("canvas");
        cVolt.width = sz; cVolt.height = sz;
        const ctxV = cVolt.getContext("2d");
        ctxV.fillStyle = "#1e222c";
        ctxV.beginPath(); ctxV.arc(64, 56, 32, 0, Math.PI * 2); ctxV.fill();
        ctxV.strokeStyle = CONFIG.COLORS.CYAN; ctxV.lineWidth = 3; ctxV.stroke();
        // Sensor cian
        ctxV.fillStyle = CONFIG.COLORS.CYAN;
        ctxV.fillRect(48, 50, 32, 12);
        // Cañón eléctrico amarillo
        ctxV.fillStyle = CONFIG.COLORS.YELLOW;
        ctxV.fillRect(94, 52, 20, 8);
        // 3 propulsores con llamas azules
        [42, 64, 86].forEach((tx) => {
            ctxV.fillStyle = "#12141a"; ctxV.fillRect(tx - 6, 82, 12, 10);
            ctxV.fillStyle = CONFIG.COLORS.CYAN;
            ctxV.beginPath(); ctxV.moveTo(tx - 5, 92); ctxV.lineTo(tx, 116); ctxV.lineTo(tx + 5, 92); ctxV.fill();
        });
        sprites["volt"] = cVolt;

        // Compatibilidad con tipos anteriores
        sprites["drone"] = cVolt;
        sprites["imp"] = cXyron;
        sprites["baron"] = cBrutus;

        // Cargar texturas oficiales PNG con transparencia para máxima fidelidad gráfica
        ["xyron", "brutus", "nyx", "florax", "volt"].forEach((name) => {
            const img = new Image();
            img.src = `assets/sprites/${name}.png`;
            img.onload = () => {
                sprites[name] = img;
                if (name === "volt") sprites["drone"] = img;
                if (name === "xyron") sprites["imp"] = img;
                if (name === "brutus") sprites["baron"] = img;
            };
        });

        return sprites;
    }
}
