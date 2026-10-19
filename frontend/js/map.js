/**
 * MAPA Y CONSULTAS ESPACIALES DEL MUNDO (CYBER-ARENA 2099)
 * 0: Suelo libre transitable
 * 1: Placa de acero Cyber-Matrix (Neón Cian)
 * 2: Núcleo de energía Cyber-Core (Neón Magenta)
 * 3: Blindaje Industrial con peligro amarillo/negro
 * 4: Bio-mecánica demoníaca (Neón Rojo)
 */
const GAME_MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 0, 0, 4, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 0, 3, 3, 1],
    [1, 0, 0, 0, 0, 1, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1],
    [1, 0, 3, 3, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 1],
    [1, 2, 0, 2, 2, 0, 0, 4, 0, 0, 4, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
];

const MAP_W = GAME_MAP[0].length;
const MAP_H = GAME_MAP.length;

function isWall(x, y) {
    const gx = Math.floor(x);
    const gy = Math.floor(y);
    if (gx < 0 || gx >= MAP_W || gy < 0 || gy >= MAP_H) {
        return true;
    }
    return GAME_MAP[gy][gx] > 0;
}

function checkLOS(x1, y1, x2, y2, dist) {
    const steps = Math.floor(dist * 5);
    if (steps <= 0) return true;
    const stepX = (x2 - x1) / steps;
    const stepY = (y2 - y1) / steps;
    let currX = x1;
    let currY = y1;
    for (let i = 0; i < steps; i++) {
        currX += stepX;
        currY += stepY;
        if (isWall(currX, currY)) {
            return false;
        }
    }
    return true;
}
