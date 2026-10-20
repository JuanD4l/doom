/**
 * MÓDULO DE ANALÍTICA Y GRÁFICOS // CHART.JS
 * Consume datos en formato JSON desde el backend FastAPI (/api/analytics y /api/stats)
 * y los renderiza en gráficos interactivos con estética Cyberpunk.
 */

class CyberChartsManager {
    constructor() {
        this.modal = document.getElementById("charts-modal");
        this.btnOpenTitle = document.getElementById("btn-open-charts");
        this.btnOpenGameOver = document.getElementById("btn-go-charts");
        this.btnClose = document.getElementById("btn-close-charts");

        this.chartScoresInstance = null;
        this.chartPerformanceInstance = null;

        this._setupListeners();
    }

    _setupListeners() {
        if (this.btnOpenTitle) {
            this.btnOpenTitle.addEventListener("click", (e) => {
                e.stopPropagation();
                this.openModal();
            });
        }

        if (this.btnOpenGameOver) {
            this.btnOpenGameOver.addEventListener("click", (e) => {
                e.stopPropagation();
                this.openModal();
            });
        }

        if (this.btnClose) {
            this.btnClose.addEventListener("click", (e) => {
                e.stopPropagation();
                this.closeModal();
            });
        }

        // Cerrar con Escape si el modal está abierto
        window.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && this.modal && this.modal.classList.contains("active")) {
                this.closeModal();
            }
        });
    }

    openModal() {
        if (!this.modal) return;
        this.modal.classList.add("active");
        this.loadAndRenderCharts();
    }

    closeModal() {
        if (!this.modal) return;
        this.modal.classList.remove("active");
    }

    async loadAndRenderCharts() {
        const loadingIndicator = document.getElementById("charts-loading");
        if (loadingIndicator) loadingIndicator.style.display = "block";

        try {
            const res = await fetch(`${CONFIG.BACKEND_URL}/api/analytics`, {
                headers: { "Accept": "application/json" }
            });

            if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);

            const json = await res.json();
            const data = json.data;

            this._updateMetrics(data.summary);
            this._renderScoresChart(data.labels, data.scores);
            this._renderPerformanceChart(data.labels, data.waves, data.kills);

            if (loadingIndicator) loadingIndicator.style.display = "none";
        } catch (err) {
            console.warn("No se pudo conectar con el backend para analítica. Usando fallback local:", err);
            this._renderFallback();
            if (loadingIndicator) loadingIndicator.style.display = "none";
        }
    }

    _updateMetrics(summary) {
        if (!summary) return;
        const elGames = document.getElementById("metric-games");
        const elKills = document.getElementById("metric-kills");
        const elAvgScore = document.getElementById("metric-avg-score");
        const elAvgWave = document.getElementById("metric-avg-wave");

        if (elGames) elGames.textContent = summary.total_games ?? 0;
        if (elKills) elKills.textContent = summary.total_kills ?? 0;
        if (elAvgScore) elAvgScore.textContent = Math.round(summary.avg_score ?? 0);
        if (elAvgWave) elAvgWave.textContent = (summary.avg_wave ?? 1).toFixed(1);
    }

    _renderScoresChart(labels, scores) {
        const canvas = document.getElementById("chartScores");
        if (!canvas || typeof Chart === "undefined") return;

        if (this.chartScoresInstance) {
            this.chartScoresInstance.destroy();
        }

        const ctx = canvas.getContext("2d");
        const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
        gradient.addColorStop(0, "rgba(0, 243, 255, 0.85)");
        gradient.addColorStop(1, "rgba(255, 0, 127, 0.85)");

        this.chartScoresInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels.length ? labels : ["SIN DATOS"],
                datasets: [{
                    label: "Puntaje Total (PTS)",
                    data: scores.length ? scores : [0],
                    backgroundColor: gradient,
                    borderColor: "#00f3ff",
                    borderWidth: 1.5,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: "#00f3ff",
                            font: { family: "'Share Tech Mono', monospace", size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: "rgba(10, 14, 24, 0.95)",
                        titleColor: "#ffd60a",
                        bodyColor: "#ffffff",
                        borderColor: "#00f3ff",
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: "rgba(0, 243, 255, 0.12)" },
                        ticks: { color: "#a0aec0", font: { family: "'Share Tech Mono', monospace" } }
                    },
                    y: {
                        grid: { color: "rgba(0, 243, 255, 0.08)" },
                        ticks: { color: "#ffffff", font: { family: "'Share Tech Mono', monospace", weight: "bold" } }
                    }
                }
            }
        });
    }

    _renderPerformanceChart(labels, waves, kills) {
        const canvas = document.getElementById("chartPerformance");
        if (!canvas || typeof Chart === "undefined") return;

        if (this.chartPerformanceInstance) {
            this.chartPerformanceInstance.destroy();
        }

        const ctx = canvas.getContext("2d");

        this.chartPerformanceInstance = new Chart(ctx, {
            type: "line",
            data: {
                labels: labels.length ? labels : ["SIN DATOS"],
                datasets: [
                    {
                        label: "Bajas Confirmadas (Kills)",
                        data: kills.length ? kills : [0],
                        borderColor: "#ff007f",
                        backgroundColor: "rgba(255, 0, 127, 0.15)",
                        borderWidth: 2,
                        tension: 0.35,
                        fill: true,
                        pointBackgroundColor: "#ff007f",
                        pointRadius: 4
                    },
                    {
                        label: "Oleada Superada",
                        data: waves.length ? waves : [0],
                        borderColor: "#ffd60a",
                        backgroundColor: "rgba(255, 214, 10, 0.08)",
                        borderWidth: 2,
                        tension: 0.35,
                        fill: true,
                        pointBackgroundColor: "#ffd60a",
                        pointRadius: 4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: "#ffd60a",
                            font: { family: "'Share Tech Mono', monospace", size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: "rgba(10, 14, 24, 0.95)",
                        titleColor: "#ffd60a",
                        bodyColor: "#ffffff",
                        borderColor: "#ff007f",
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { color: "rgba(255, 0, 127, 0.12)" },
                        ticks: { color: "#a0aec0", font: { family: "'Share Tech Mono', monospace" } }
                    },
                    y: {
                        grid: { color: "rgba(255, 0, 127, 0.08)" },
                        ticks: { color: "#ffffff", font: { family: "'Share Tech Mono', monospace" } }
                    }
                }
            }
        });
    }

    _renderFallback() {
        const highscore = parseInt(localStorage.getItem("cyberdoom_highscore") || "0", 10);
        const fallbackLabels = ["LOCAL_RECORD", "CYBER_AGENT", "RECON_01"];
        const fallbackScores = [highscore > 0 ? highscore : 3500, 2400, 1200];
        const fallbackWaves = [3, 2, 1];
        const fallbackKills = [12, 7, 3];

        this._updateMetrics({
            total_games: 3,
            total_kills: 22,
            avg_score: 2366,
            avg_wave: 2.0
        });

        this._renderScoresChart(fallbackLabels, fallbackScores);
        this._renderPerformanceChart(fallbackLabels, fallbackWaves, fallbackKills);
    }
}

// Exponer globalmente
window.cyberCharts = null;
window.addEventListener("DOMContentLoaded", () => {
    window.cyberCharts = new CyberChartsManager();
});
