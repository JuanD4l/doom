/**
 * CONFIGURACIÓN GLOBAL DEL CLIENTE WEB
 */
const CONFIG = {
    // Dimensiones del juego
    SCREEN_WIDTH: 960,
    SCREEN_HEIGHT: 680,
    VIEWPORT_HEIGHT: 550,
    HUD_HEIGHT: 130,

    // Raycasting
    FOV: Math.PI / 3,       // 60 grados
    NUM_RAYS: 240,
    MAX_DEPTH: 20.0,
    TEX_SIZE: 64,

    // Paleta de Colores
    COLORS: {
        ABYSS: "#06080e",
        CEILING: "#0e081a",
        FLOOR: "#0a0e18",
        CYAN: "#00f3ff",
        MAGENTA: "#ff007f",
        PURPLE: "#9d4edd",
        GREEN: "#39ff14",
        YELLOW: "#ffd60a",
        ORANGE: "#ff7800",
        RED: "#ff1e3c",
        DARK_METAL: "#141824",
        LIGHT_STEEL: "#a0aec0",
        WHITE: "#ffffff"
    },

    // URL del Backend (con detección automática local/remota y soporte de parámetro ?api=)
    BACKEND_URL: (() => {
        const urlParams = new URLSearchParams(window.location.search);
        const queryApi = urlParams.get("api");
        if (queryApi) {
            localStorage.setItem("cyberdoom_backend_url", queryApi);
            return queryApi.replace(/\/+$/, "");
        }
        const savedApi = localStorage.getItem("cyberdoom_backend_url");
        if (savedApi) return savedApi.replace(/\/+$/, "");

        return (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
            ? "http://localhost:8000"
            : "https://cyberdoom-api.onrender.com";
    })()
};
